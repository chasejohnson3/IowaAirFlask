import unittest

from main import *


class TestDatabaseFunctions(unittest.TestCase):

    def test_add_user(self):
        test_name = "test_name"
        test_email = "test_email"
        original_count = count_users_by_name(test_name)
        id = add_user(test_email, first_name=test_name)
        final_count = count_users_by_name(test_name)
        self.assertEqual(original_count+1, final_count)
        delete_user_by_id(id)

    def test_check_password_by_email(self):
        test_email = "test_email"
        test_password = "test_password"
        id = add_user(test_email, first_name="test_name", password=test_password)
        # add_user("test_name")
        password_matches = check_password_by_email(test_email, test_password)
        self.assertTrue(password_matches)
        delete_user_by_id(id)

    def test_get_usersid_by_email(self):
        test_email = "test_email1"
        expected_id = add_user(email=test_email)
        id = get_idusers_by_email(test_email)
        self.assertEqual(expected_id, id)
        delete_user_by_id(id)

    def test_check_if_id_exists(self):
        id = add_user("test")
        print("id from add_user: " + str(id))
        self.assertTrue(check_if_id_exists(id))
        self.assertFalse(check_if_id_exists("nonsense"))
        delete_user_by_id(id)

    def test_delete_user_by_id(self):
        id = add_user("test")
        self.assertTrue(check_if_id_exists(id))
        delete_user_by_id(id)
        self.assertFalse(check_if_id_exists(id))

    def test_get_first_name_by_id(self):
        expected_test_name = "test_name"
        id = add_user("test", first_name=expected_test_name)
        actual_first_name = get_first_name_by_id(id)
        self.assertEqual(expected_test_name, actual_first_name)
        delete_user_by_id(id)

