#!/usr/bin/env python3
"""
This module contains the function to_kv which takes a string and an int
or float
"""
from typing import Union, Tuple


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """Returns a tuple of a string and a float."""
    return (k, float(v**2))
