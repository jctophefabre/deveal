from __future__ import unicode_literals

__license__ = "GPLv3"
__author__ = "Jean-Christophe Fabre <jctophe.fabre@gmail.com>"


import sys

if sys.version_info[0] < 3:
    raise Exception("Python 3 or a more recent version is required.")


import os
import argparse
import shutil
import time
import subprocess
import yaml
import jinja2
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from .about import __version__


##############################################################################


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SKELETON_DIR = os.path.join(BASE_DIR, "skeleton")

DEFAULT_CONFIG = {
    "reveal_theme": "black",
    "reveal_path": "https://cdn.jsdelivr.net/npm/reveal.js@4.1.0"
}

REVEAL_CLONE_DIR = 'reveal.js'


##############################################################################


class Deveal(FileSystemEventHandler):

    def __init__(self):
        pass

    @staticmethod
    def __print_error(msg):
        print("[ERROR] {}".format(msg))

    @staticmethod
    def __print_warning(msg):
        print("[WARNING] {}".format(msg))

    def __build_vars(self):
        vars = dict()

        if not os.path.isfile("deveal.yaml"):
            Deveal.__print_warning("File deveal.yaml not found. Config file ignored.")
        else:
            with open(os.path.join(os.getcwd(), "deveal.yaml"), 'r') as yaml_file:
                try:
                    vars = yaml.load(yaml_file, Loader=yaml.FullLoader)
                except yaml.YAMLError as E:
                    mark = E.problem_mark
                    Deveal.__print_warning(
                        "Problem reading deveal.yaml file at line {}, column {}. Config file ignored."
                        .format(mark.line+1, mark.column+1)
                    )

        for (key, value) in DEFAULT_CONFIG.items():
            if key not in vars:
                vars[key] = value
                Deveal.__print_warning(
                    "Missing parameter {} in configuration, using defaullt value \"{}\".".format(key, value)
                )

        return vars

    def run_new(self, args):
        dest_dir = os.path.join(os.getcwd(), args['path'])

        if os.path.exists(dest_dir):
            Deveal.__print_error("{} already exists.".format(dest_dir))
            return 1

        print("Creating new slideshow in {}...".format(dest_dir))
        shutil.copytree(SKELETON_DIR, dest_dir)
        print("Done")

        if "with_reveal" in args and args["with_reveal"]:
            ret = self.run_reveal(args)
            if ret == 0:
                # rewrite config file to used cloned reveal repository
                yamlfile_path = os.path.join(dest_dir, 'deveal.yaml')
                with open(yamlfile_path) as yaml_file:
                    vars = yaml.load(yaml_file, Loader=yaml.FullLoader)
                vars['reveal_path'] = REVEAL_CLONE_DIR
                with open(yamlfile_path, 'w') as yaml_file:
                    yaml.dump(vars, yaml_file)
            else:
                return ret

        return 0

    def run_reveal(self, args):
        work_path = os.getcwd()
        if 'path' in args:
            work_path = args['path']

        if not os.path.isdir(work_path):
            Deveal.__print_error("Directory {} not found".format(work_path))
            return 127

        try:
            subprocess.run(["git", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.SubprocessError:
            Deveal.__print_error("Git not found")
            return 127

        is_git_workdir = True
        try:
            subprocess.run(["git", "status"], cwd=work_path, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.SubprocessError:
            is_git_workdir = False

        if is_git_workdir:
            print("Adding reveal.js as git submodule")
            try:
                subprocess.run(
                    ['git', 'submodule', 'add', 'https://github.com/hakimel/reveal.js.git', REVEAL_CLONE_DIR],
                    cwd=work_path
                )
            except subprocess.SubprocessError:
                return 127
        else:
            print("Cloning reveal.js in subdirectory")
            try:
                subprocess.run(
                    ['git', 'clone', 'https://github.com/hakimel/reveal.js.git', REVEAL_CLONE_DIR],
                    cwd=work_path
                )
            except subprocess.SubprocessError:
                return 127

        return 0

    def run_build(self, args):
        vars = self.__build_vars()

        try:
            tpl_filename = "deveal-index.html"
            generated_content = jinja2.Environment(
                                    loader=jinja2.FileSystemLoader(os.getcwd())
                                ).get_template(tpl_filename).render(**vars)
        except jinja2.TemplateSyntaxError as e:
            Deveal.__print_error("Template problem : {} (file {}, line {})".format(e.message, e.filename, e.lineno))
            return 127
        except jinja2.TemplateNotFound:
            Deveal.__print_error("Template not found")
            return 127
        except jinja2.TemplateError:
            Deveal.__print_error("Unknown template problem")
            return 127

        outFile = open(os.path.join(os.getcwd(), "index.html"), "w")
        outFile.write(generated_content)
        outFile.close()
        print("Build on {}".format(time.strftime("%Y-%d-%m %H:%M:%S")))

        return 0

    def on_any_event(self, event):
        if event.src_path != os.path.join(os.getcwd(), "index.html"):
            print("{} is {}".format(os.path.relpath(event.src_path), event.event_type))
            self.run_build(dict())

    def run_watch(self, args):
        print("Watching {} ...".format(os.getcwd()))
        obs = Observer(timeout=0.1)
        obs.schedule(self, path=os.getcwd(), recursive=True)
        obs.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("")
            print("Interrupted by keyboard...")
            obs.stop()

        obs.join()
        print("Done")

        return 0


##############################################################################


def main():

    parser = argparse.ArgumentParser(
        description="Helper tool for creation and management of reveal.js slideshows")

    subparsers = parser.add_subparsers(dest="command_name")

    parser_new = subparsers.add_parser("new", help="create new reveal.js slideshow")
    parser_new.add_argument("path", type=str)
    parser_new.add_argument("--with-reveal", action="store_true",
                            help="donwloads the reveal repository in a subdirectory (requires git)")
    subparsers.add_parser("build", help="build reveal.js slideshow")
    subparsers.add_parser("watch", help="watch for changes and build reveal.js slideshow")
    subparsers.add_parser("reveal", help="donwload the reveal repository in a subdirectory (requires git)")
    subparsers.add_parser("version", help="show deveal version")

    cmd_args = vars(parser.parse_args())

    dvl = Deveal()

    if cmd_args["command_name"] == "new":
        return dvl.run_new(cmd_args)
    elif cmd_args["command_name"] == "reveal":
        return dvl.run_reveal(cmd_args)
    elif cmd_args["command_name"] == "build":
        return dvl.run_build(cmd_args)
    elif cmd_args["command_name"] == "watch":
        return dvl.run_watch(cmd_args)
    elif cmd_args["command_name"] == "version":
        print(__version__)
