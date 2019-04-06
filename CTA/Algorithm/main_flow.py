import logging
from Utils import logger
from Algorithm.Chunk import Chunk
from Utils import configuration


class main(object):

    def __init__(self, config):
        self.config = config

        self.log = logging.getLogger(__name__ + "." + __class__.__name__)
        self.log = logger.add_log_file(self.log, config)

    def run(self):
        self.log.info("NEW REGRESSION IS STARTING!")
        chunk = Chunk(self.config)
        chunk.print_chunk_size()
        chunk.print_delay()
        # Step 1
        # Step 2
        # Step 3...


if __name__ == "__main__":
    # Unitest
    config = configuration.config().setup()
    main = main(config)
    #main.run()
