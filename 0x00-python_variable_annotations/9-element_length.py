#!/usr/bin/env python3
"""This module contains the function element_length which takes a list of"""
from typing import Iterable, List, Sequence, Tuple


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """Returns a list of tuples of a sequence and its length."""
    return [(i, len(i)) for i in lst]
