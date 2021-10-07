import os
from setuptools import setup

# The directory containing this file
HERE = os.path.dirname(os.path.realpath(__file__))

# The text of the README file
with open(HERE + "/README.md", "r") as f:
    README = f.read()

setup(
    name="movielens_private_api",
    version="0.0.1",
    description="A package to interact with Movielens unpublished API",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Mello-Yello/movielens-api",
    author="Giacomo Pigani",
    author_email="pigani.giacomo+movielens@gmail.com",
    license="GPLv3",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    packages=['movielens_private_api'],
    include_package_data=True,
    install_requires=["requests"],
)