#!/usr/bin/env python
"""
Setup script for divoom-timesgate.
This is here for backward compatibility. The package is configured via pyproject.toml.
"""

from setuptools import setup

if __name__ == "__main__":
    setup(
        scripts=[
            'bin/divoom',
            'bin/divoom-brightness',
            'bin/divoom-screen',
            'bin/divoom-weather',
            'bin/divoom-display',
            'bin/divoom-beep',
            'bin/divoom-text',
        ],
    ) 