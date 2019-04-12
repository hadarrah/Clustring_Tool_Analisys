from Utils import logger
from Utils import configuration
from Utils import Word2VecWrapper
import logging


class Chunk(object):

    def __init__(self, config):
        self.chunk_size = config.get("CHUNKS", "size")
        self.delay = config.get("CHUNKS", "delay")

        self.log = logging.getLogger(__name__ + "." + __class__.__name__)
        self.log = logger.setup()
        #self.log = logger.add_log_file(self.log, config)


    def print_delay(self):
        self.log.info("Delay: " + self.delay)

    def print_chunk_size(self):
        self.log.info("Size: " + self.chunk_size)


if __name__ == "__main__":
    # Unitest
    config = configuration.config().setup()
    chunk2 = Chunk(config)
    # functions

    # option 1: external word embedding
    model = Word2VecWrapper.Model(config, filepath="C:\\Users\\Hadar\\Downloads\\wiki.he\\wiki.he.vec")

    # option 2: create word embedding based on the documents collection
    #documents = ["C:\\Users\\Hadar\\Downloads\\texts\\Bamidbar_chapter_B.txt",
    #             "C:\\Users\\Hadar\\Downloads\\texts\\Bereshit_chapter_A.txt",
    #             "C:\\Users\\Hadar\\Downloads\\texts\\MelachimB_chapter_C.txt",
    #             "C:\\Users\\Hadar\\Downloads\\texts\\Shoftim_chapter_H.txt",
    #             "C:\\Users\\Hadar\\Downloads\\texts\\Yiov_chapter_A.txt"]
#
    #model = Word2VecWrapper.Model(config, documents=documents)


    model.build_model()

    word = "אהבה"
    if (model.exist_in_vocab(word)):
        print(str(model.get_vector(word)))

    word = "אֶ֖לֶף"
    if (model.exist_in_vocab(word)):
        print(str(model.get_vector(word)))
