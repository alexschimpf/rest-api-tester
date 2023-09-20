import json
from setuptools import setup


with open('README.md', 'r') as readme_file:
    long_description = readme_file.read()

with open('requirements.txt', 'r') as requirements_file:
    requirements_list = requirements_file.readlines()

with open('package.json', 'r') as package_file:
    package_dict = json.loads(package_file.read().strip())
    version = package_dict['version']

setup(
    name='rest_api_tester',
    version=version,
    author='Alex Schimpf',
    author_email='aschimpf1@gmail.com',
    description='Rest API tester',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/alexschimpf/python-rest-api-tester',
    packages=[
        '',
        'rest_api_tester',
        'rest_api_tester.parser',
        'rest_api_tester.client'
    ],
    package_data={
        '': ['README.md', 'requirements.txt', 'package.json'],
        'rest_api_tester': ['py.typed']
    },
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11'
    ],
    install_requires=requirements_list,
    python_requires='>=3.7'
)
