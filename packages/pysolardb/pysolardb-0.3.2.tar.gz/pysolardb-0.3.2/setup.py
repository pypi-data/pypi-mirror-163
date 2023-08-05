from setuptools import setup
from pysolardb import sample

with open("README.md", "r") as readme:
    long_description = readme.read()

setup(
    name='pysolardb',
    version=sample.__version__,
    description='Package used to access the LE2P solar database SolarDB',
    url='https://github.com/LE2P/pysolardb',
    author=sample.__author__,
    author_email='manuparfait@gmail.com',
    license='MIT',
    include_package_data=True,
    packages=['pysolardb', 'pysolardb.sample'],
    install_requires=[
        'outdated>=0.2.1',
        'pandas>=1.4.2',
        'requests>=2.25.1',
        'urllib3>=1.26.9'
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Education',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering'
    ]
)