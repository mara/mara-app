from setuptools import setup, find_packages

setup(
    name='mara-app',
    version='2.0.0',

    description="Framework for distributing flask apps across separate packages with minimal dependencies",

    python_requires='>=3.6',

    install_requires=[
        'mara-page>=1.4.1',
        'mara-db>=3.0.0',
        'flask>=1.0.2'
    ],

    dependency_links=[
    ],

    packages=find_packages(),

    author='Mara contributors',
    license='MIT',

    entry_points={
    }
)
