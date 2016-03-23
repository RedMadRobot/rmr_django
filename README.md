# rmr_django

Template Django project

master: [![Build Status](https://travis-ci.org/RedMadRobot/rmr_django.svg)](https://travis-ci.org/RedMadRobot/rmr_django)
version_1.x: [![Build Status](https://travis-ci.org/RedMadRobot/rmr_django.svg?branch=version_1.x)](https://travis-ci.org/RedMadRobot/rmr_django)

## Install
* add `-e git+https://github.com/RedMadRobot/rmr_django.git#egg=rmr-django` to the list of your requirements (requirements.txt)
* add 'rmr.extensions.middleware.cache.UpdateCacheMiddleware' at the begin and 'rmr.extensions.middleware.json.RequestDecoder' at the end of the MIDDLEWARE_CLASSES of your settings file
