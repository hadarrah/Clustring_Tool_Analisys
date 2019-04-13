from Utils import logger
from Utils import configuration
from Algorithm import document
import numpy as np
from Algorithm import chunk
from Algorithm import cl
from scipy.stats import spearmanr

import logging


class Distance_Matric(object):
    """
    This class responsible on the distance metric which will delivered into PAM algorithm.
    The input is a documents collection with chunks.
    """
    def __init__(self, config, documents):
        self.config = config
        self.distance_metric = []
        self.documents = documents
        self.comparable_chunks = []
        self.chunks_index = {}

        self.log = logging.getLogger(__name__ + "." + __class__.__name__)
        self.log = logger.setup()
        #self.log = logger.add_log_file(self.log, config)

    def build_metric(self):
        """
        This function build the distance metric based on PTHG algorithm.
        :return:
        """
        # get all the comparable chunks
        for doc in self.documents:
            self.comparable_chunks.append(doc.get_comparable_chunks())    # <- from Aviram

        # iterate all over the comparable chunks and build their row in the metric
        for chunk in self.comparable_chunks:
            chunk_metric_row = []

            # calculate the distance between the chunks based on dzv function
            for compared_chunk in self.comparable_chunks:
                dzv_val = self.compute_dzv(chunk, compared_chunk)
                chunk_metric_row.append(dzv_val)

            self.distance_metric.append(chunk_metric_row)
            # save the chunk's index in the  metric in order to be able to recognize them after PAM
            self.chunks_index[1] = chunk


    def compute_dzv(self, chunk1, chunk2):
        """
        DZV function from PTHG algorithm.
        :param chunk1: first Chunk in the comparison
        :param chunk2: second Chunk in the comparison
        :return: distance value between the chunks
        """
        zv_homogeneous_1 = self.compute_zv(chunk1, chunk1.get_precursors_chunks())      # <- from Aviram
        zv_heterogeneous_1 = self.compute_zv(chunk1, chunk2.get_precursors_chunks())    # <- from Aviram
        zv_homogeneous_2 = self.compute_zv(chunk2, chunk2.get_precursors_chunks())      # <- from Aviram
        zv_heterogeneous_2 = self.compute_zv(chunk2, chunk1.get_precursors_chunks())    # <- from Aviram

        return abs(zv_homogeneous_1 + zv_homogeneous_2 - zv_heterogeneous_1 - zv_heterogeneous_2)

    def compute_zv(self, chunk, precursors_chunks):
        """
        ZV function from PTHG algorithm.
        :param chunk: Chunk to compare with
        :param precursors_chunks: set of precursors Chunks to compare with (based on the delay parameter)
        :return: similarity value between the chunks
        """
        sum = 0
        chunk_vec = chunk.get_vector()  # <- from Aviram
        for pre_chunk in precursors_chunks:
            corr, p_value = spearmanr(chunk_vec, pre_chunk.get_vector())
            sum += corr

        return sum/self.config.get("CHUNKS", "delay")

    def get_distance_metric(self):
        return self.distance_metric

    def get_chunks_index(self):
        return self.chunks_index




if __name__ == "__main__":
    # Unitest
    config = configuration.config().setup()
    # functions


