'''
1. Essential for packaging and distributing Python Projects.
2. Used by setuptools to define configuration of project such as meta data, dependencies
'''
from setuptools import find_packages,setup
from typing import List 

def get_requirements() -> List[str]:

    requirements_list:List[str]=[]
    try:
        with open('requirements.txt', 'r') as f:
            ## Read Lines
            lines=f.readlines()
            ## processing Each line
            for line in lines:
                ## Removeing spaces
                requirements=line.strip()
                ## ignoring empty lines and -e .
                if requirements and not requirements.startswith('-e'):
                    requirements_list.append(requirements)
    except FileNotFoundError:
        print("No requirements.txt file found")

    return requirements_list

## Setting Up Meta data
setup(
    name='NetworkSecurity',
    version='1.0.0',
    packages=find_packages(),
    install_requires=get_requirements(),
    author='Hammad Nasir',
    author_email='hammadnasir797@gmail.com',
    )



