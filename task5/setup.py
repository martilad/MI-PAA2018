from setuptools import setup
from Cython.Build import cythonize
import numpy

setup(
    name='GA-CNFSolver',
    ext_modules=cythonize('GA.pyx', language_level=3),
    include_dirs=[numpy.get_include()],
    setup_requires=[
        'Cython',
        'NumPy',
    ],
    install_requires=[
        'NumPy',
    ],
)