"""
Copyright (c) Saurabh Pujari
All rights reserved.

This source code is licensed under the BSD-style license found in the LICENSE file in the root directory of this source tree.
"""

from datetime import datetime


class LogEntry: 
    """
    A single record in the Change log
    """
    def __init__(self, attr, old, new) -> None:
        self.attr = attr
        self.old = old
        self.new = new 
        self.timestamp = datetime.now()

    def print(self):
        return print(self.__dict__)
    
    def __str__(self) -> str:
        return f"{self.timestamp} - Attribute '{self.attr}' : '{self.old}' --> '{self.new}'"

    def __repr__(self) -> str:
        return str({'attr': self.attr, 'old': self.old, 'new': self.new, 'timestamp': self.timestamp})
