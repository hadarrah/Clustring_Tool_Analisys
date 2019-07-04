from Utils import logger
import numpy as np
import logging
import math

class Chunk(object):

    def __init__(self, config, text, docID, chunkID, model, preChunks=[]):
        self.chunk_size = config.get("CHUNKS", "size")
        self.delay = config.get("CHUNKS", "delay")
        self.log = logging.getLogger(__name__ + "." + __class__.__name__)
        self.log = logger.setup()
        self.chunkID = chunkID
        self.chunkVec = None
        self.Doc = text
        self.docID = docID
        self.model = model
        self.cluster = None
        self.preChunks = preChunks
        self.ranked_vec = {}
        Chunk.createVec(self)

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
        """
        Set the cluster for this chunk
        :param cluster: cluster's id
        :return:
        """
        self.cluster = cluster

    def get_cluster(self):
        """
        Get the cluster's id for this chunk
        :return: cluster's id
        """
        return self.cluster

    def createVec(self):
        """
        build distances chunk by using cosine similarity
        :return: distances vector
        """
        cosResult = list()
        i = 1
        for d1 in self.Doc:
            j = 0
            for d2 in self.Doc:
                if (j < i):  # skip all the precursors words include this one
                    j += 1
                    continue
                cos = np.dot(self.model.get_vector(d1), self.model.get_vector(d2)) / (
                            np.linalg.norm(self.model.get_vector(d1)) * np.linalg.norm(self.model.get_vector(d2)))
                cosResult.append(cos)
            i += 1
        self.chunkVec = np.array(cosResult)
        self.create_cumulative_vector(self.chunkVec)

    def create_cumulative_vector(self, vector):
        self.cummulative_vector = np.cumsum(vector)
        size = len(self.cummulative_vector)
        interval = math.floor(size/20)
        vec = []
        for i in range(0, size, interval):
            vec.append(self.cummulative_vector[i])

        self.shrinked_vector = np.array(vec)

    def get_shrinked_cummulative_vec(self):
        return self.shrinked_vector
