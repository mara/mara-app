from setuptools import setup, find_packages


def get_long_description():
    with open('README.md') as f:
        return f.read()


setup(
    name='mara-app',
    version='2.1.0',

    description="Framework for distributing flask apps across separate packages with minimal dependencies",

    long_description=get_long_description(),
    long_description_content_type='text/markdown',

    python_requires='>=3.6',

    install_requires=[
        'mara-page>=1.4.1',
        'mara-db>=3.0.0',
        'flask>=1.0.2'
    ],

    extras_require={
        'test': ['pytest', 'pytest_click'],
    },

    packages=find_packages(),

    author='Mara contributors',
    license='MIT',

    entry_points={}
)
