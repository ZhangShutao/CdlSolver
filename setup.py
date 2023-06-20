from setuptools import setup

setup(
    name='cdlsolver',
    version='0.1.7',
    packages=['cdlsolver', 'cdlsolver.solver', 'cdlsolver.control', 'cdlsolver.preprocessor'],
    url='',
    license='MIT',
    author='xx',
    author_email='',
    description='A solver for cdl programs',
    python_requires='>=3.6',
    install_requires=[
        'clingo>5.5',
        'clingox>1.0'
    ],
    entry_points={
        'console_scripts': ['cdlsolver=cdlsolver.__main__:main']
    }
)
