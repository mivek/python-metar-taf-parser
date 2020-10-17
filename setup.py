import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="metar-taf-parser-mivek",
    version="0.0.1",
    author="Jean-Kevin KPADEY",
    author_email="jeankevin.kpadey@gmail.com",
    description="Python project parsing metar and taf message",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mivek/python-metar-taf-parser",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['parameterized'],
    keywords='metar taf parser icao airport',
)
