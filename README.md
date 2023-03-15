<div align="center">
    <img src="./assets/hawkeye.png" width ="75%">
    
# hawkeye :eagle:
</div align="center">
<br>

A pure python object change &amp; history tracker. Monitor all changes in your objects lifecycle and trigger callback functions to capture them. :pencil:

```sh
$ pip install hawk-eye
```

Tested for python `3.7` and above.

<span id="features"></span>
## Key Features

-  Determine if a python object has changed.
-  Investigate change history through the structured changelog.
-  Trigger callback functions whenever the object or an attribute has changed.
-  Simple query interface for object changelog. 


<hr>

<span id="contents"></span>
## Table of Contents :
* [Key Features](#features)
* [Basic Usage](#usage)   
* [Guide](#guide)
    * [Configuration](#config)
    * [Track object change](#change)
    * [Changelog](#changelog)
    * [Querying changelog](#query)
    * [Adding observers](#observers)
* [Tests](#tests)
* [Release notes](#releases)
* [License](#license) 

<br>

<span id="usage"></span>
## Basic Usage 

```python

from hawk_eye import ObjectTracker

def observer(attr, old, new):
    print(f"Observer : {attr} -> {old} - {new}")

class User(ObjectTracker):
    def __init__(self, name) -> None:
        self._observers = [observer,]
        self.name = name


user = User("A")
print(user._has_changed()) 
# False

user.name = "B" # observers will be triggered
# Observer : name -> A - B

print(user._has_changed()) 
# True

```

<span id="guide"></span>
## Guide 

Hawkeye uses an `underscore _` before method and attribute names, to prevent being overriden. 

[Go back to the table of contents](#contents)


<span id="config"></span>
### Configuration 

There are a bunch of config variables that can be modified when inheriting the `ObjectTracker` class:

-  `_auto_notify = True` -> Autmatically notifies observers everytime an attribute is set. Can be set to `False` and called manually using `_notify_observers(self, attr, old, new)`

- `_ignore_init = True` -> Ignore changes made from `__init__` functions. These will not be pushed to the changelog or be notified. 

- `_changelog` -> An instance of `ObjectChangeLog`, stores a structured log and exposes a query interface to object history. 

- `_observers, _observable_attributes, _attribute_observer_map` -> Read more about [adding observers](#observers)

```python

from hawk_eye import ObjectTracker

def observer(attr, old, new):
    print(f"Observer : {attr} -> {old} - {new}")

class User(ObjectTracker):
    def __init__(self, name) -> None:
        self._observers = [observer,]
        self._auto_notify = False
        self.name = name

```

<br>

[Go back to the table of contents](#contents)

<span id="change"></span>
### Track object change

`_has_changed()` checks if _any_ attribute has changed, whereas `_has_attribute_changed(attr)` checks if a single attribute has changed.


```python

user = User("A")
print(user._has_changed()) 
# False

user.name = "B" 

print(user._has_changed()) 
# True

print(user._has_attribute_changed('name'))
# True

print(user._has_attribute_changed('age'))
# False

```

use `_track_initial_state()` to create a deepcopy of the current object for faster `has_changed` comparision later 

```python

user = User("A")
user._track_initial_state()

```

[Go back to the table of contents](#contents)

<span id="changelog"></span>
### Changelog 

Each trackable object has a structured changelog - `self._changelog` - for all the attributes, an instance of `ObjectChangeLog`.

It maintains 2 lists, a `log` of every change and a query `buffer` for temporary storage while [querying](#query)

Both lists carry instances of `LogEntry`, a structured log record containing 

- `attr` - String representation of the attribute that was modified

- `old` - Old value of the attribute

- `new` - New value of the attribute

- `timestamp` - An instance of `datetime.datetime` 

Every change is implicitly pushed - `push(attr, old, new)` - to the `_changelog` 

```python

user = User("A")
user.name = "B" 

user_.changelog.print()

history = user_.changelog.fetch()
print(history) 

```

[Go back to the table of contents](#contents)


<span id="query"></span>
### Querying the changelog 

The `ObjectChangeLog` class offers a simple query interface to filter logs - 

Terminal methods (do not chain ie. `return self`) - 

- `fetch(self)` - returns the current query buffer

- `flush(self)` - Flushes the entire query buffer

- `count(self)` - Counts the number of log entries 

Chaned methods (`return self`) -

- `filter(self, attrs)` - Accepts an optional attribute string OR list of attribute strings, and filters out their logs.

- `exclude(self, atrrs)` - Accepts an optional attribute string OR list of attribute strings, and excludes their logs from the query buffer

The changelog also offers the `has_changed(self)` and `has_attribute_changed(self, attr)` methods that check if there was a change by resolving the change log for each attribute

```python 

class User(ObjectTracker):
    def __init__(self, name, age) -> None:
        self.name = name
        self.age = age

user = User("A", 20)
user.name = "B" 
user.age = 50

user._changelog.print()
# [{'attr': 'name', 'old': 'A', 'new': 'B', 'timestamp': datetime.datetime(2023, 3, 15, 15, 4, 52, 583628)}, {'attr': 'age', 'old': 20, 'new': 50, 'timestamp': datetime.datetime(2023, 3, 15, 15, 4, 52, 583665)}]

print(user._changelog.count())
# 2

name_history = user._changelog.filter('name').fetch()
print(name_history)
# [{'attr': 'name', 'old': 'A', 'new': 'B', 'timestamp': datetime.datetime(2023, 3, 15, 15, 4, 52, 583628)}]

print(user._changelog.filter('name').count()) 
# 1

print(user._changelog.exclude('name').count())
# 1

user._changelog.filter('age').flush()

print(user._changelog.count())
# 1

user._changelog.flush()

print(user._changelog.count())
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

from hawk_eye import ObjectTracker

def observer(attr, old, new):
    print(f"Observer : {attr} -> {old} - {new}")

class User(ObjectTracker):
    def __init__(self, name) -> None:
        self._observers = [observer,]
        self.name = name


user = User("A")
print(user._has_changed()) 
# False

user.name = "B" # observers will be triggered
# Observer : name -> A - B

print(user._has_changed()) 
# True

```

`_attribute_observer_map = {}` -> This is a dictionary of attribute strings mapped to a `list of observer functions` that will be called whenever a change takes place on that specific attribute. 

```python

def observer_a(attr, old, new):
    print(f"Observer A: {attr} -> {old} - {new}")

def observer_b(attr, old, new):
    print(f"Observer B: {attr} -> {old} - {new}")

class User(ObjectTracker):
    def __init__(self, name) -> None:
        self._attribute_observer_map = {
            'name': [observer_a, observer_b], 
            'age': [observer_a,]
        }
        self.name = name
        self.age

```

When `_attribute_observer_map` is empty, then the `_observers` list is used. 


```python

def observer_a(attr, old, new):
    print(f"Observer A: {attr} -> {old} - {new}")

def observer_b(attr, old, new):
    print(f"Observer B: {attr} -> {old} - {new}")

class User(ObjectTracker):
    def __init__(self, name) -> None:
        self._observers = [observer_a, observer_b],
        self.name = name

```

- You can set a list of `_observable attributes`, and the `_observers` will only be called when there is a change in one of these attributes. 


```python

from hawk_eye import ObjectTracker

def observer(attr, old, new):
    print(f"Observer : {attr} -> {old} - {new}")

class User(ObjectTracker):
    def __init__(self, name) -> None:
        self._observers = [observer,]
        self._observable_attributes = ['name',]
        self.name = name
        self.age = age

```

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

* Latest - `v0.1.0` 

View Hawkeye's detailed [release history](https://github.com/saurabh0719/hawkeye/releases/).

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

<hr>
