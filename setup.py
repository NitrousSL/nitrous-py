from setuptools import setup, find_packages

setup(
    name='nitrous-oxide',
    version='0.2.0',
    description='A Python client for the Nitrous-Oxide API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='NITROUSOXIDE',  
    author_email='hello@nitrous-oxi.de',  
    url='https://github.com/NitrousSL/nitrous-py',  
    packages=find_packages(),
    install_requires=[
        'requests',
        'prompt_toolkit',
        'rich'
    ],
    entry_points={
        'console_scripts': [
            'nitrous-oxide=nitrous_oxide.cli:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GPLv3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
