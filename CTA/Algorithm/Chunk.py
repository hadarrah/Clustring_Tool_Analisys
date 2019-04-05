from Utils import logger
import logging


class Chunk(object):

    def __init__(self, config):
        self.chunk_size = config.get("CHUNKS", "chunk_size")
        self.delay = config.get("CHUNKS", "delay")

        self.log = logging.getLogger(__name__ + "." + __class__.__name__)
        self.log = logger.add_log_file(self.log, config)


    def print_delay(self):
        self.log.info("Delay: " + self.delay)

    def print_chunk_size(self):
        self.log.info("Size: " + self.chunk_size)

