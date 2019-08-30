from pyclustering.cluster.kmedoids import kmedoids
import logging
from pyclustering.cluster.silhouette import silhouette
import multiprocessing
from multiprocessing.dummy import Pool as ThreadPool
from Utils import logger


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
        self.log = logger.add_log_file(self.log, config.get("GENERAL", "logfile"))

    def generate_clusters(self):
        """
        Call to PAM algorithm for each k value in the range.
        :return:
        """
        to = min(int(self.config.get("CLUSTER", "to"))+1, len(self.distance_metric))

        num_of_cpu = int(multiprocessing.cpu_count())

        # prepare arguments
        updates_in_parallel = []
        for k in range(int(self.config.get("CLUSTER", "from")), to):
            updates_in_parallel.append({"distance_metric": self.distance_metric, "k": k, "log": self.log})

        # create pool
        pool = ThreadPool(num_of_cpu)
        results = pool.map(calculate_k_clusters, updates_in_parallel)

        # close the pool and wait for the work to finish
        pool.close()
        pool.join()

        self.clustring_results = results

    def get_best_clustering_result(self):
        """
        Get the best result among the clustering result in the range.
        :return: the best clustering result
        """
        max_silhouette = -1
        cl_max = None
        indicator_max = None

        num_of_cpu = int(multiprocessing.cpu_count())

        # prepare arguments
        updates_in_parallel = []
        for cl_result in self.clustring_results:
            updates_in_parallel.append({"cl": cl_result, "distance_metric": self.distance_metric, "log": self.log})

        # create pool
        pool = ThreadPool(num_of_cpu)
        results = pool.map(get_silhouette, updates_in_parallel)

        # close the pool and wait for the work to finish
        pool.close()
        pool.join()

        for res in results:
            current = res[0]
            cluster_indicator = res[1]
            cl_result = res[2]
            if (current > max_silhouette):
                max_silhouette = current
                cl_max = cl_result
                indicator_max = cluster_indicator

        return cl_max, indicator_max, max_silhouette


def get_silhouette(args_dict):
    """
    Get the silhouette coefficients as an average for all the elements.
    :param cl: clustering result
    :return:   silhouette avg score
    """
    cl = args_dict["cl"]
    distance_metric = args_dict["distance_metric"]
    log = args_dict["log"]
    # get the clusters result with the following example format: [[0,4][1,2,3]] -> 2 clusters
    # where the indexes inside represents the chunk's row from distance metric
    clusters = cl.get_clusters()
    # initialize array with size of the comparable chunks
    # each index in the array represent the chunk'a row from distance metric while the value is the cluster's id
    cluster_indicator = [0] * len(distance_metric)
    i = 0
    for cluster in clusters:
        for chunk_index in cluster:
            cluster_indicator[chunk_index] = i
        i += 1
    silhouette_width_list = silhouette(distance_metric,clusters).process().get_score()
    silhouette_width = 0
    for score in silhouette_width_list:
        silhouette_width += score
    silhouette_width = float(silhouette_width)/len(silhouette_width_list)
    log.info("K={num_clusters}".format(num_clusters=str(len(clusters))))
    log.info("{result}".format(result=str(clusters)))
    log.info("Silhouette width={sil}".format(sil=str(silhouette_width)))
    return silhouette_width, cluster_indicator, cl


def calculate_k_clusters(args_dict):
    log = args_dict["log"]
    distance_metric = args_dict["distance_metric"]
    k = args_dict["k"]

    log.info("Calculate for k={}".format(str(k)))
    intial_mediods_index = [index for index in range(0, k)]  # randomize initial mediods start from 0 till k
    kmedoids_instance = kmedoids(distance_metric, intial_mediods_index, data_type='distance_matrix')
    kmedoids_instance.process()
    return kmedoids_instance