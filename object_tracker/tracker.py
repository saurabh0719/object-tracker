"""
Copyright (c) Saurabh Pujari
All rights reserved.

This source code is licensed under the BSD-style license found in the LICENSE file in the root directory of this source tree.
"""

from copy import deepcopy
from .exceptions import InitialStateMissingException
from .query_log import QueryLog


class Tracker:
    """

    The Tracker

    It maintains 2 lists - 
        -> log : the permanent store of log entries
        -> buffer : temporary memory to store state while filtering 

    """

    def __init__(self, **kwargs) -> None:
        self.log = QueryLog() # init query log
        self.observers = kwargs.get("observers", [])
        self.auto_notify = kwargs.get("auto_notify", True)
        self.ignore_init = kwargs.get("ignore_init", True)
        self.observable_attributes = kwargs.get("observable_attributes", [])
        self.attribute_observer_map = kwargs.get("attribute_observer_map", {})
        if kwargs.get("initial_state"):
            self.initial_state = deepcopy(kwargs.get("initial_state"))
        else:
            self.initial_state = None

    def __str__(self) -> str:
        return f"ObjectChangeLog -> BUFFER {self.log.buffer_len} LOG {self.log.log_len}"
    
    def __repr__(self) -> str:
        return str({'log': self.log.log_len, 'buffer': self.log.buffer_len})
    
    def __len__(self) -> int:
        return self.log.log_len

    def _call_observers(self, attr, old, new, observers: list):
        for observer in observers:
            observer(attr, old, new)

    def notify_observers(self, attr, old, new) -> None:
        """

        Notifies all observers 

        if self.auto_notify is False
        This method will have to be called manually

        """
        if self.attribute_observer_map:
            observers = self.attribute_observer_map.get(attr, [])
            self._call_observers(attr, old, new, observers)
            return
        
        if self.observers:
            if self.observable_attributes and attr not in self.observable_attributes:
                return 
            else:
                self._call_observers(attr, old, new, self.observers)

    @property
    def history(self):
        """
        Query the log by using tracker.history
        """
        return self.log

    def track_initial_state(self) -> None:
        """
        creates a deepcopy of the current object for faster 'has_changed' comparision later
        """
        self.initial_state = deepcopy(self)

    def print(self):
        """
        Utility std print fn
        """
        self.log.print()

    def attribute_changed(self, attr, obj=None) -> bool:
        """
        Checks if an attribute has changed by verifying against the log
        """

        if obj:
            if not self.initial_state:
                raise InitialStateMissingException()
            return getattr(self.initial_state, attr, None) != getattr(obj, attr, None)

        if self.initial_state:
            return getattr(self.initial_state, attr, None) != getattr(self, attr, None)

        first = None
        last = None

        for i in range(len(self.log.log)):
            if attr != self.log.log[i].attr:
                continue
            if not first:
                first = self.log.log[i]
                continue
            last = self.log.log[i]

        if not first:
            return False

        if first and not last:
            return True if first.old != first.new else False

        return first.old != last.new

    def changed(self, obj=None) -> bool:
        """
        Checks if any attribute of the object has been hanged by verifying against the log
        """

        if obj:
            if not self.initial_state:
                raise InitialStateMissingException()
            return obj.__dict__ != self.initial_state.__dict__
                
        if self.initial_state:
            return self.__dict__ != self.initial_state.__dict__

        seen = set()
        for entry in self.log.log:
            if entry.attr in seen:
                continue
            if self.attribute_changed(entry.attr):
                return True
            seen.add(entry.attr)
        return False
