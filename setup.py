"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
import setuptools
#, find_packages
# To use a consistent encoding
# from codecs import open
# from os import path

# here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
# with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
#     long_description = f.read()

setuptools.setup(
    setup_requires=['pbr>=1.8'],
    pbr=True
)
