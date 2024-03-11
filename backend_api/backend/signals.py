from django.db.models.signals import post_migrate
from django.db import connection
from django.dispatch import receiver
from django.conf import settings
from django.db.utils import ProgrammingError


@receiver(post_migrate)
def create_database(sender, **kwargs):
    """
    Signal receiver function to create the database if it does not exist.
    """
    if 'default' in settings.DATABASES:
        database_config = settings.DATABASES['default']
        database_name = database_config['NAME']
        db_cursor = connection.cursor()
        try:
            db_cursor.execute("CREATE DATABASE IF NOT EXISTS {}".format(database_name))
        except ProgrammingError:
            # Handle exception if the database creation fails
            pass
