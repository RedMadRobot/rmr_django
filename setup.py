from distutils.core import setup
from setuptools import find_packages

with open('README.md') as description:
    long_description = description.read()

setup(
    name='rmr-django',
    version='1.1.5',
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
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Environment :: Web Environment',
    ],
    install_requires=[
        'crcmod>=1.7,<2.0',
        'django-cache>=0.1,<0.2',
        'pytz',
    ],
)
