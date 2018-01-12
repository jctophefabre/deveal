__license__ = "GPLv3"
__author__ = "Jean-Christophe Fabre <jean-christophe.fabre@inra.fr>"


##############################################################################
##############################################################################


import os
import jinja2
import argparse
import shutil
import yaml
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


##############################################################################
##############################################################################


BaseDir = os.path.dirname(os.path.abspath(__file__))
SkeletonDir = os.path.join(BaseDir,"skeleton")


##############################################################################
##############################################################################



class Deveal(FileSystemEventHandler):

  def __init__(self):
    pass


##############################################################################


  def __buildVars(self):
    Vars = dict()

    with open(os.path.join(os.getcwd(),"deveal.yaml"), 'r') as YAMLFile:
      try:
        Vars = yaml.load(YAMLFile)
      except yaml.YAMLError as E:
        print(exc)

    return Vars


##############################################################################


  def runNew(self,Args):
    DestDir = os.path.join(os.getcwd(),Args['path'])
    print("Creating new slideshow in %s..." % DestDir)
    shutil.copytree(SkeletonDir,DestDir)
    print("Done")


##############################################################################


  def runBuild(self,Args):
    Vars = self.__buildVars()

    TplFilename = "deveal-index.html"
    GeneratedContent = jinja2.Environment(loader=jinja2.FileSystemLoader(os.getcwd())).get_template(TplFilename).render(**Vars)

    OutFile = open(os.path.join(os.getcwd(),"index.html"),"w")
    OutFile.write(GeneratedContent.encode('utf8'))
    OutFile.close()

    print("Build on %s" % time.strftime("%Y-%d-%m %H:%M:%S"))


##############################################################################


  def on_any_event(self, event):
    if event.src_path != os.path.join(os.getcwd(),"index.html"):
      print("%s is %s" % (os.path.relpath(event.src_path),event.event_type))
      self.runBuild(dict())


##############################################################################


  def runWatch(self,Args):
    print("Watching %s ..." % os.getcwd())
    Obs = Observer(timeout=0.1)
    Obs.schedule(self, path=os.getcwd(), recursive=True)
    Obs.start()

    try:
      while True:
        time.sleep(1)
    except KeyboardInterrupt:
      print ""
      print("Interrupted by keyboard...")
      Obs.stop()

    Obs.join()
    print("Done")


##############################################################################
##############################################################################


def main():

  Parser = argparse.ArgumentParser(description="Helper tool for creation and management of reveal.js slideshows")

  SubParsers = Parser.add_subparsers(dest="command_name")

  ParserNew = SubParsers.add_parser("new",help="create new reveal.js slideshow")
  ParserNew.add_argument("path",type=str)
  ParserBuild = SubParsers.add_parser("build",help="build reveal.js slideshow")
  ParserWatch = SubParsers.add_parser("watch",help="watch for changes and build reveal.js slideshow")

  Args = vars(Parser.parse_args())

  Dvl = Deveal()

  if Args["command_name"] == "new":
    Dvl.runNew(Args)
  elif Args["command_name"] == "build":
    Dvl.runBuild(Args)
  elif Args["command_name"] == "watch":
    Dvl.runWatch(Args)
