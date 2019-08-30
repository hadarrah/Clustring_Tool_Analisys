import logging
import sys


def setup(log_level=logging.INFO):

    fmt = "%(asctime)s %(levelname)s:%(name)s: %(message)s"
    logging.basicConfig(level=log_level, stream=sys.stdout, format=fmt, filemode='a+')
    log = logging.getLogger(__name__)
    return log

def add_log_file(log, logfile):

    fmt = logging.Formatter("%(asctime)s %(levelname)s:%(name)s: %(message)s")
    hdlr = logging.FileHandler(logfile, mode='a+')
    hdlr.setFormatter(fmt)
    log.addHandler(hdlr)

    return log

def reset_logging():
    # Remove all handlers associated with the root logger object.
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

