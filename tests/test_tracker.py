import unittest
from object_tracker import ObjectTracker, Tracker, InitialStateMissingException

def observer(attr, old, new):
    return attr, old, new

# Demo object for testing
class User(ObjectTracker):
    def __init__(self, name, age) -> None:
        ObjectTracker.__init__(self, observers=[observer,])
        self.name = name
        self.age = age

class UntrackedUser:
    def __init__(self, name, age) -> None:
        self.name = name
        self.age = age


class TestTracker(unittest.TestCase):
    def setUp(self):
        pass

    def test_ops(self):
        user = User("A", 100)
        self.assertFalse(user.tracker.attribute_changed('name'))
        self.assertFalse(user.tracker.changed())
        user.name = "B"
        self.assertTrue(user.tracker.attribute_changed('name'))
        self.assertTrue(user.tracker.changed())
        user.tracker.history.flush()

    def test_query(self):
        user = User("A", 100)
        self.assertFalse(user.tracker.changed())
        user.name = "B"
        user.age = 20
        self.assertEqual(user.tracker.history.count(), 2)
        self.assertEqual(user.tracker.history.filter([]).count(), 2)
        self.assertEqual(user.tracker.history.filter().count(), 2)
        self.assertEqual(user.tracker.history.filter(['name',]).count(), 1)

        qs = user.tracker.history.exclude(['name',]).fetch()

        self.assertEqual(qs[0].attr, 'age')

        user.tracker.history.exclude(['name',]).flush()
        self.assertEqual(user.tracker.history.count(), 1)
        self.assertEqual(user.tracker.history.log[0].attr, 'name')

        user.tracker.history.flush()
        self.assertEqual(user.tracker.history.count(), 0)

    def test_tracker_only(self):
        user = UntrackedUser("A", 100)
        tracker = Tracker()
        self.assertEqual(tracker.initial_state, None)
        self.assertRaises(InitialStateMissingException, tracker.changed, user)
        tracker = Tracker(initial_state=user)
        self.assertFalse(tracker.changed(user))
        user.name = "B"
        self.assertTrue(tracker.changed(user))
        self.assertTrue(tracker.attribute_changed('name', user))


class TestObjectTracker(unittest.TestCase):
    def setUp(self):
        pass

    def test_change(self):
        user = User("A", 100)
        self.assertFalse(user.tracker.changed())
        user.name = "B"
        self.assertTrue(user.tracker.changed())

    def test_attribute_change(self):
        user = User("A", 100)
        self.assertFalse(user.tracker.attribute_changed('name'))
        user.name = "B"
        self.assertTrue(user.tracker.attribute_changed('name'))

    def test_defaults(self):
        user = User("A", 100)
        self.assertTrue(user.tracker.ignore_init)
        self.assertTrue(user.tracker.auto_notify)
        self.assertEqual(len(user.tracker.history), 0)

        user_2 = User("B", 50)
        assert user.name == "A"
        assert user_2.name == "B"
        assert user_2.age == 50

        self.assertEqual(len(user.tracker.observers), 1)
        assert callable(user.tracker.observers[0])

    def test_track_initial_state(self):
        user = User("A", 100)
        user.tracker.set_initial_state(user)
        self.assertFalse(user.tracker.changed())
        self.assertFalse(user.tracker.attribute_changed('name'))
        user.name = "B"
        self.assertTrue(user.tracker.changed())
        self.assertTrue(user.tracker.attribute_changed('name'))

    def test_ignore_init(self):
        user = User("A", 100)
        assert user.tracker.changed() is False
        user.name = "B"
        assert user.tracker.changed() is True
        user.tracker.history.flush()
        
        class Example:
            def __init__(self, name, age) -> None:
                self.user = User(name, age)
                assert self.user.tracker.changed() is False
                self.user.name = "B"
                assert self.user.tracker.changed() is True

        Example("A", 50)
