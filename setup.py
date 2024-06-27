from setuptools import setup, find_packages

setup(
    name='nitrous-oxi',
    version='0.2.0',
    description='A Python client for the Nitrous-Oxi API',
    packages=find_packages(),
    install_requires=[
        'requests',
        'prompt_toolkit',
        'rich'
        'argparse'
    ],
    entry_points={
        'console_scripts': [
            'nitrous-oxi=nitrous_oxi.cli:main',
        ],
    },
)
