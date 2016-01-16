Changelog
=========

Release 1.0.21
--------------

- Enhancement: Added :code:`rmr.utils.cache.CacheTimeout`, lazy value for :code:`django.views.decorators.cache.cache_page` decorator
- Enhancement: Added custom cache backend :code:`rmr.utils.cache.RmrLibMCCache` which enables to use :code:`rmr.utils.cache.CacheTimeout` decorator

Release 1.0.20
--------------

- Enhancement: Added :code:`rmr.utils.iterate.multimap()`
- Enhancement: Added decorator :code:`rmr.views.validate_request()`
- Enhancement: Added custom form fields :code:`rmr.forms.MultiValueField` and :code:`rmr.forms.BooleanField` for JSON form validation purpose

Release 1.0.19
--------------

- Enhancement: Added :code:`rmr.utils.datetime.fromtimestamp()` and :code:`rmr.utils.datetime.strptime()`
- Enhancement: Removed :code:`rmr.utils.test.mocked_datetime()`

Release 1.0.18
--------------

- Enhancement: Removed decorators :code:`anonymous_required` and :code:`login_required`

Release 1.0.17
--------------

- Enhancement: Added custom PostgreSQL range fields with :code:`upper` and :code:`lower` lookups
- Enhancement: Added :code:`rmr.management.commands.BaseCommand` class

Release 1.0.16
--------------

- Enhancement: Added :code:`rmr.utils.hash.crc32()` and :code:`rmr.utils.hash.crc64()` functions
- Enhancement: Added :code:`rmr.utils.iterate.split_every()` and :code:`rmr.utils.iterate.unique()` functions

Release 1.0.15
--------------

- Enhancement: Added :code:`rmr.views.Json.get_range()` method

Release 1.0.14
--------------

- Enhancement: Added :code:`rmr.models.fields.PgTrigramTextField` and :code:`rmr.models.fields.PgTrigramCharField` supporting PostgreSQL's pg_trgm extension
