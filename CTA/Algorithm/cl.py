from Utils import logger
from Utils import configuration
from pyclustering.cluster import kmedoids
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
        for k in range(self.config.get("CLUSTER", "from"), self.config.get("CLUSTER", "to")):
            kmedoids_instance = kmedoids(self.distance_metric, k, data_type='distance_matrix')
            kmedoids_instance.process()
            self.clustring_results.append(kmedoids_instance)

    def get_silhouette(self, cl):
        """
        Get the silhouette coefficients as an average for all the elements.
        :param cl: clustering result
        :return:   silhouette avg score
        """
        clusters = cl.get_clusters()
        silhouette_width = silhouette_score(self.distance_metric, clusters, metric="precomputed")
        return silhouette_width

    def get_best_clustering_result(self):
        """
        Get the best result among the clustering result in the range.
        :return: the best clustering result
        """
        max_silhouette = -1
        cl_max = None
        for cl_result in self.clustring_results:
            current = self.get_silhouette(cl_result)
            if (current > max_silhouette):
                max_silhouette = current
                cl_max = cl_result

        return cl_max


if __name__ == "__main__":
    # Unitest
    config = configuration.config().setup()
    # functions


