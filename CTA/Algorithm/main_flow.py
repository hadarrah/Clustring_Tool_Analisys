from Utils import logger
from Utils import configuration
import logging
from Algorithm.Chunk import Chunk

config = configuration.config().setup()
log = logger.setup()
log = logger.add_log_file(log, config)


if __name__ == "__main__":
    log.info("NEW REGRESSION IS STARTING!")
    log.error("TEST ERROR")

    chunk = Chunk(config)
    chunk.print_chunk_size()
    chunk.print_delay()
