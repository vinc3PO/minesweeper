from setuptools import setup, find_packages

setup(
    name='mines',
    version='1.1',
    packages=find_packages(),
    install_requires=[
        'PyQt5>=5.14.1',
    ],
    entry_points={'console_scripts':'mines=minesweeper.__main__:main'}
)