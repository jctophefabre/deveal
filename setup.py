from setuptools import setup

setup(name = 'deveal',
      version = '0.0.3',
      description = '',
      author='Jean-Christophe Fabre',
      author_email='jean-christophe.fabre@inra.fr',
      url='http://github.com/fabrejc/deveal',
      license='GPLv3',
      packages = ['deveal'],
      package_data={
          'deveal': ['skeleton/*']
      },
      include_package_data=True,
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
