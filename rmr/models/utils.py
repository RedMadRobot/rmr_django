import warnings

from rmr.utils.db import BulkModelCreator

warnings.warn(
    'BulkModelCreator moved to rmr.utils.db, make sure you import it from '
    'the new place before upgrading to rmr-django 2.0',
    category=RuntimeWarning, stacklevel=2,
)
