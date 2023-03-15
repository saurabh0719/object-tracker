import pathlib
from distutils.core import setup

long_description = pathlib.Path("README.rst").read_text()

setup(
    name="hawk-eye",
    packages=["hawk_eye"],
    version="0.1.0",
    license="three-clause BSD",
    description="A pure python object change and history tracker. Monitor all changes in your objects lifecycle and trigger callback functions to capture them.",
    long_description=long_description,
    long_description_content_type= 'text/x-rst',
    author="Saurabh Pujari",
    author_email="saurabhpuj99@gmail.com",
    url="https://github.com/saurabh0719/elara",
    keywords=[
        "hawk-eye", 
        "changelog",
        "object history", 
        "tracker", 
        "change tracker", 
        "history"
    ],
    project_urls={
        "Documentation": "https://github.com/saurabh0719/hawk-eye#README",
        "Source": "https://github.com/saurabh0719/hawk-eye",
    },
    install_requires=[],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
    ],
)
