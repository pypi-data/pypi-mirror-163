from setuptools import setup, find_packages
from pathlib import Path

# read the contents of your README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='medusa-kernel',
    packages=find_packages(),
    include_package_data=True,
    version='0.2.6',
    keywords=['Signal', 'Biosignal', 'EEG', 'BCI'],
    url='https://medusabci.com/medusa-kernel',
    author='Eduardo Santamaría-Vázquez, '
           'Víctor Martínez-Cagigal, '
           'Víctor Rodríguez-González, '
           'Diego Marcos-Martínez, '
           'Sergio Pérez-Velasco',
    author_email='eduardo.santamaria@gib.tel.uva.es',
    license='MIT',
    install_requires=[
        'numpy',
        'scipy',
        'matplotlib',
        'numba',
        'sklearn',
        'statsmodels',
        'bson',
        'h5py',
        'dill',
        'tqdm',
        'tensorflow'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3 :: Only',
    ],
    description='Advanced biosignal processing toolbox',
    long_description=long_description,
    long_description_content_type='text/markdown'
)
