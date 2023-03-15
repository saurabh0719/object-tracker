import pathlib
from distutils.core import setup

long_description = pathlib.Path("README.rst").read_text()

setup(
    name="object-tracker",
    packages=["object_tracker"],
    version="0.1.1",
    license="three-clause BSD",
    description="A pure python object change and history tracker. Monitor all changes in your objects lifecycle and trigger callback functions to capture them.",
    long_description=long_description,
    long_description_content_type= 'text/x-rst',
    author="Saurabh Pujari",
    author_email="saurabhpuj99@gmail.com",
    url="https://github.com/saurabh0719/object-tracker",
    keywords=[
        "object_tracker", 
        "object-tracker", 
        "changelog",
        "object history", 
        "tracker", 
        "change tracker", 
        "history"
    ],
    project_urls={
        "Documentation": "https://github.com/saurabh0719/object-tracker#README",
        "Source": "https://github.com/saurabh0719/object-tracker",
    },
    install_requires=[],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
    ],
)
