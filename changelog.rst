Changelog
=========

Release 1.0.19
--------------

- Enhancement: Added fixed version of 'Europe/Moscow' timezone
- Enhancement: Added 'CEST' timezone

Release 1.0.18
--------------

- Enhancement: Removed unnecessary decorators :code:`anonymous_required` and :code:`login_required`

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
