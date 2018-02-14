from distutils.core import setup

setup(name='slurpbox',
      version='1.0',
      description='Download all files from a Box.com folder',
      author='Quasar Jarosz',
      author_email='quasar@uams.edu',
      #url='https://www.python.org/sigs/distutils-sig/',
      packages=['slurpbox'],
      scripts=['bin/slurpbox'],
      install_requires=[
          'pycurl >= 7.43.0.1',
          'PyYAML >= 3.12',
          'tqdm >= 4.19.5',
          'lxml >= 4.1.1',
      ]
     )
