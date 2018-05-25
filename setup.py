from distutils.core import setup

setup(name='slurpbox',
      version='1.1',
      description='Download all files from a Box.com folder',
      author='Quasar Jarosz',
      author_email='quasar@uams.edu',
      url='http://pypi.python.org/pypi/Slurpbox/',
      license='LICENSE.txt',
      packages=['slurpbox'],
      scripts=['bin/slurpbox'],
      long_description=open('README.txt').read(),
      install_requires=[
          'pycurl >= 7.43.0.1',
          'PyYAML >= 3.12',
          'tqdm >= 4.19.5',
          'lxml >= 4.1.1',
      ]
     )
