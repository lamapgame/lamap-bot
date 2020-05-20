#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Dylan Tientcheu"
__version__ = "0.1.0"
__license__ = "MIT"

from logzero import logger


def main():
    """ Main entry point of the app """
    logger.debug("Hello")


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
