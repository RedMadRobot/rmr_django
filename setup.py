from distutils.core import setup

with open('README.md') as description:
    long_description = description.read()

setup(
    name='rmr_django',
    version='1.0.25',
    author='Rinat Khabibiev',
    author_email='rh@redmadrobot.com',
    packages=[
        'rmr',
        'rmr/extensions',
        'rmr/extensions/middleware',
        'rmr/models',
        'rmr/models/fields',
        'rmr/views',
    ],
    url='https://github.com/RedMadRobot/rmr_django',
    license='MIT',
    description='rmr_django',
    long_description=long_description,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
    ],
    install_requires=[
        'django>=1.8,<2.0',
        'crcmod>=1.7,<2.0',
        'psycopg2>=2.6,<3.0',
    ],
)
