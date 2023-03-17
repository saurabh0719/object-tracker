"""
Copyright (c) Saurabh Pujari
All rights reserved.

This source code is licensed under the BSD-style license found in the LICENSE file in the root directory of this source tree.
"""

from .entry import Entry


class QueryLog:
    def __init__(self) -> None:
        self.log = []
        self.buffer = []
        self.log_len = 0
        self.buffer_len = 0

    def __str__(self) -> str:
        return f"QueryLog -> BUFFER {self.buffer_len} LOG {self.log_len}"
    
    def __repr__(self) -> str:
        return str({'log': self.log_len, 'buffer': self.buffer_len})
    
    def __len__(self) -> int:
        return self.log_len
    
    def print(self):
        if self.buffer:
            print(self.buffer)
            return
        print(self.log)

    def _filter(self, entry: Entry, attrs):
            return entry.attr in attrs if attrs else True

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

        if exclude:
            self.buffer = list(filter(lambda x: not self._filter(x, _attrs), self.log))
        else:
            self.buffer = list(filter(lambda x: self._filter(x, _attrs), self.log))
        
        self.buffer_len = len(self.buffer)
        return self

    def filter(self, attrs=None):
        """
            obj.filter(['name',]).fetch()

            - Includes given attributes in the result log
            - Stores temporary filtered result in self.buffer
        """
        return self._process_filter(attrs)
    
    def exclude(self, attrs=None):
        """
            obj.exclude(['name',]).fetch()

            - Encludes given attributes in the result log
            - Stores temporary filtered result in self.buffer
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
        self.log_len = len(self.log)
            
        self.buffer = []
        self.buffer_len = len(self.buffer)

    def count(self) -> None:
        return self.buffer_len if self.buffer else self.log_len

    def push(self, attr, old, new) -> None:
        """
            Pushes a new structured log entry 
        """
        self.log.append(
            Entry(
                attr=attr, 
                old=old, 
                new=new
            )
        )
        self.log_len += 1
