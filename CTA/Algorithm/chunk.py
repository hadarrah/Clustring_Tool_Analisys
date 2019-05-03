from Utils import logger
from Utils import configuration
from Utils import Word2VecWrapper
import numpy as np
import logging



class Chunk(object):

    def __init__(self, config, text, docID, chunkID, model, preChunks = []):
        self.chunk_size = config.get("CHUNKS", "size")
        self.delay = config.get("CHUNKS", "delay")
        self.log = logging.getLogger(__name__ + "." + __class__.__name__)
        self.log = logger.setup()
        self.chunkID = chunkID
        self.chunkVec = None
        self.Doc = text
        self.docID = docID
        self.model= model
        self.cluster = None
        self.preChunks = preChunks
        Chunk.createVec(self)
        #self.log = logger.add_log_file(self.log, config)

    def get_precursors_chunks(self):
        """
        return the precursors chunks of a given chunk
        in order to compare them
        :return:
        """
        return self.preChunks

    def getchunkVec(self):
        return self.chunkVec


    def getdocID(self):
        """
        docId's chunk getter
        :return:
        """
        return self.docID

    def getChunkID(self):
        """
        ChunkId getter
        :return:
        """
        return self.chunkID

    def set_cluster(self, cluster):
        self.cluster = cluster

    def get_cluster(self):
        return self.cluster

    def createVec(self):
        """
        build distances chunk by using cosin similarity
        :return: dictances vector
        """
        #cosResult = set()      #using set in order to avoid duplications
        cosResult = list()
        i = 1
        for d1 in self.Doc:
            j = 0
            for d2 in self.Doc:
                if (j < i):
                    j += 1
                    continue
                cos = np.dot(self.model.get_vector(d1),self.model.get_vector(d2))/(np.linalg.norm(self.model.get_vector(d1))*np.linalg.norm(self.model.get_vector(d2)))
                cosResult.append(cos)
            i += 1
        self.chunkVec = np.array(cosResult)

    def print_delay(self):
        self.log.info("Delay: " + self.delay)

    def print_chunk_size(self):
        self.log.info("Size: " + self.chunk_size)


if __name__ == "__main__":
    # Unitest
    config = configuration.config().setup()
    #chunk2 = Chunk(config)
    # functions

    # option 1: external word embedding
    model = Word2VecWrapper.Model(config,
                                  filepath="C:\\Users\\Aviram Kounio\\Google Drive\\סמסטר ח\\פרויקט חלק ב\\Text\\wiki.he.vec")

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
    c1 = Chunk(config, text, 10, 0, model)
    print("c1 ID:"  + str(c1.chunkID)+ " " + "c1 doc ID:" + str(c1.docID))
    print(c1.getchunkVec())

