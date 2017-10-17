from distutils.core import setup
import setuptools


setup(
    name='scrapehost',
    version='0.1',
    install_requires=[
        'flask',
        'flask_assets',
        'jsmin',
        'pymongo'
    ],
    packages=[
        'scrapehost'
    ],
    entry_points={
        "console_scripts": [
        ]
    }
)
