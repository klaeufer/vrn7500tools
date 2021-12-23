#!/usr/bin/env python

from . import helpers

import argparse
import logging
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", help="", nargs='?', type=str, default="Unnamed Channel Group")
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG)
    logging.info(args)

    helpers.chirp2cg(sys.stdin, args.name)
