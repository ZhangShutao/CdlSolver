from setuptools import setup

setup(
    name='alpsolver',
    version='0.1.8',
    packages=['alpsolver', 'alpsolver.solver', 'alpsolver.control', 'alpsolver.preprocessor'],
    url='',
    license='MIT',
    author='xx',
    author_email='',
    description='A solver for ALP programs',
    python_requires='>=3.6',
    install_requires=[
        'clingo>5.5',
        'clingox>1.0'
    ],
    entry_points={
        'console_scripts': ['alpsolver=alpsolver.__main__:main']
    }
)
