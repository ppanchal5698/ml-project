from typing import List

from setuptools import find_packages, setup

HYPHEN_E_DOT = "-e ."

def get_requirements(file_path:str) -> List[str]:
    """
    This function will return the list of requirements from a given file path
    """
    with open(file_path) as f:
        requirements = f.read().splitlines()
        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)
    return requirements

setup(
    name="ml-project",
    version="0.1.0",
    author="Parth Panchal",
    author_email="coding.parthpanchal@gmail.com",
    packages = find_packages(),
    install_requires=get_requirements("requirements.txt")
)
