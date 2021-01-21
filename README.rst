###############################
Deveal, a reveal.js helper tool
###############################


Deveal is an helper tool for using the marvelous `reveal.js presentation framework <https://revealjs.com>`_.

It provides the ability to

* create a new presentation
* split presentation into multiple files
* easily parameterize the presentation (title, theme, custom css, ...)
* build presentation into a single index.html file
* watch for presentation updates while editing the source files


Deveal is developped in Python 3 and mainly relies on the wonderful
`Jinja2 <http://jinja.pocoo.org>`_, `PyYaml <https://pyyaml.org/>`_ and `watchdog <https://pypi.python.org/pypi/watchdog>`_ packages.



Installation
============

Use the pip installation tool

.. code-block:: shell

    pip install deveal

The dependencies will be automatically installed.


Usage
=====

Deveal is a command line tool. It must be used from within a terminal.

Run the following command to get help

.. code-block:: shell

    deveal --help


deveal new
----------

The ``deveal new`` command creates a new presentation.
As it creates the presentation directory itself, the command must be run in the upper directory where the new presentation will be created

(example below for creating a new presentation named "mynewslideshow")

.. code-block:: shell

    deveal new mynewslideshow


This command creates the minimal required files in the presentation directory

* the **deveal-index.html** template file
* the **deveal.yaml** configuration file

A **deveal.css** file for optional custom styles and a **sections** directory with an example presentation are also created

The deveal-index.html file is the template for the presentation.
It a Jinja2 template rendered throught the ``deveal build`` command, using the variables contained in the deveal.yaml file.
Unless you want to modify the reveal.js configuration, you should not have to modify this template.

The deveal.yaml file contains the configuration for the presentation. It should contains the folling expected variables:

* reveal_path : The path or URL to the installed reveal.js framework ("https://cdn.jsdelivr.net/npm/reveal.js@3.6.0" if not defined)
* reveal_theme : The theme to use for ("black" if not defined)
* content_files : The ordered array of files containing the parts of the presentation
* custom_css : The path to the custom css file if any

Any other variable defined in this file is made available as a Jinja2 variable for the template file.
This may be useful if you plan to customize the template.



deveal build
------------

The ``deveal build`` command builds the presentation as a single **index.html** file using the deveal-index.html and deveal.yaml files

.. code-block:: shell

    deveal build

The obtained index.html file is the presentation itself that can be open throught a web browser.


deveal watch
------------

The ``deveal watch`` command watches for files changes in the presentation directory and subdirectories.
If a change is detected, a build is automatically triggered. Type ``Ctrl+C`` to stop watching.

.. code-block:: shell

    deveal watch


Tips
----

* For an easier writing and maintenance of the presentation, it is encouraged to split the presentation into multiple files (for example title.html, part1.html, part2.html, ...)
* it is encouraged to put the graphics used in the presentation in a dedicated subdirectory (named "graphics" for example)


Authors
=======

Deveal is developed by `Jean-Christophe Fabre <https://github.com/jctophefabre>`_
