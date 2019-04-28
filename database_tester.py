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


    def test_get_user_is_admin(self):
        id = add_user("test")
        self.assertFalse(get_user_is_admin(id))
        delete_user_by_id(id)
        id = add_user("test", is_admin=False)
        self.assertFalse(get_user_is_admin(id))
        delete_user_by_id(id)
        id = add_user("test", is_admin=True)
        self.assertTrue(get_user_is_admin(id))
        delete_user_by_id(id)


    def test_add_flight(self):
        original_count = count_flights_by_gate("O")
        id = add_flight("2019-01-01 00:00:00", "2019-01-01 00:00:00", "O")
        final_count =  count_flights_by_gate("O")
        self.assertEqual(original_count+1, final_count)
        delete_flight_by_id(id)

    def test_get_id_by_flightid(self):
        id = add_flight("2019-01-01 00:00:00", "2019-01-01 00:00:00", "O")
        id2 = get_id_by_flightid(id)
        self.assertEqual(id, id2)
        delete_user_by_id(id)

    def test_delete_flight_by_id(self):
        id = add_flight("2019-01-01 00:00:00", "2019-01-01 00:00:00", "O")
        self.assertEqual(id,get_id_by_flightid(id))
        delete_flight_by_id(id)
        self.assertEqual(None,get_id_by_flightid(id))


    def test_add_aircraft(self):
        id = add_aircraft("test", "O")
        id2 = get_id_by_craftname("test")
        self.assertEqual(id, id2)
        print(id)
        delete_aircraft_by_id(id)


    def test_get_id_by_craftnamet(self):
        id1 = get_id_by_craftname("test")
        self.assertEqual(None, id1)
        id = add_aircraft("test", "O")
        id2 = get_id_by_craftname("test")
        self.assertEqual(id, id2)
        delete_aircraft_by_id(id)

    def test_delete_aircraft_by_id(self):
        id = add_aircraft("test", "O")
        self.assertEqual(id, get_id_by_craftname("test"))
        delete_aircraft_by_id(id)
        self.assertEqual(None, get_id_by_craftname("test"))



