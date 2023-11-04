"""Lethal Input"""

from dataclasses import dataclass


@dataclass
class Input:
    """User input passed to Module.update"""

    dt: float
    keys: list[str]

    @classmethod
    def key_to_str(cls, key):
        """Convert keystroke objects to strings"""
        if key.is_sequence:
            return key.name
        return str(key)
