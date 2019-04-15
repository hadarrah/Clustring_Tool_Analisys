import logging
from Utils import logger
from Algorithm.chunk import Chunk
from Utils import configuration


class main(object):

    def __init__(self, config, documents, external_vec):
        self.config = config
        self.documents = documents.split()
        self.external_vec = external_vec

        self.log = logging.getLogger(__name__ + "." + __class__.__name__)
        self.log = logger.setup()
        #self.log = logger.add_log_file(self.log, config)

    def run(self):
        self.log.info("NEW REGRESSION IS STARTING!")

        # Step 1
        # Step 2
        # Step 3...


if __name__ == "__main__":
    # Unitest
    config = configuration.config().setup()
    main = main(config, "blabla", None)
    main.run()
