from setuptools import setup, find_packages

setup(
    name='mara-app',
    version='1.4.2',

    description="Framework for distributing flask apps across separate packages with minimal dependencies",

    install_requires=[
        'mara-page>=1.2.3',
        'mara-db>=2.0.0',
        'flask>=0.12',
        'alembic>=0.8.10',
        'sqlalchemy-utils>=0.32.14'
    ],

    dependency_links=[
        'git+ssh://git@github.com/mara/mara-page.git@1.2.3#egg=mara-page-1.2.3',
        'git+ssh://git@github.com/mara/mara-db.git@2.0.0#egg=mara-db-2.0.0',
    ],

    packages=find_packages(),

    author='Mara contributors',
    license='MIT',

    entry_points={
    }
)
