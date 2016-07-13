Changelog
=========

Release 1.0.31
--------------

- Enhancement: Added :code:`rmr.extensions.middleware.version.VersionMiddleware` function

Release 1.0.30
--------------

- Enhancement: Added :code:`rmr.utils.db.dictfetchall` function

Release 1.0.29
--------------

- Enhancement: Added :code:`rmr.utils.datetime.get_date_range` function

Release 1.0.28
--------------

- Enhancement: Added :code:`rmr.models.fields.PgLtreeField` supporting PostgreSQL's ltree extension

Release 1.0.27
--------------

- Fix: MultipleValueField now can be used with values containing lists
- Enhancement: :code:`rmr.extensions.middleware.json.RequestDecoder` now can parse any JSON (not only objects)

Release 1.0.26
--------------

- Enhancement: Added :code:`rmr.views.decorators.auth.authentication_required()` views decorator

Release 1.0.25
--------------

- Enhancement: Added cache invalidation after :code:`rmr.views.Json.last_modified()` value has been changed
- Enhancement: Added 'Last-Modified', 'Cache-Control' and 'Expires' headers to the HTTP responses with 304 status code

Release 1.0.24
--------------

- Enhancement: Added :code:`rmr.extensions.middleware.cache.FixCacheControlMaxAge`
- Enhancement: Added :code:`rmr.models.utils.BulkModelCreator`

Release 1.0.23
--------------

- Enhancement: Added :code:`rmr.utils.iterate.consume()`
- Enhancement: Added base :code:`rmr.forms.OffsetLimit` validation form
- Fix: :code:`Json.get_range()` raises an error when set 'limit_max' and 'limit' is not provided

Release 1.0.22
--------------

- Enhancement: Added 'request' instance property to the :code:`rmr.views.Json`
- Enhancement: :code:`rmr.views.decorators.validate.validate_request()` replaces request's GET and POST by validated ones

Release 1.0.21
--------------

- Enhancement: Added HTTP-caching headers management to the :code:`rmr.views.Json`
- Enhancement: Moved :code:`validate_request` decorator to :code:`rmr.views.decorators.validation` module
- Enhancement: Removed :code:`rmr.views.Json.get_device_id()` method

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
