from Utils import logger
from Utils import configuration
import numpy as np
import pandas as pd
import math
import logging


class Distance_Matric(object):
    """
    This class responsible on the distance metric which will delivered into PAM algorithm.
    The input is a documents collection with chunks.
    """
    vectors_dict = {}
    corr_matrix = None

    def __init__(self, config, documents):
        self.config = config
        self.distance_metric = []
        self.documents = documents
        self.comparable_chunks = []
        self.chunks_index = {}
        self.transferred_vectors = []
        Distance_Matric.vectors_dict = {}
        Distance_Matric.corr_matrix = None

        self.log = logging.getLogger(__name__ + "." + __class__.__name__)
        self.log = logger.setup()
        #self.log = logger.add_log_file(self.log, config)

    def build_metric(self):
        """
        This function build the distance metric based on PTHG algorithm.
        :return:
        """
        np.seterr(divide='ignore', invalid='ignore')
        # get all the comparable chunks
        vector_size = int(self.config.get("CHUNKS", "size"))
        vector_size = int((vector_size*(vector_size-1))/2)
        i = 0
        for doc in self.documents:
            self.comparable_chunks.extend(doc.get_comparable_chunks())
            for chunk in doc.get_chunks():
                # transfer chunks vector and treat them as a columns in order to use pd.DataFrame.corr function
                for j in range(0, vector_size):
                    if (i == 0):
                        initial_vector = [chunk.getchunkVec()[j]]
                        self.transferred_vectors.append(initial_vector)
                    else:
                        self.transferred_vectors[j].append(chunk.getchunkVec()[j])
                Distance_Matric.vectors_dict["{}{}".format(chunk.getdocID(), chunk.getChunkID())] = i
                i += 1

        self.log.info("total comparable chunks: " + str(len(self.comparable_chunks)))
        self.create_spearman_matrix()
        # iterate all over the comparable chunks and build their row in the metric
        i = 0
        counter = len(self.comparable_chunks)
        for chunk in self.comparable_chunks:
            counter -= 1
            self.log.info("calculating metric's cell for chunk ID {} in Doc ID {}.   (chunks left: {})".format(chunk.getChunkID(), chunk.getdocID(), counter))
            chunk_metric_row = []
            j = 0

            # calculate the distance between the chunks based on dzv function
            for compared_chunk in self.comparable_chunks:
                dzv_val = self.compute_dzv(chunk, compared_chunk) if (i <= j) else self.distance_metric[j][i]
                chunk_metric_row.append(dzv_val)
                j += 1

            self.distance_metric.append(chunk_metric_row)
            # save the chunk's index in the  metric in order to be able to recognize them after PAM
            self.chunks_index[i] = chunk
            i += 1
        self.distance_metric = np.matrix(self.distance_metric)
        np.set_printoptions(precision=3)
        for row in self.distance_metric:
            self.log.info(row)


    def compute_dzv(self, chunk1, chunk2):
        """
        DZV function from PTHG algorithm.
        :param chunk1: first Chunk in the comparison
        :param chunk2: second Chunk in the comparison
        :return: distance value between the chunks
        """
        zv_homogeneous_1 = Distance_Matric.compute_zv(chunk1, chunk1.get_precursors_chunks())
        zv_heterogeneous_1 = Distance_Matric.compute_zv(chunk1, chunk2.get_precursors_chunks())
        zv_homogeneous_2 = Distance_Matric.compute_zv(chunk2, chunk2.get_precursors_chunks())
        zv_heterogeneous_2 = Distance_Matric.compute_zv(chunk2, chunk1.get_precursors_chunks())

        return abs(zv_homogeneous_1 + zv_homogeneous_2 - zv_heterogeneous_1 - zv_heterogeneous_2)

    def create_spearman_matrix(self):
        """
        Create spearman correlation matrix for all chunks (including the incomparable chunks)
        :return:
        """
        self.log.info("Calculate spearman correlation matrix")
        df = pd.DataFrame(self.transferred_vectors)
        Distance_Matric.corr_matrix = df.corr(method="spearman")
        print(str(Distance_Matric.corr_matrix))


    @staticmethod
    def compute_zv(chunk, precursors_chunks):
        """
        ZV function from PTHG algorithm.
        :param chunk: Chunk to compare with
        :param precursors_chunks: set of precursors Chunks to compare with (based on the delay parameter)
        :return: similarity value between the chunks
        """
        sum = 0
        for pre_chunk in precursors_chunks:
            i = Distance_Matric.vectors_dict["{}{}".format(chunk.getdocID(), chunk.getChunkID())]
            j = Distance_Matric.vectors_dict["{}{}".format(pre_chunk.getdocID(), pre_chunk.getChunkID())]
            corr = Distance_Matric.corr_matrix[i][j]
            if (math.isnan(corr)):
                corr = 0.0
            sum += corr

        return sum/int(len(precursors_chunks))

    def get_distance_metric(self):
        """
        Get the distance metric
        :return: distance metric
        """
        return self.distance_metric

    def get_chunks_index(self):
        """
        Get the chunks index dictionary
        :return: dictionary where key is chunk's row from distance metric and value is the chunk object
        """
        return self.chunks_index


if __name__ == "__main__":
    # Unitest
    config = configuration.config().setup()
    # functions


