import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

requirements = [
  "ocrmypdf",
  "PyPDF2",
  "pyyaml"
]


setup(
    name = "mailcategorizer",
    version = "0.1",
    author = "Sandro Elsweijer",
    author_email = "sandro.elsweijer(at)gmail.com",
    description = ("A module to automatically sort scanned mails according to keywords."),
    keywords = "automation home mail pdf scan",
    url = "https://github.com/sandro-elsweijer/mailcategorizer",
    packages=["mailcategorizer"],
    long_description=read('README.md'),
    install_requires=requirements,
    entry_points={
      'console_scripts': [
          'mailcategorizer=mailcategorizer.mailcategorizer:main',
      ]
    },
)