from Utils import logger
from Utils import configuration
import logging
from Algorithm.document import Document
import operator

class Statistical_Data(object):
    """
    This class responsible on analyzing and generating data based on the last regression.
    """
    def __init__(self, config, documents, number_of_clusters):
        self.config = config
        self.documents = documents
        self.number_of_styles = number_of_clusters
        self.max_docs_in_style = None
        self.min_docs_in_style = None
        self.log = logging.getLogger(__name__ + "." + __class__.__name__)
        self.log = logger.setup()

    def analyze_data(self):
        """
        Calculate and set general data from the last regression.
        :return:
        """
        self.log.info("Analyze Data")

        # initialize array with zero where each index represents cluster's id
        # and the value is number of documents which belong to cluster
        clusters_vote = [0]*self.number_of_styles

        # calculate array
        for doc in self.documents:
            clusters_vote[doc.get_cluster()] += 1

        # set max and min values
        index, self.max_docs_in_style = max(enumerate(clusters_vote), key=operator.itemgetter(1))
        index, self.min_docs_in_style = min(enumerate(clusters_vote), key=operator.itemgetter(1))

        self.log.info("Number of styles: " + str(self.number_of_styles))
        self.log.info("Max documents in style: " + str(self.max_docs_in_style))
        self.log.info("Min documents in style: " + str(self.min_docs_in_style))

    def get_number_of_styles(self):
        """
        Get the number of styles.
        :return:
        """
        return str(self.number_of_styles)

    def get_max_docs_in_style(self):
        """
        Get the value of maximum documents in cluster.
        :return:
        """
        return str(self.max_docs_in_style)

    def get_min_docs_in_style(self):
        """
        Get the value of minimum documents in cluster.
        :return:
        """
        return str(self.min_docs_in_style)

    def get_documents_distribution_data(self):
        """
        Get the data structure for Documents Distribution graph.
        :return:
        """
        documents = [doc.get_basename() for doc in self.documents]
        styles = []
        for doc in self.documents:
            styles.append(doc.get_cluster()+1)

        data = {'Documents' : documents, 'Styles' : styles}
        return data

