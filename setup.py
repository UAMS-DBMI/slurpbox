from distutils.core import setup

setup(name='slurpbox',
      version='1.3',
      description='Download all files from a Box.com folder',
      author='Quasar Jarosz',
      author_email='quasar@uams.edu',
      url='https://github.com/UAMS-DBMI/slurpbox',
      license='LICENSE.txt',
      packages=['slurpbox'],
      scripts=['bin/slurpbox'],
      long_description=open('README.txt').read(),
      install_requires=[
          'requests >= 2.18.4',
          'tqdm >= 4.19.5',
          'lxml >= 4.1.1',
      ]
     )
