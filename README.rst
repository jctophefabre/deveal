===============================
Deveal, a reveal.js helper tool
===============================


Deveal is an helper tool for using the marvelous `reveal.js presentation framework <https://revealjs.com>`_.

It provides the ability to

* create a new presentation
* split presentation into multiple files
* build presentation into a single index.html file
* watch for presentation updates while editing the source files
* parameterize the usage of reveal.js (title, theme, custom css, ...)

Deveal is developped in Python and mainly relies on Jinja2, PyYaml and watchdog packages.

Installation
------------

Use the pip installation tool

.. code-block:: shell

    pip install deveal


Usage
-----

Run the following command to get help

.. code-block:: shell

    deveal --help
