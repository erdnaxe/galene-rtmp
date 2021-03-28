# Copyright (C) 2021 Alexandre Iooss
# SPDX-License-Identifier: MIT

"""
Main script for Galène RTMP gateway.
"""

import argparse
import asyncio
import logging
import sys

from galene_rtmp.galene import GaleneClient


def main(opt: argparse.Namespace):
    """Init Galène client and start gateway

    :param opt: program options
    :type opt: argparse.Namespace
    """
    client = GaleneClient(
        options.group, options.server, options.username, options.password
    )

    # Connect and run main even loop
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(client.connect())
    event_loop.run_until_complete(client.loop(event_loop))


if __name__ == "__main__":
    # Arguments parser
    parser = argparse.ArgumentParser(
        prog="galene-rtmp",
        description="RTMP to Galène gateway.",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        default=False,
        help="debug mode: show debug messages",
    )
    parser.add_argument(
        "--server",
        required=True,
        help='Server to connect to, e.g. "wss://galene.example.com/ws"',
    )
    parser.add_argument(
        "--group",
        required=True,
        help="Join this group",
    )
    parser.add_argument(
        "--username",
        required=True,
        help="Group username",
    )
    parser.add_argument(
        "--password",
        help="Group password",
    )
    options = parser.parse_args()

    # Configure logging
    level = logging.DEBUG if options.debug else logging.INFO
    logging.addLevelName(logging.INFO, "\033[1;36mINFO\033[1;0m")
    logging.addLevelName(logging.WARNING, "\033[1;33mWARNING\033[1;0m")
    logging.addLevelName(logging.ERROR, "\033[1;91mERROR\033[1;0m")
    logging.addLevelName(logging.DEBUG, "\033[1;30mDEBUG")
    logging.basicConfig(
        level=level,
        format="\033[90m%(asctime)s\033[1;0m [%(name)s] %(levelname)s %(message)s\033[1;0m",
    )

    try:
        main(options)
    except KeyboardInterrupt:
        sys.exit(1)
