from setuptools import setup
from os import path

current_dir = path.abspath(path.dirname(__file__))

with open(path.join(current_dir, "README.md"), "r") as f:
    readme = f.read()

setup(
    name="wisty",
    version="1.0.0",
    url="https://github.com/knowbee/wisty.git",
    author="Igwaneza Bruce",
    author_email="knowbeeinc@gmail.com",
    description="A fast minimal command line tool to download videos hosted on wistia with video id",
    long_description=readme,
    long_description_content_type="text/markdown",
    platforms="any",
    python_requires=">=3.6",
    packages=["wisty"],
    install_requires=[
        "click == 7.1.2",
        "requests == 2.23.0",
        "tqdm==4.54.1",
    ],
    entry_points={"console_scripts": ["wisty = wisty:main"]},
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
)
