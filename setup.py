# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
with open('README.md') as readme_file:
    readme = readme_file.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="EMbuilder",
    version="0.0.1",
    packages=find_packages(),
    author="Pablo Alarcón Moreno",
    author_email="pabloalarconmoreno@gmail.com",
    url="https://github.com/pabloalarconm/EMB",
    description="Etemenanki Builder -- Python-controlled YARRRML builder",
    license="MIT",
    keywords=["YAML","YARRRML","RDF","FAIR","EJP"],
    long_description=readme
)