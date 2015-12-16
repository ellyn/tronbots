from distutils.core import setup
from Cython.Build import cythonize

setup(
    name = 'tronbots app',
    ext_modules = cythonize("*.pyx")
)
