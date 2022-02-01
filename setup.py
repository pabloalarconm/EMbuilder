# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
with open('README.md') as readme_file:
    readme = readme_file.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="EMbuilder",
    version="0.0.4",
    packages=["embuilder"],
    author="Pablo Alarcón Moreno",
    author_email="pabloalarconmoreno@gmail.com",
    url="https://github.com/pabloalarconm/EMbuilder",
    description="Etemenanki Builder -- Python-controlled YARRRML builder",
    license="MIT",
    keywords=["YAML","YARRRML","RDF","FAIR","EJP"]
    #long_description=readme
)