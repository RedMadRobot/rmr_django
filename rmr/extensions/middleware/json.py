import warnings

from rmr.middleware.json import RequestDecoder

warnings.warn(
    'RequestDecoder moved to rmr.middleware.json, make sure you import it from '
    'the new place before upgrading to rmr-django 2.0',
    category=RuntimeWarning,
)
