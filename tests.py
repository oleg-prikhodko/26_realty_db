import unittest

from server import make_pages_list


class PaginationTestCase(unittest.TestCase):
    def test_pages_list(self):
        self.assertEqual(make_pages_list(1, 4), [1, 2, 3])
        self.assertEqual(make_pages_list(1, 3), [1, 2, 3])
        self.assertEqual(make_pages_list(1, 2), [1, 2])
        self.assertEqual(make_pages_list(1, 1), [1])
        self.assertEqual(make_pages_list(1, 0), [])
        self.assertEqual(make_pages_list(3, 3), [1, 2, 3])
        self.assertEqual(make_pages_list(2, 2), [1, 2])
        self.assertEqual(make_pages_list(2, 3), [1, 2, 3])
        self.assertEqual(make_pages_list(4, 7), [3, 4, 5])
