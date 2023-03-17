object-tracker
--------------

A pure python object change and history tracker. Monitor all changes in your objects lifecycle and trigger callback functions to capture them.

View the `Github repository <https://github.com/saurabh0719/object-tracker>`__ and the `official docs <https://github.com/saurabh0719/object-tracker#README>`__.

.. code:: sh

    $ pip install object-tracker

Tested for python 3.6, 3.7 and above.

Key Features
------------

-  Determine if a python object has changed.
-  Investigate change history through the changelog.
-  Trigger callback functions whenever the object or an attribute has changed.
-  Simple and structured API. 
-  Queryable change history log.

License
-------

::

    Copyright (c) Saurabh Pujari
    All rights reserved.

    This source code is licensed under the BSD-style license found in the LICENSE file in the root directory of this source tree.


Usage :
~~~~~~~~~~~~~

.. code:: python

   from object_tracker import ObjectTracker

    def observer(attr, old, new):
        print(f"Observer : {attr} -> {old} - {new}")

    class User(ObjectTracker):
        def __init__(self, name) -> None:
            ObjectTracker.__init__(self, observers=[observer,])
            self.name = name


    user = User("A")
    print(user.tracker.changed()) 
    # False

    user.name = "B" # observers will be triggered
    # Observer : name -> A - B

    print(user.tracker.changed()) 
    # True
