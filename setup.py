# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
with open('README.md') as readme_file:
    readme = readme_file.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="EMbuilder",
    version="0.0.14",
    packages=["embuilder"],
    author="Pablo Alarcón Moreno",
    author_email="pabloalarconmoreno@gmail.com",
    url="https://github.com/pabloalarconm/EMbuilder",
    description="Etemenanki Builder -- Semantic implementation builder",
    license="MIT",
    keywords=["YARRRML","OBDA","RDF","ShEx","FAIR","EJP"]
    #long_description=readme
)