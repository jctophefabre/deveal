from setuptools import setup

setup(name = 'deveal',
      version = '0.0.1',
      description = '',
      author='Jean-Christophe Fabre',
      author_email='jean-christophe.fabre@inra.fr',
      url='http://github.com/fabrejc/deveal',
      license='GPLv3',
      packages = ['deveal'],
      entry_points = {
          'console_scripts': [
              'deveal = deveal.__main__:main'
          ]
      },
      install_requires = [
          'argparse',
          'jinja2 >= 2.7',
          'PyYAML',
          'watchdog'
      ]
     )
