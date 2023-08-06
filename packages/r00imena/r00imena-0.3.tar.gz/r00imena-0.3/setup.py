from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='r00imena',
    version='0.3',
    license='MIT',
    author="Andrey Ivanov",
    author_email='r00ft1h@gmail.com',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.rst')).read(),
    package_data={'': ['*.txt']},
)