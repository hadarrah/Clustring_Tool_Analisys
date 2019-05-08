from Utils import logger
from Utils import configuration
from pyclustering.cluster.kmedoids import kmedoids
from sklearn.metrics import silhouette_score
import logging


class CL(object):
    """
    This class represents the clustering result using PAM algorithm.
    For each result in the range([from, to]) the class calculates the silhouette score and return the best result.
    """
    def __init__(self, config, distance_metric):
        self.config = config
        self.distance_metric = distance_metric
        self.clustring_results = []

        self.log = logging.getLogger(__name__ + "." + __class__.__name__)
        self.log = logger.setup()
        #self.log = logger.add_log_file(self.log, config)


    def generate_clusters(self):
        """
        Call to PAM algorithm for each k value in the range.
        :return:
        """
        to = min(int(self.config.get("CLUSTER", "to"))+1, len(self.distance_metric))
        for k in range(int(self.config.get("CLUSTER", "from")), to):
            intial_mediods_index = [index for index in range(0, k)] # randomize initial mediods start from 0 till k
            kmedoids_instance = kmedoids(self.distance_metric, intial_mediods_index, data_type='distance_matrix')
            kmedoids_instance.process()
            self.clustring_results.append(kmedoids_instance)

    def get_silhouette(self, cl):
        """
        Get the silhouette coefficients as an average for all the elements.
        :param cl: clustering result
        :return:   silhouette avg score
        """
        # get the clusters result with the following example format: [[0,4][1,2,3]] -> 2 clusters
        # where the indexes inside represents the chunk's row from distance metric
        clusters = cl.get_clusters()


        # initialize array with size of the comparable chunks
        # each index in the array represent the chunk'a row from distance metric while the value is the cluster's id
        cluster_indicator = [0] * len(self.distance_metric)

        i = 0
        for cluster in clusters:
            for chunk_index in cluster:
                cluster_indicator[chunk_index] = i
            i += 1

        silhouette_width = silhouette_score(self.distance_metric, cluster_indicator, metric="precomputed")
        #self.log.info("\nK={num_clusters}\n{result}\nSilhouette width={sil}".format(num_clusters=str(len(clusters)),
        #                                                                            result=str(clusters),
        #                                                                            sil=str(silhouette_width)))
        self.log.info("K={num_clusters}".format(num_clusters=str(len(clusters))))
        self.log.info("{result}".format(result=str(clusters)))
        self.log.info("Silhouette width={sil}".format(sil=str(silhouette_width)))
        return silhouette_width, cluster_indicator

    def get_best_clustering_result(self):
        """
        Get the best result among the clustering result in the range.
        :return: the best clustering result
        """
        max_silhouette = -1
        cl_max = None
        indicator_max = None
        for cl_result in self.clustring_results:
            current, cluster_indicator = self.get_silhouette(cl_result)
            if (current > max_silhouette):
                max_silhouette = current
                cl_max = cl_result
                indicator_max = cluster_indicator

        return cl_max, indicator_max


if __name__ == "__main__":
    # Unitest
    config = configuration.config().setup()
    # functions


