# Import required functions
from setuptools import setup, find_packages

# Call setup function
setup(
    author="Qiana Yang",
    description="A python package of useful functions to be used on FAO's AQUASTAT dataset.",
    name="aquastat",
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    version="0.0.1",
    python_requires='>=3.6, <4',
    install_requires=['pandas', 'matplotlib', 'seaborn'],
    tests_require=['pytest', 'numpy', 'pandas'],
)
