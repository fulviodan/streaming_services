import setuptools,os

def get_requirements():
    return [x for x in open("./requirements.txt").read().split("\n") if not x.startswith("pkg_resources")]

import json
ppom=json.load(open("./ppom.json"))
version=None

setuptools.setup(
    name="streaming_services",
    version=version,
    author="Live Tech",
    author_email="f.dantonio@eilivetech.it",
    description="",
    long_description="",
    python_requires='>3.5.0',
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=get_requirements()

)
