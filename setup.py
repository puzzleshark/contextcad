from setuptools import setup, find_packages


with open("requirements.txt") as requirement_file:
    requirements = requirement_file.read().split()


setup(
    name="contextcad",
    version="0.0.1",
    author="Samuel Banning",
    author_email="samcbanning@gmail.com",
    install_requires=requirements,
    packages=find_packages()
)