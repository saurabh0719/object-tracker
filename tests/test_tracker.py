import unittest
from object_tracker import ObjectTracker


class User(ObjectTracker):
    def __init__(self, name, age) -> None:
        self.name = name
        self.age = age


class TestTracker(unittest.TestCase):
    def setUp(self):
        self.user = User("A", 100)
        self.user._changelog.flush()
        self.assertTrue(self.user._ignore_init)
        self.assertEqual(len(self.user._changelog), 0)

    def test_change(self):
        self.assertFalse(self.user._has_changed())
        self.user.name = "B"
        self.assertTrue(self.user._has_changed())

    def test_attribute_change(self):
        self.assertFalse(self.user._has_attribute_changed('name'))
        self.user.name = "B"
        self.assertTrue(self.user._has_attribute_changed('name'))
