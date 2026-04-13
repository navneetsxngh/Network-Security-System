'''
The setup.py file is an essential part of packagaing and distributing python projects.
It is Used by setuptools to define the configuration of your project, such as its metadata, dependencies and more.
'''

from setuptools import find_packages, setup
from typing import List

def get_requirements() -> List[str]:
    """
    This Function will return list of requirements
    """
    requirement_list: List[str] = []
    try:
        with open('requirements.txt', 'r') as file:
            ## Read Lines from the file
            lines = file.readlines()

            for line in lines:
                requirement = line.strip()
                ## ignore empty and -e .
                if requirement and requirement != '-e .':
                    requirement_list.append(requirement)
    except FileNotFoundError:
        print("requirements.txt Not Found")
    
    return requirement_list

setup(
    name="Network Security",
    version="0.0.1",
    author="Navneet Singh",
    author_email="singhnavneet2590@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()
)