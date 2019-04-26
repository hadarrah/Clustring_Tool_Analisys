from Utils import logger
from Utils import configuration
from Utils import Word2VecWrapper
from numpy import array
import logging
from Algorithm import document


class Chunk(object):

    ID = 0

    def __init__(self, config, text = {}):
        self.chunk_size = config.get("CHUNKS", "size")
        self.delay = config.get("CHUNKS", "delay")
        self.log = logging.getLogger(__name__ + "." + __class__.__name__)
        self.log = logger.setup()
        self.chunkID = None
        self.chunkVec = None
        self.set_chunkID()
        self.Doc = text
        Chunk.createChunk(self)
        Chunk.set_ID(self)
        #self.log = logger.add_log_file(self.log, config)

    def createChunk(self):
        """
        build one chunk for a given text
        :return:
        """
        for t in self.Doc:
            print(t)
            vec = model.get_vector(t)
            print(vec)


    def set_chunkID(self):
        """
        Set the chunk ID
        :return:
        """
        self.chunkID = Chunk.get_ID(self)+1

    def get_chunkID(self):
        """
        Get the number of document
        :return:
         """
        return self.chunkID

    def set_ID(self):
        """
        Set the global ID
        :return:
        """
        Chunk.ID = Chunk.ID + 1

    def get_ID(self):
        """
        Get the global ID
        :return:
         """
        return Chunk.ID

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
    model = Word2VecWrapper.Model(config, filepath="C:\\Users\\Aviram Kounio\\Google Drive\\סמסטר ח\\פרויקט חלק ב\\Text\\wiki.he.vec")

    # option 2: create word embedding based on the documents collection
    #documents = ["C:\\Users\\Aviram Kounio\\Google Drive\\סמסטר ח\\פרויקט חלק ב\\Text\\Bamidbar_chapter_B.txt",
    #             "C:\\Users\\Aviram Kounio\\Google Drive\\סמסטר ח\\פרויקט חלק ב\\Text\\Bereshit_chapter_A.txt",
    #             "C:\\Users\\Aviram Kounio\\Google Drive\\סמסטר ח\\פרויקט חלק ב\\Text\\MelachimB_chapter_C.txt",
    #             "C:\\Users\\Aviram Kounio\\Google Drive\\סמסטר ח\\פרויקט חלק ב\\Text\\Shoftim_chapter_H.txt",
    #             "C:\\Users\\Aviram Kounio\\Google Drive\\סמסטר ח\\פרויקט חלק ב\\Text\\Yiov_chapter_A.txt"]
#
    #model = Word2VecWrapper.Model(config, documents=documents)


    model.build_model()

    #word = "אהבה"
    #if (model.exist_in_vocab(word)):
    #    print(str(model.get_vector(word)))

    #word = "אֶ֖לֶף"
    #if (model.exist_in_vocab(word)):
    #    print(str(model.get_vector(word)))

    text = ['אבירם','בבית','גר']
    c1 = Chunk(config, text)
    print(c1.chunk_size)