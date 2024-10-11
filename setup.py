from setuptools import setup, find_packages

setup(
    name='SimplifierClient',
    version='0.3',
    packages=find_packages(),
    install_requires=[
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'fhirpackage=simplifierclient.cli:cli',
        ],
    },
)
