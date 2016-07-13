from distutils.core import setup
from setuptools import find_packages

with open('README.md') as description:
    long_description = description.read()

setup(
    name='rmr-django',
    version='1.0.31',
    author='Rinat Khabibiev',
    author_email='srenskiy@gmail.com',
    packages=list(map('rmr.'.__add__, find_packages(where='rmr'))) + ['rmr'],
    url='https://github.com/RedMadRobot/rmr_django',
    license='MIT',
    description='rmr_django',
    long_description=long_description,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    install_requires=[
        'django>=1.8,<2.0',
        'crcmod>=1.7,<2.0',
        'psycopg2>=2.6,<3.0',
    ],
)
