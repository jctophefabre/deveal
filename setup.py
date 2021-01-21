from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

def version():
    about_file = "deveal/about.py"
    with open(about_file) as f:
        exec(compile(f.read(), about_file, "exec"))
    return locals()["__version__"]

setup(name = 'deveal',
      version = version(),
      description = 'A reveal.js helper tool',
      long_description=readme(),
      author='Jean-Christophe Fabre',
      author_email='jctophe.fabre@gmail.com',
      url='https://github.com/jctophefabre/deveal',
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
          'watchdog',
          'livereload'
      ],
      python_requires='~=3.5',
     )
