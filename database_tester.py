import unittest

from main import *


class TestDatabaseFunctions(unittest.TestCase):

    def test_add_user(self):
        test_name = "test_name"
        original_count = count_users_by_name(test_name)
        add_user(test_name)
        final_count = count_users_by_name(test_name)
        self.assertEqual(original_count+1, final_count)
