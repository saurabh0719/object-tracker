"""
Copyright (c) Saurabh Pujari
All rights reserved.

This source code is licensed under the BSD-style license found in the LICENSE file in the root directory of this source tree.
"""


class InitialStateMissingException(Exception):
    def __init__(self, message=None):
        help = "initial_state param needs to be set for the Tracker -> tracker = Tracker(initial_state=obj)"
        self.message = message or help

    def __str__(self):
        return f"InitialStateMissingError -> {self.message}"
