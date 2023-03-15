<div align="center">
    <img src="./assets/hawkeye.png" width ="75%">
    
## hawkeye :eagle:
</div align="center">
<br>

A pure python object change &amp; history tracker. Monitor all changes in your objects lifecycle and trigger callback functions to capture them. :pencil:

```sh
$ pip install hawk-eye
```

Tested for python `3.7` and above.

### Key Features

-  Determine if a python object has changed.
-  Investigate change history through the changelog.
-  Trigger callback functions whenever the object or an attribute has changed.
-  Simple query interface for object changelog. 


### Usage 

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


### License

```
Copyright (c) Saurabh Pujari
All rights reserved.

This source code is licensed under the BSD-style license found in the LICENSE file in the root directory of this source tree.
```

<hr>
