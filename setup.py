from setuptools import setup, find_packages

setup(
    name='mara-app',
    version='1.0.3',

    description="Framework for distributing flask apps across separate packages with minimal dependencies",

    install_requires=[
        'mara-page>=1.0.0',
        'mara-db>=1.0.0',
        'flask>=0.12',
        'alembic>=0.8.10'
    ],

    dependency_links=[
        'https://github.com/mara/mara-page.git@1.0.0#egg=mara-page'
        'https://github.com/mara/mara-db.git@1.0.0#egg=mara-db'
    ],

    packages=find_packages(),

    author='Mara contributors',
    license='MIT',

    entry_points={
    }
)
