"""
Copyright (c) Saurabh Pujari
All rights reserved.

This source code is licensed under the BSD-style license found in the LICENSE file in the root directory of this source tree.
"""

from .entry import LogEntry


class ObjectChangeLog:
    """
    The Change log

    It maintains 2 lists - 
        -> log : the permanent store of log entries
        -> buffer : temporary memory to store state while filtering 
    """

    def __init__(self) -> None:
        self.log = []
        self.buffer = []

    def __str__(self) -> str:
        return f"ObjectChangeLog -> BUFFER {len(self.buffer)} LOG {len(self.log)}"
    
    def __repr__(self) -> str:
        return str({'log': len(self.log), 'buffer': len(self.buffer)})
    
    def __len__(self) -> int:
        return len(self.log)

    def _process_filter(self, attrs, exclude=False):
        """
        Processes filter attrs and saves it in the buffer

        - exclude = True for exluding attrs
        """
        _attrs = None
        if attrs:
            if isinstance(attrs, list):
                _attrs = attrs

            elif isinstance(attrs, str):
                _attrs = [attrs,]

        # innner
        def _filter(entry: LogEntry):
            return entry.attr in _attrs if _attrs else True

        if exclude:
            self.buffer = list(filter(lambda x: not _filter(x), self.log))
        else:
            self.buffer = list(filter(lambda x: _filter(x), self.log))

        return self

    def filter(self, attrs=None):
        """
        obj.filter(['name',]).fetch()
        """
        return self._process_filter(attrs)
    
    def exclude(self, attrs=None):
        """
        obj.exclude(['name',]).fetch()
        """
        return self._process_filter(attrs, True)
    
    def fetch(self) -> list:
        return self.buffer or self.log

    def flush(self) -> None:
        if self.buffer:
            for item in self.buffer:
                self.log.remove(item)
        else:
            self.log = []
            
        self.buffer = []

    def count(self) -> None:
        return len(self.buffer) if self.buffer else len(self.log)

    def push(self, attr, old, new) -> None:
        self.log.append(
            LogEntry(
                attr=attr, 
                old=old, 
                new=new
            )
        )

    def print(self):
        if self.buffer:
            print(self.buffer)
            return
        print(self.log)

    def has_attribute_changed(self, attr):
        """
        Checks if an attribute has changed by verifying against the log
        """
        first = None
        last = None

        for i in range(len(self.log)):
            if attr != self.log[i].attr:
                continue
            if not first:
                first = self.log[i]
                continue
            last = self.log[i]

        if not first:
            return False

        if first and not last:
            return True if first.old != first.new else False

        return first.old != last.new

    def has_changed(self):
        """
        Checks if any attribute has been hanged by verifying against the log
        """
        seen = set()
        for entry in self.log:
            if entry.attr in seen:
                continue
            if self.has_attribute_changed(entry.attr):
                return True
            seen.add(entry.attr)
        return False
