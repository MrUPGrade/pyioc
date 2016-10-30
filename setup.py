# coding=utf-8
from setuptools import setup

setup(
    name='pyioc',
    version='0.2.1',
    packages=['pyioc'],
    url='https://github.com/MrUPGrade/pyioc',
    license='MIT',
    author='Jakub (Mr. UPGrade) Czapliński',
    author_email='itsupgradetime@gmail.com',
    description='Python IoC tools.',
    install_requires=[
        'six>=1.9.0',
        'future>=0.15.2',
        'enum34>=1.1.1',
    ],
    extras_require={
        'test': [
            'pytest>=2.7.3',
            'mock>=1.0.1',
            'coverage>=4.0.0'
        ],
        'dev': [
            'ipython'
        ],
        'docs': [
            'sphinx'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5"
    ]
)
