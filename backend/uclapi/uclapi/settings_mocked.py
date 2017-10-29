# flake8: noqa
# Patched settings file that allows mocking of database requests
# The import * is important as it should mimic the entire settings
# file, with the only difference being the monkey-patched
# database access done nby the Django Mock Queries plugin.

from django_mock_queries.mocks import monkey_patch_test_db

from uclapi.settings import *


monkey_patch_test_db()
