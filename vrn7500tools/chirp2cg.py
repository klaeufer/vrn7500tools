#!/usr/bin/env python

from . import helpers

import argparse
import itertools
import logging
import sys

def main():
    parser = argparse.ArgumentParser(description="converts CHIRP csv from RepeaterBook to JSON channel group for Vero N-7500/Retevis RT99")
    parser.add_argument("-n", "--name", help="channel group name", nargs='?', type=str, default="Unnamed Channel Group")
    parser.add_argument("-s", "--skip", help="number of leading rows to skip", nargs='?', type=int, default=0)
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG)
    logging.info(args)

    helpers.chirp2cg(sys.stdin, args.name, args.skip)
