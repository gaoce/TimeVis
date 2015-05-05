from __future__ import print_function
import os
from setuptools import setup
from setuptools.command.install import install


# Utility function to read the README file.
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


class MyInstall(install):
    """ Customized install class to initialize database during install
    """
    def run(self):
        import timevis.models as m
        print('Initalizing built-in database')
        m.Base.metadata.create_all(m.engine)
        print('Done initalizing built-in database')
        install.run(self)

# Setup, some thing to note
#   1. zip_safe needs to be False since we need access to templates
setup(
    name="TimeVis",
    version="0.2",
    author="Ce Gao",
    author_email="gaoce@coe.neu.edu",
    description=("TimeVis: An interactive tool to query and visualize "
                 "time series gene expression data"),
    license="MIT",
    install_requires=[
        "Flask>=0.10.1",
        "SQLAlchemy>=1.0.3",
    ],
    packages=['timevis'],
    package_dir={"timevis": "timevis"},
    package_data={
        "timevis": [
            "db/*.db",
            "static/images/*",
            "static/js/*.js",
            "static/js/lib/*.js",
            "static/css/*.css",
            "static/css/lib/*.css",
            "static/css/lib/images/*",
            "templates/*.html",
        ]
    },
    long_description=read('README.md'),
    entry_points={'console_scripts': ['timevis = timevis.app:main']},
    zip_safe=False,
    cmdclass={'install': MyInstall}
)
