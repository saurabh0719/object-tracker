import unittest
from object_tracker import ObjectTracker

# Demo object for testing
class User(ObjectTracker):
    def __init__(self, name, age) -> None:
        self.name = name
        self.age = age


class TestChangeLog(unittest.TestCase):
    def setUp(self):
        pass

    def test_ops(self):
        user = User("A", 100)
        self.assertFalse(user._changelog.has_attribute_changed('name'))
        self.assertFalse(user._changelog.has_changed())
        user.name = "B"
        self.assertTrue(user._changelog.has_attribute_changed('name'))
        self.assertTrue(user._changelog.has_changed())
        user._changelog.flush()

    def test_query(self):
        user = User("A", 100)
        self.assertFalse(user._changelog.has_changed())
        user.name = "B"
        user.age = 20
        self.assertEqual(user._changelog.count(), 2)
        self.assertEqual(user._changelog.filter([]).count(), 2)
        self.assertEqual(user._changelog.filter().count(), 2)
        self.assertEqual(user._changelog.filter(['name',]).count(), 1)

        qs = user._changelog.exclude(['name',]).fetch()

        self.assertEqual(qs[0].attr, 'age')

        user._changelog.exclude(['name',]).flush()
        self.assertEqual(user._changelog.count(), 1)
        self.assertEqual(user._changelog.log[0].attr, 'name')

        user._changelog.flush()
        self.assertEqual(user._changelog.count(), 0)


class TestTracker(unittest.TestCase):
    def setUp(self):
        pass

    def test_change(self):
        user = User("A", 100)
        self.assertFalse(user._has_changed())
        user.name = "B"
        self.assertTrue(user._has_changed())
        user._changelog.flush()

    def test_attribute_change(self):
        user = User("A", 100)
        self.assertFalse(user._has_attribute_changed('name'))
        user.name = "B"
        self.assertTrue(user._has_attribute_changed('name'))
        user._changelog.flush()

    def test_defaults(self):
        user = User("A", 100)
        self.assertTrue(user._ignore_init)
        self.assertTrue(user._auto_notify)
        self.assertEqual(len(user._changelog), 0)
        user._changelog.flush()

        user_2 = User("B", 50)
        assert user.name == "A"
        assert user_2.name == "B"
        assert user_2.age == 50

    def test_ignore_init(self):
        user = User("A", 100)
        assert user._has_changed() is False
        user.name = "B"
        assert user._has_changed() is True
        user._changelog.flush()
        
        class Example:
            def __init__(self, name, age) -> None:
                self.user = User(name, age)
                assert self.user._has_changed() is False
                self.user.name = "B"
                assert self.user._has_changed() is True

        Example("A", 50)
