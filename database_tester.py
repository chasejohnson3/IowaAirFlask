import unittest

from main import *


class TestDatabaseFunctions(unittest.TestCase):

    def test_add_user(self):

        test_name = "test_name"
        original_count = count_users_by_name(test_name)
        add_user(test_name)
        final_count = count_users_by_name(test_name)
        self.assertEqual(original_count+1, final_count)


    def test_check_password_by_email(self):
        test_email = "test_email"
        test_password = "test_password"
        add_user("test_name", email=test_email, password=test_password)
        # add_user("test_name")
        password_matches = check_password_by_email(test_email, test_password)
        self.assertTrue(password_matches)


    def test_get_usersid_by_username(self):
        test_name = "test_name1"
        expected_id = add_user(test_name)
        id = get_idusers_by_username(test_name)
        self.assertEqual(expected_id, id)
        #TODO: Fix this test