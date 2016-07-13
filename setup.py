# -*- coding: utf-8 -*-
import os.path
from setuptools import setup

project_name = 'bravado-falcon'
version = '0.0.1'

setup_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(setup_dir, 'requirements.txt')) as req_file:
    requirements = [lib.split('==')[0] for lib in req_file.readlines()]
with open(os.path.join(setup_dir, 'README.rst')) as readme_file:
    readme = readme_file.read()

setup(
    name=project_name,
    version=version,
    description='Integration of Falcon API unit tests with Bravado.',
    long_description=readme,
    author='Michał Bultrowicz',
    author_email='michal.bultrowicz@gmail.com',
    url='https://github.com/butla/bravado-falcon',
    packages=[
        project_name.replace('-', '_'),
    ],
    package_dir={project_name: project_name},
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    keywords='falcon bravado test',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
    ],
)
