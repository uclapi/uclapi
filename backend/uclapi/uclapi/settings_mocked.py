# Patched settings file that allows mocking of database requests
from django_mock_queries.mocks import monkey_patch_test_db

from uclapi.settings import *


monkey_patch_test_db()
