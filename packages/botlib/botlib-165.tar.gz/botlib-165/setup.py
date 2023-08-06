# This file is placed in the Public Domain.


from setuptools import setup


def read():
    return open("README.rst", "r").read()


setup(
    name="botlib",
    version="165",
    url="https://github.com/bthate/botlib",
    author="Bart Thate",
    author_email="bthate67@gmail.com",
    description="The Python3 bot Namespace",
    long_description=read(),
    install_requires=["oplib"],
    license="Public Domain",
    packages=["bot"],
    zip_safe=False,
    scripts=["bin/bot", "bin/botc"],
    include_package_data=True,
    data_files=[
                ("share/doc/botlib", ["README.rst",]),
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: Public Domain",
        "Operating System :: Unix",
        "Programming Language :: Python",
        "Topic :: Utilities",
    ],
)
