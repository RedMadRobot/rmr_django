import logging

from django.core.management.base import BaseCommand as DjangoBaseCommand


class BaseCommand(DjangoBaseCommand):
    """Django command implementation with predefined logging setup

    Use logging.info(), logging.debug() and other logging methods to
    print log messages
    """

    @property
    def logger_name(self):
        return self.__class__.__module__.rsplit('.', 1)[-1]

    @staticmethod
    def get_logger_level(verbosity):
        if verbosity == 1:
            return logging.INFO
        if verbosity == 0:
            return logging.WARNING
        return logging.DEBUG

    def execute(self, *args, **options):
        logging.basicConfig(
            level=self.get_logger_level(options.get('verbosity')),
            format='%(asctime)s [%(levelname)s] ({logger}) %(message)s'.format(
                logger=self.logger_name,
            ),
            datefmt='%Y-%m-%d %H:%M:%S',
        )
        return super().execute(*args, **options)
