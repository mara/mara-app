import pathlib
from setuptools import setup, find_packages


def get_long_description():
    with open('README.md') as f:
        return f.read()


def add_file_to_package(main_path: str, sub_path: str) -> [str]:
    module_path = pathlib.Path(main_path)
    files = []
    for file in module_path.glob(sub_path):
        if file.is_file():
            files.append(str(file.relative_to(module_path)))
    return files


packaged_files = add_file_to_package(main_path="mara_app", sub_path="static/**/*") + \
        add_file_to_package(main_path="mara_app", sub_path=".scripts/*")

setup(
    name='mara-app',
    version='2.3.0',

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
    package_data={'mara_app': packaged_files},

    author='Mara contributors',
    license='MIT',

    entry_points={}
)
