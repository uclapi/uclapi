# flake8: noqa
# Patched settings file that allows mocking of database requests
# The import * is important as it should mimic the entire settings
# file, with the only difference being the monkey-patched
# database access done nby the Django Mock Queries plugin.

from django_mock_queries.mocks import monkey_patch_test_db

from uclapi.settings import *

# https://stackoverflow.com/a/7004517
TEST_RUNNER = 'uclapi.custom_test_runner.NoDbTestRunner'

monkey_patch_test_db()
