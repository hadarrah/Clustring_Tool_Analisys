import logging
import sys


def setup():

    fmt = "%(asctime)s %(levelname)s:%(name)s: %(message)s"
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout, format=fmt, filemode='a+')
    log = logging.getLogger(__name__)
    return log

def add_log_file(log, config):

    fmt = logging.Formatter("%(asctime)s %(levelname)s:%(name)s: %(message)s")
    hdlr = logging.FileHandler(config.get("GENERAL", "logfile"), mode='a+')
    hdlr.setFormatter(fmt)
    log.addHandler(hdlr)

    return log
