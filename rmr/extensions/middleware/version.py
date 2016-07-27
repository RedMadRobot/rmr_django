import warnings

from rmr.middleware.version import VersionMiddleware

warnings.warn(
    'VersionMiddleware moved to rmr.middleware.version, make sure '
    'you import it from the new place before upgrading to rmr-django 2.0',
    category=RuntimeWarning,
)
