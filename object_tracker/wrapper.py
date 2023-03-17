"""
Copyright (c) Saurabh Pujari
All rights reserved.

This source code is licensed under the BSD-style license found in the LICENSE file in the root directory of this source tree.
"""

import inspect
from .tracker import Tracker 


class ObjectTracker:
    """
    A tracker to see if an object has changed 

    Internally uses a `self.tracker` variable of type `Tracker` 

    Usage : 

        def observer(attr, old, new):
            print(f"Observer : {attr} -> {old} - {new}")

        class User(ObjectTracker):
            def __init__(self, name) -> None:
                ObjectTracker.__init__(self, observers=[observer,])
                self.name = name


        user = User("A")
        print(user.tracker.changed()) # False

        user.name = "B"
        # Observer : name -> A - B

        print(user.tracker.changed()) # True
        
    """

    # Class variables of the tracker 
    # In the case where ObjectTracker's __init__ method is not called
    # The class variables will be used. This will only work with Singletons 
    # Otherwise there will be overwrites/loss of data due to a common changelog

    tracker = Tracker() # class static tracker

    def __init__(self, **kwargs) -> None:
        """
        Initialise all instance variables for the tracker
        """
        self.tracker = Tracker(**kwargs) # Instance tracker


    def __setattr__(self, attr, value) -> None:
        """

        Overrides __setattr__ to track history and notify observers

        CPython implementation detail: 
    
        https://docs.python.org/3/library/inspect.html#inspect.currentframe
        
        "This function relies on Python stack frame support in the interpreter, 
        which isn’t guaranteed to exist in all implementations of Python. 
        If running in an implementation without Python stack frame support this function returns None."

        In that case, it is pushed to changelog and observers are notified anyways.

        """
        curr = getattr(self, attr, value)
        super().__setattr__(attr, value)

        # get previous frame
        caller_frame = inspect.currentframe().f_back
        if caller_frame:
            caller_fn = caller_frame.f_code.co_name
            if (
                caller_frame.f_locals['self'].__class__ == self.__class__
                and '__init__' in caller_fn
                and self.tracker.ignore_init
            ):
                # Ignore changes made in the __init__ fn of the same class if self._ignore_init
                return

        # push log entry
        self.tracker.log.push(
            attr=attr, 
            old=curr, 
            new=value
        )

        # notify all observers
        if self.tracker.auto_notify:
            self.tracker.notify_observers(attr, curr, value)

        return
