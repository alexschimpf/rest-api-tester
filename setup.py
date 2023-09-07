from setuptools import setup

with open('README.md', 'r') as readme_file:
    long_description = readme_file.read()

with open('requirements.txt', 'r') as requirements_file:
    requirements_list = requirements_file.readlines()

setup(
    name='rest_api_tester',
    version='0.2.0',
    author='Alex Schimpf',
    author_email='aschimpf1@gmail.com',
    description='Rest API tester',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/alexschimpf/python-rest-api-tester',
    package_data={'rest_api_tester': ['py.typed']},
    packages=[
        'rest_api_tester',
        'rest_api_tester.parser',
        'rest_api_tester.client'
    ],
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11'
    ],
    install_requires=requirements_list,
    python_requires='>=3.9'
)
