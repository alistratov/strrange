import unittest
import os


loading_tests_enabled = unittest.skipIf(
    not os.environ.get('LOADING_TESTS_ENABLED', False), 'Skip loading tests',
)
