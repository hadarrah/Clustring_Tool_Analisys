import logging
from Utils import logger
from Algorithm.chunk import Chunk
from Utils import configuration


class main(object):

    def __init__(self, config, documents, external_vec):
        self.config = config
        self.documents = documents.split()
        self.external_vec = external_vec
        self.stage = 1

        self.log = logging.getLogger(__name__ + "." + __class__.__name__)
        self.log = logger.setup()
        #self.log = logger.add_log_file(self.log, config)

    def run(self, top):
        self.log.info("NEW REGRESSION IS STARTING!")

        # Step 1
        top.set_v_word2vec()

        # Step 2
        self.stage += 1
        top.set_v_tfidf()

        # Step 3
        self.stage += 1
        top.set_v_filtering()

        # Step 4
        self.stage += 1
        raise Exception("fail in stage 4")  # example for raising exception
        top.set_v_metric()

        # Step 5
        self.stage += 1
        top.set_v_pam()

        # Step 6
        self.stage += 1
        top.set_v_silhouette()

        # Step 7
        self.stage += 1
        top.set_v_chunks()

    def get_stage(self):
        return self.stage


if __name__ == "__main__":
    # Unitest
    config = configuration.config().setup()
    main = main(config, "blabla", None)
    main.run()
