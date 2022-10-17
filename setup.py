# coding=utf-8
from setuptools import setup
import sys


if sys.version_info < (3, 5):
    print('Glances requires at least Python 3.5 to run.')
    sys.exit(1)

setup(
    author="Tlntin",
    description="Convert html file to epub",
    url="https://github.com/Tlntin/html2epub",
    name="html2epub",
    version="0.0.1",
    packages=['html2epub'],
    install_requires=[
        "requests>=2.23.0",
    ],
    entry_points={
        'console_scripts':
            [
                'html2epub = html2epub.html2epub:test'
            ]
    },
    # exclude_package_date = {
    #     '': ['.gitignore'],
    #     '': ['dist'],
    #     '': 'build',
    #     '': 'html2epub.egg.info'
    # }
)
