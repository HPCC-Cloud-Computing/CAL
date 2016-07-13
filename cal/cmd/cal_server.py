"""Starter script for Nova OS API."""

import sys

from oslo_config import cfg
from oslo_log import log as logging


from cal import config


CONF = cfg.CONF


def main():
    config.parse_args(sys.argv, default_config_files="/home/techbk/PycharmProjects/CAL/etc/cal/cal.conf")
    logging.setup(CONF, "cal")
