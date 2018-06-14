from setuptools import setup

setup(
    # Application name:
    name="avto-scraper",

    # Version number:
    version="0.1.0",

    # Application author details:
    author="aljaz erzen",
    author_email="aljaz.erzen@gmail.com",

    # Packages
    packages=["app"],

    # Include additional files into the package
    include_package_data=False,

    # Details
    url="http://aljaz.erzen.si",

    #
    # license="LICENSE.txt",
    description="Script that sends reports about new cars on avto.net",

    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=[
        "beautifulsoup4", "certifi", "PyYAML", "urllib3", "flask"
    ],
)
