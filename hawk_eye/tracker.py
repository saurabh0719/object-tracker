"""
Copyright (c) Saurabh Pujari
All rights reserved.

This source code is licensed under the BSD-style license found in the LICENSE file in the root directory of this source tree.
"""

from copy import deepcopy
import inspect
from .changelog import ObjectChangeLog    


class ObjectTracker:
    """
    A tracker to see if an object has changed 

    Usage : 

        def observer(attr, old, new):
            print(f"Observer : {attr} -> {old} - {new}")

        class User(ObjectTracker):
            def __init__(self, name) -> None:
                self._observers = [observer,]
                self.name = name


        user = User("A")
        print(user._has_changed()) # False

        user.name = "B"
        # Observer : name -> A - B

        print(user._has_changed()) # True
        
    """

    _observers = []
    _auto_notify = True
    _ignore_init = True
    _changelog = ObjectChangeLog()
    _observable_attributes = []
    _attribute_observer_map = {}
    _initial_state = None
    _tracker_attrs = [
        '_observers', 
        '_auto_notify', 
        '_changelog', 
        '_observable_attributes', 
        '_attribute_observer_map', 
        '_initial_state'
        '_tracker_attrs'
    ]

    def __setattr__(self, attr, value) -> None:
        """
        Overrides __setattr__ to track history and notify observers

        """
        curr = getattr(self, attr, value)
        super().__setattr__(attr, value)


        caller = inspect.currentframe().f_back.f_code.co_name
        # _ignore_init skips tracking for changes done in the init method
        # don't push to changelog and observers
        if '__init__' in caller and self._ignore_init:
            return

        self._changelog.push(
            attr=attr, 
            old=curr, 
            new=value
        )

        if self._auto_notify:
            self._notify_observers(attr, curr, value)

    def _call_observers(self, attr, old, new, observers: list):
        for observer in observers:
            observer(attr, old, new)

    def _notify_observers(self, attr, old, new):
        if self._attribute_observer_map:
            observers = self._attribute_observer_map.get(attr, [])
            self._call_observers(attr, old, new, observers)
            return
        
        if self._observers:
            if self._observable_attributes and attr not in self._observable_attributes:
                return 
            else:
                self._call_observers(attr, old, new, self._observers)

    def _has_attribute_changed(self, attr):
        """
        print(obj._has_attribute_changed('name'))
        """
        if self._initial_state:
            return getattr(self._initial_state, attr, None) != getattr(self, attr, None)
        return self._changelog.has_attribute_changed(attr)

    def _has_changed(self):
        """
        print(obj._has_changed('name'))
        """
        if self._initial_state:
            curr_dict = deepcopy(self.__dict__)
            curr_dict.pop('_initial_state')
            return curr_dict != self._initial_state.__dict__
        return self._changelog.has_changed()
    
    def _track_initial_state(self):
        self._initial_state = deepcopy(self)
