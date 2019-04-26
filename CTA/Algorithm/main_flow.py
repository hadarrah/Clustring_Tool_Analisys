import logging
from Utils import logger
from Algorithm.chunk import Chunk
from Utils import configuration
from Utils.Word2VecWrapper import Model

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

        ################## Step 1 ##################
        self.log.info("Step 1: Get Texts")
        top.set_v_stage(self.stage)


        ################## Step 2 ##################
        self.log.info("Step 2: Word2Vec")
        self.stage += 1

        if (self.external_vec):
            model = Model(self.config, filepath=self.external_vec)
        else:
            model = Model(self.config, documents=self.Documents_Collection)
        model.build_model()

        top.set_v_stage(self.stage)


        ################## Step 3 ##################
        self.log.info("Step 2: Build Chunks")
        self.stage += 1
        top.set_v_stage(self.stage)


        ################## Step 4 ##################
        self.log.info("Step 4: Build Distance Metric")
        self.stage += 1
        #raise Exception("fail in stage 4")  # example for raising exception
        top.set_v_stage(self.stage)


        ################## Step 5 ##################
        self.log.info("Step 5: PAM")
        self.stage += 1
        top.set_v_stage(self.stage)


        ################## Step 6 ##################
        self.log.info("Step 6: Silhouette")
        self.stage += 1
        top.set_v_stage(self.stage)


    def get_stage(self):
        return self.stage


if __name__ == "__main__":
    # Unitest
    config = configuration.config().setup()
    main = main(config, "blabla", None)
    main.run()
