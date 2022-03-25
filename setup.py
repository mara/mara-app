import pathlib
from setuptools import setup, find_packages


def get_long_description():
    with open('README.md') as f:
        return f.read()

def static_files() -> [str]:
    module_path = pathlib.Path('mara_app')
    files = []
    for p in module_path.glob('static/**/*'):
        if p.is_file():
            files.append(str(p.relative_to(module_path)))
    return files


setup(
    name='mara-app',
    version='2.2.1',

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
    package_data={'mara_app': static_files()},

    author='Mara contributors',
    license='MIT',

    entry_points={}
)
