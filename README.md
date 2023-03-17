<div align="center">
    <img src="https://content-dump-3.s3.ap-south-1.amazonaws.com/saurabh/hawkeye.png" width ="75%">
</div>

<div align="center">
    <h1>Object Tracker</h1>
</div>

<br>

A pure python object change &amp; history tracker. Monitor all changes in your object's lifecycle and trigger callback functions to capture them. :pencil:

```sh
$ pip install object-tracker
```

<div align="center">
    <strong><a href="https://github.com/saurabh0719/object-tracker">Github</a> | <a href="https://saurabh0719.github.io">Website</a> | <a href="https://github.com/saurabh0719/object-tracker/releases">Release notes</a> </strong>
</div>

Tested for python `3.7` and above.

<span id="features"></span>
## Key Features

-  Determine if a python object has changed during it's lifecycle.
-  Investigate change history through the structured changelog.
-  Trigger callback functions whenever an attribute has changed.
-  Simple and structured API. 
-  Queryable change history log. 


<hr>

<span id="contents"></span>
## Table of Contents :
* [Key Features](#features)
* [Basic Usage](#usage)   
* [Getting Started](#guide)
    * [How does it work?](#how)
       * [class ObjectTracker](#objecttracker)
       * [class Tracker](#tracker)
* [Tracker API](#trackerapi)
    * [Configuration](#config)
    * [Track object change](#change)
    * [History](#history)
    * [Querying change history](#query)
    * [Adding observers](#observers)
    * [Using a standalone Tracker instance ie. No inheritance](#lonetracker)
* [Tests](#tests)
* [Release notes](#releases)
* [License](#license) 


<span id="usage"></span>
## Basic Usage 

Inherit the `ObjectTracker` class to create a trackable object.

```python

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

```

To use the tracker without inheriting - [read this guide](#lonetracker)

<span id="guide"></span>
## Getting Started

The `ObjectTracker` class implements `__setattr__` and tracks change history. Any object that needs to be tracked must inherit `ObjectTracker`.

[Go back to the table of contents](#contents)

<span id="help"></span>
### How does it work?

The **object_tracker** module consists of 2 major classes - 

#### class `ObjectTracker` 

An inheritable class that implements the `__setattr__` methods and reports changes to the `Tracker` class that's initialised inside it.

```python 
from object_tracker import ObjectTracker

class TrackerObject(ObjectTracker):
    def __init__(self, name) -> None:
        ObjectTracker.__init__(self)
        pass
```
- It adds a `tracker` attribute to the subclass and can be accessed by `self.tracker`.

- Don't forget to initialise call it's `__init__` . You can define various parameters, see [the configuration guide](#config)
 
- See further implementation details in `object_tracker/wrapper.py`.


#### class `Tracker` 

This object is initialised inside the `ObjectTracker` and does all the heavylifting ie. storing change history and checking if any change has occured. Can be accessed through the `tracker` attribute when inheriting `ObjectTracker`. 

**Note** - The  `**kwargs` passed to `ObjectTracker` are passed down to the `Tracker` instance to initialise it. 

```python

class User(ObjectTracker):
    def __init__(self, name) -> None:
        ObjectTracker.__init__(self, observers=[observer,])
        self.name = name

user = User("A")
user.name = "B" # o
print(user.tracker.changed()) 

```

- See further implementation details in `object_tracker/tracker.py`.

[Go back to the table of contents](#contents)

<hr>


<span id="trackerapi"></span>
## Tracker API

When an object has inherited `ObjectTracker`, it is now a trackable object. You can access the `Tracker` instance by using the `self.tracker` attribute of your trackable object. 

You can also use a standalone instance of `Tracker`, with some caveats - [read more here](#lonetracker)

<span id="config"></span>
### Configuration 

There are a bunch of config variables that can be modified when inheriting the `ObjectTracker` class:

**Note** - The  `**kwargs` passed to `ObjectTracker` are passed down to the `Tracker` instance to initialise it. 

-  `auto_notify` - default `True` - Autmatically notifies observers everytime an attribute is set. Can be set to `False` and called manually using `notify_observers(self, attr, old, new)`

- `ignore_init` - default `True` - Ignore changes made from `__init__` functions. These will not be pushed to the changelog or be notified. 

- `log` -> An instance of `QueryLog`, stores a structured log and exposes a query interface to object history. [Read more about it here](#history)

- `observers, observable_attributes, attribute_observer_map` -> Read more about [adding observers](#observers)

```python

from object_tracker import ObjectTracker

def observer(attr, old, new):
    print(f"Observer : {attr} -> {old} - {new}")

class User(ObjectTracker):
    def __init__(self, name) -> None:
        ObjectTracker.__init__(self, observers=[observer,], auto_notify=False)
        self.name = name

```

<br>

[Go back to the table of contents](#contents)

<span id="change"></span>
### Track object change

`changed(obj=None)` checks if _any_ attribute has changed, whereas `tracker.attribute_changed(attr, obj=None)` checks if a single attribute has changed. The `obj` argument is only needed when using a standalone instance of `Tracker` instead of inheriting `ObjectTracker`, [read more here](#lonetracker)


```python

user = User("A")
print(user.tracker.changed()) 
# False

user.name = "B" 

print(user.tracker.changed()) 
# True

print(user.tracker.attribute_changed('name'))
# True

print(user.tracker.attribute_changed('age'))
# False

```


[Go back to the table of contents](#contents)

<span id="history"></span>
### History

Each `Tracker` object has a structured change history log - `self.log` - for all the attributes, an instance of `QueryLog`.

The `QueryLog` object maintains 2 lists, a `log` of every change and a query `buffer` for temporary storage while [querying](#query)

Both lists carry instances of `Entry`, a structured log record containing 

- `attr` - String representation of the attribute that was modified

- `old` - Old value of the attribute

- `new` - New value of the attribute

- `timestamp` - An instance of `datetime.datetime` 

Every change is implicitly pushed - `push(attr, old, new)` - to the `QueryLog` instance. 

The log/history instance can be accessed by `self.history` or `self.log` 

```python

user = User("A")
user.name = "B" 

user.tracker.print()
user.tracker.history.print() 

history = user.tracker.history.fetch()
print(history) 

```

[Go back to the table of contents](#contents)


<span id="query"></span>
### Querying change history

The `QueryLog` class offers a simple query interface to filter logs - 

Terminal methods (do not chain ie. `return self`) - 

- `fetch(self)` - returns the current query buffer

- `flush(self)` - Flushes the entire query buffer

- `count(self)` - Counts the number of log entries 

Chaned methods (`return self`) -

- `filter(self, attrs)` - Accepts an optional attribute string OR list of attribute strings, and filters out their logs.

- `exclude(self, atrrs)` - Accepts an optional attribute string OR list of attribute strings, and excludes their logs from the query buffer

The `QueryLog` instance can be accessed by `tracker.history` or `tracker.log`

```python 

class User(ObjectTracker):
    def __init__(self, name, age) -> None:
        super().__init__()
        self.name = name
        self.age = age

user = User("A", 20)
user.name = "B" 
user.age = 50

user.tracker.history.print()
# [{'attr': 'name', 'old': 'A', 'new': 'B', 'timestamp': datetime.datetime(2023, 3, 15, 15, 4, 52, 583628)}, {'attr': 'age', 'old': 20, 'new': 50, 'timestamp': datetime.datetime(2023, 3, 15, 15, 4, 52, 583665)}]

print(user.tracker.history.count())
# 2

name_history = user.tracker.history.filter('name').fetch()
print(name_history)
# [{'attr': 'name', 'old': 'A', 'new': 'B', 'timestamp': datetime.datetime(2023, 3, 15, 15, 4, 52, 583628)}]

print(user.tracker.history.filter('name').count()) 
# 1

print(user.tracker.history.exclude('name').count())
# 1

user.tracker.history.filter('age').flush()

print(user.tracker.history.count())
# 1

user.tracker.history.flush()

print(user.tracker.history.count())
# 0

```

[Go back to the table of contents](#contents)


<span id="observers"></span>
### Adding observers

Observer fn signature - 

```python
def observer(attr, old, new)
```

You can set observer functions that will be triggered whenever a change takes place for an attribute 

```python

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

```

`attribute_observer_map` - default `{}` - This is a dictionary of attribute strings mapped to a `list of observer functions` that will be called whenever a change takes place on that specific attribute.

**Note** - The  `**kwargs` passed to `ObjectTracker` are passed down to the `Tracker` instance to initialise it. 

```python

def observer_a(attr, old, new):
    print(f"Observer A: {attr} -> {old} - {new}")

def observer_b(attr, old, new):
    print(f"Observer B: {attr} -> {old} - {new}")

class User(ObjectTracker):
    def __init__(self, name) -> None:
        attribute_observer_map = {
            'name': [observer_a, observer_b], 
            'age': [observer_a,]
        }
        ObjectTracker.__init__(self,attribute_observer_map=attribute_observer_map)
        self.name = name
        self.age

```

When `attribute_observer_map` is empty, then the `observers` list (default `[]`) is used. 


```python

def observer_a(attr, old, new):
    print(f"Observer A: {attr} -> {old} - {new}")

def observer_b(attr, old, new):
    print(f"Observer B: {attr} -> {old} - {new}")

class User(ObjectTracker):
    def __init__(self, name) -> None:
        ObjectTracker.__init__(self, observers=[observer_a, observer_b])
        self.name = name

```

- You can set a list of `observable attributes` (default `[]`), and the `observers` will only be called when there is a change in one of those attributes. 


```python

from object_tracker import ObjectTracker

def observer(attr, old, new):
    print(f"Observer : {attr} -> {old} - {new}")

class User(ObjectTracker):
    def __init__(self, name) -> None:
        ObjectTracker.__init__(self, observers=[observer,], observable_attributes=['name',])
        self.name = name
        self.age = age

```

[Go back to the table of contents](#contents)


<span id="lonetracker"></span>
## Using a standalone Tracker instance ie. No inheritance

It is possible to use a standalone instance of the `Tracker` class, by setting a special `initial_state` attribute. Eg - 

```python

from object_tracker import Tracker

class UntrackedUser:
    def __init__(self, name, age) -> None:
        self.name = name
        self.age = age

user = UntrackedUser("A", 100)
tracker = Tracker(initial_state=user)

print(tracker.changed(user))
# False

user.name = "B"

print(tracker.changed(user))
# True

```

#### Caveats - 

- `changed(obj=None)` AND `attribute_changed(obj=None)` have to be called with an object passed as argument. Otherwise you will get False results.

- The `Tracker` object has to contain the `initial_state` of the object you intend to track, otherwise calling `changed(obj)` or `attribute_changed(obj)` will raise a `InitialStateMissingException` 

- The standalone instance DOES NOT use the `QueryLog` object, hence the change tracker fully depends on the difference of initial_state and the current object's `__dict__` representation. Hence there is no history to query ie. It will be empty always. 

[Go back to the table of contents](#contents)

<hr>

<span id="tests"></span>
## Tests 

Run this command inside the base directory to execute all tests inside the `tests` folder:

```sh
$ python -m unittest -v
```

[Go back to the table of contents](#contents)

<hr>

<span id="releases"></span>
## Release notes 

* Latest - `v1.0.0` 

View object-tracker's detailed [release history](https://github.com/saurabh0719/object-tracker/releases/).

[Go back to the table of contents](#contents)

<hr>

<span id="license"></span>
## License

```
Copyright (c) Saurabh Pujari
All rights reserved.

This source code is licensed under the BSD-style license found in the LICENSE file in the root directory of this source tree.
```

[Go back to the table of contents](#contents)
