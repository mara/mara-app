from setuptools import setup, find_packages

setup(
    name='mara-app',
    version='1.3.0',

    description="Framework for distributing flask apps across separate packages with minimal dependencies",

    install_requires=[
        'mara-page>=1.2.0',
        'mara-db>=1.0.1',
        'flask>=0.12',
        'alembic>=0.8.10',
        'sqlalchemy-utils>=0.32.14'
    ],

    dependency_links=[
        'http://github.com/mara/mara-page/tarball/master#egg=mara-page-1.2.0',
        'http://github.com/mara/mara-db/tarball/master#egg=mara-db-1.0.1'
    ],

    packages=find_packages(),

    author='Mara contributors',
    license='MIT',

    entry_points={
    },
    python_requires='>=3.6'

)
