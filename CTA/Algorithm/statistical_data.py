from Utils import logger
from Utils import configuration
import logging
from Algorithm.document import Document
from Algorithm.distance_matric import Distance_Matric
import operator

class Statistical_Data(object):
    """
    This class responsible on analyzing and generating data based on the last regression.
    """
    def __init__(self, config, documents, number_of_clusters, silhouette_width, max_chunks_in_doc):
        self.config = config
        self.documents = documents
        self.max_chunks_in_doc = max_chunks_in_doc
        self.number_of_chunks_styles = number_of_clusters
        self.silhouette_width = round(silhouette_width, 6)
        self.max_docs_in_style = None
        self.min_docs_in_style = None
        self.number_of_documents_styles = 0
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
        clusters_vote = [0]*self.number_of_chunks_styles

        # calculate array
        for doc in self.documents:
            clusters_vote[doc.get_cluster()] += 1

        # calculate the number of styles per documents
        for cluster_index in clusters_vote:
            if (cluster_index > 0):
                self.number_of_documents_styles += 1

        # set max and min values
        index, self.max_docs_in_style = max(enumerate(clusters_vote), key=operator.itemgetter(1))
        index, self.min_docs_in_style = min(enumerate(clusters_vote), key=operator.itemgetter(1))

        self.log.info("Number of Documents styles: " + str(self.number_of_documents_styles))
        self.log.info("Number of Chunks styles: " + str(self.number_of_chunks_styles))
        self.log.info("Max documents in style: " + str(self.max_docs_in_style))
        self.log.info("Min documents in style: " + str(self.min_docs_in_style))

    def get_number_of_documents_styles(self):
        """
        Get the number of documents styles.
        :return:
        """
        return str(self.number_of_documents_styles)

    def get_number_of_chunks_styles(self):
        """
        Get the number of chunks styles.
        :return:
        """
        return str(self.number_of_chunks_styles)

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

    def get_silhouette(self):
        """
        Get the silhouette width for the clustering result
        :return:
        """
        return str(self.silhouette_width)

    def get_documents(self):
        """
        Get the documents list.
        :return:
        """
        return self.documents

    def get_documents_distribution_data(self):
        """
        Get the data structure for Documents Distribution graph.
        :return:
        """
        documents = [doc.get_basename().split(".")[0] for doc in self.documents]
        styles = []
        for doc in self.documents:
            styles.append(doc.get_cluster()+1)

        data = {'Documents' : documents, 'Styles' : styles}
        return data

    def get_chunks_distribution_data(self, doc):
        """
        Get the data structure for Chunks Distribution graph.
        :return:
        """
        chunks = []
        styles = []
        i = 1
        if (isinstance(doc, str) and doc == "All Documents"):
            chunks_leading_zeroes_str = ":0{}d".format(len(str(self.max_chunks_in_doc)))
            ch_str = "ch-{" + chunks_leading_zeroes_str + "}"
            doc_chunk_str = "doc-{}-" + ch_str
            for document in self.documents:
                i = 1
                for chunk in document.get_comparable_chunks():
                    chunks.append(doc_chunk_str.format(document.get_basename().split(".")[0], i))
                    styles.append(chunk.get_cluster() + 1)
                    i += 1
        else:
            leading_zeroes_str = ":0{}d".format(len(str(len(doc.get_comparable_chunks()))))
            ch_str = "ch-{" + leading_zeroes_str + "}"
            for chunk in doc.get_comparable_chunks():
                chunks.append(ch_str.format(i))
                styles.append(chunk.get_cluster()+1)
                i += 1

        data = {'Chunks' : chunks, 'Styles' : styles}
        return data

    def get_zv_dependencies_data(self, doc):
        """
        Get the data structure for ZV dependencies graph.
        :return:
        """
        chunks = []
        zv = []
        i = 1
        if (isinstance(doc, str) and doc == "All Documents"):
            chunks_leading_zeroes_str = ":0{}d".format(len(str(self.max_chunks_in_doc)))
            ch_str = "ch-{" + chunks_leading_zeroes_str + "}"
            doc_chunk_str = "doc-{}-" + ch_str
            for document in self.documents:
                i = 1
                for chunk in document.get_comparable_chunks():
                    chunks.append(doc_chunk_str.format(document.get_basename().split(".")[0], i))
                    zv.append(Distance_Matric.compute_zv(chunk, chunk.get_precursors_chunks()))
                    i += 1
        else:
            leading_zeroes_str = ":0{}d".format(len(str(len(doc.get_comparable_chunks()))))
            ch_str = "ch-{" + leading_zeroes_str + "}"
            for chunk in doc.get_comparable_chunks():
                chunks.append(ch_str.format(i))
                zv.append(Distance_Matric.compute_zv(chunk, chunk.get_precursors_chunks()))
                i += 1

        data = {'Chunks' : chunks, 'ZV' : zv}
        return data

