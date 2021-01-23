__license__ = "GPLv3"
__author__ = "Jean-Christophe Fabre <jctophe.fabre@gmail.com>"

from unittest import TestCase

import os
import shutil
import tempfile

from deveal import about
from deveal.__main__ import Deveal


EXEC_DIR = os.path.join(tempfile.gettempdir(), "deveal_tests_exec")


class DevealTests(TestCase):

    @classmethod
    def setUpClass(cls):
        print("Execution directory: {}".format(EXEC_DIR))
        shutil.rmtree(EXEC_DIR, ignore_errors=True)
        os.makedirs(EXEC_DIR)

    # check version string is available
    def test_001_version(self):
        print(about.__version__)
        self.assertTrue(len(about.__version__) > 0)

    # check creation of a new slideshow
    def test_010_new(self):
        dvl = Deveal()
        os.chdir(EXEC_DIR)
        args = {"path": "slides"}
        self.assertEqual(dvl.run_new(args), 0)
        slides_dir = os.path.join(EXEC_DIR, "slides")
        self.assertTrue(os.path.isfile(os.path.join(slides_dir, "deveal.yaml")))
        self.assertTrue(os.path.isfile(os.path.join(slides_dir, "deveal-index.html")))
        self.assertTrue(os.path.isfile(os.path.join(slides_dir, "deveal.css")))
        self.assertTrue(os.path.isdir(os.path.join(slides_dir, "sections")))

    # check creation of a new slideshow with cloning of reveal.js
    def test_011_new_withreveal(self):
        dvl = Deveal()
        os.chdir(EXEC_DIR)
        args = {"path": "slideswithreveal", "with_reveal": True}
        self.assertEqual(dvl.run_new(args), 0)
        slides_dir = os.path.join(EXEC_DIR, "slideswithreveal")
        self.assertTrue(os.path.isdir(slides_dir))
        self.assertTrue(os.path.isdir(os.path.join(slides_dir, "reveal.js")))

    # check detection of existing slideshow when attempting to create one with the same name
    def test_012_new_alreadyexists(self):
        dvl = Deveal()
        os.chdir(EXEC_DIR)
        args = {"path": "slides"}
        self.assertNotEqual(dvl.run_new(args), 0)

    # check build of a slideshow
    def test_020_build(self):
        dvl = Deveal()
        slides_dir = os.path.join(EXEC_DIR, "slides")
        os.chdir(slides_dir)
        args = {}
        self.assertEqual(dvl.run_build(args), 0)
        self.assertTrue(os.path.isfile(os.path.join(slides_dir, "index.html")))

    # check management of missing main template
    def test_021_build_templateerror_missingindex(self):
        dvl = Deveal()
        os.chdir(EXEC_DIR)
        args = {"path": "slidestplindex"}
        self.assertEqual(dvl.run_new(args), 0)
        slides_dir = os.path.join(EXEC_DIR, "slidestplindex")
        os.remove(os.path.join(slides_dir, "deveal-index.html"))
        os.chdir(slides_dir)
        args = {}
        self.assertEqual(dvl.run_build(args), 127)
        self.assertFalse(os.path.isfile(os.path.join(slides_dir, "deveal-index.html")))

    # check management of missing included template
    def test_022_build_templateerror_missingsections(self):
        dvl = Deveal()
        os.chdir(EXEC_DIR)
        args = {"path": "slidestplsections"}
        self.assertEqual(dvl.run_new(args), 0)
        slides_dir = os.path.join(EXEC_DIR, "slidestplsections")
        shutil.rmtree(os.path.join(slides_dir, "sections"))
        os.chdir(slides_dir)
        args = {}
        self.assertEqual(dvl.run_build(args), 127)
        self.assertFalse(os.path.isdir(os.path.join(slides_dir, "sections")))

    # check cloning of reveal.js in an existing slideshow
    def test_030_clonereveal(self):
        dvl = Deveal()
        slides_dir = os.path.join(EXEC_DIR, "slides")
        os.chdir(slides_dir)
        args = {}
        self.assertFalse(os.path.exists(os.path.join(slides_dir, "reveal.js")))
        self.assertEqual(dvl.run_reveal(args), 0)
        self.assertTrue(os.path.isdir(os.path.join(slides_dir, "reveal.js")))
