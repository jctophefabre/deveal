from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name = 'deveal',
      version = '1.1.0',
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
