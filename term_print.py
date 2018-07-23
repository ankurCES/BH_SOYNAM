#!/usr/bin/env python
# encoding: utf-8
'''
Custom print methods for visualization and logging to file
'''

import sys
import logging
from datetime import datetime

# Uncomment for file logging
logging.basicConfig(
    # filename='logs/{:%Y-%m-%d %H:%M}.app_run.log'.format(datetime.now()),
    level=logging.DEBUG,
    format="%(asctime)s:%(levelname)s:%(message)s"
    )


def error(string, exception_message = None):
    print("\033[91m {}\033[00m" .format(string))
    # logging.error(string + '\n' + exception_message)

def success(string):
    print("\033[92m {}\033[00m" .format(string))
    # logging.debug(string)

def info(string):
    print("\033[96m {}\033[00m" .format(string))
    # logging.info(string)

def warning(string):
    print("\033[93m {}\033[00m" .format(string))
    # logging.warning(string)

def _print(string):
    sys.stdout.write("\r"+string)
    sys.stdout.flush()
