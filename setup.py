from setuptools import setup, find_packages

setup(
    name='piaf-edit',
    version='0.0.1-dev0',
    packages=find_packages(),
    author='flegac',
    description='',
    install_requires=[line for line in open('requirements.txt')],
)
