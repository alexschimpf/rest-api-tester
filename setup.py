from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='rest_api_tester',
    version='0.1.0',
    author='Alex Schimpf',
    author_email='aschimpf1@gmail.com',
    description='Rest API tester for Python web applications',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/alexschimpf/python-rest-api-tester',
    package_data={'rest_api_tester': ['py.typed']},
    packages=['rest_api_tester'],
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'ujson>=5.6.0',
        'requests>=2.28.1'
    ],
    python_requires='>=3.6'
)