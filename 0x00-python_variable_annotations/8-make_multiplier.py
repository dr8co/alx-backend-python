#!/usr/bin/env python3
"""
This module contains the function make_multiplier which takes a float
"""
from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """Returns a function that multiplies a float by multiplier."""
    return lambda x: x * multiplier
