import os
from setuptools import setup


# Utility function to read the README file.
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

# Setup, some thing to note
#   1. zip_safe needs to be False since we need access to templates/
setup(
    name="TimeVis",
    version="0.1",
    author="Ce Gao",
    author_email="gaoce@coe.neu.edu",
    description=("TimeVis: An interactive tool to query and visualize "
                 "time series gene expression data"),
    license="MIT",
    packages=['timevis'],
    package_dir={"timevis": "timevis"},
    package_data={
        "timevis": [
            "static/js/*.js",
            "templates/*.html",
        ]
    },
    long_description=read('README.md'),
    entry_points={'console_scripts': ['timevis = timevis.app:main']},
    zip_safe=False
)
