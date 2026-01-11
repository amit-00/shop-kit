# """
# Pytest configuration for Django tests.
# """
# import pytest


# @pytest.fixture(scope='session', autouse=True)
# def django_db_modify_db_settings():
#     """
#     Override database settings to use SQLite for tests.
#     This is the pytest-django recommended way to modify database settings.
    
#     pytest-django will automatically call this fixture to modify database
#     settings before creating the test database.
#     """
#     from django.conf import settings
    
#     # Override database settings for tests
#     settings.DATABASES['default'] = {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': ':memory:',
#         'ATOMIC_REQUESTS': False,
#     }
    
#     # Override cache settings to use dummy cache for tests
#     # This avoids requiring a running Redis server
#     settings.CACHES = {
#         'default': {
#             'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
#         }
#     }

