from Utils import logger
from Utils import configuration
import logging
from Algorithm.document import Document
import operator

class Statistical_Data(object):

    def __init__(self, config, documents, number_of_clusters):
        self.config = config
        self.documents = documents
        self.number_of_styles = number_of_clusters
        self.max_docs_in_style = None
        self.min_docs_in_style = None
        self.log = logging.getLogger(__name__ + "." + __class__.__name__)
        self.log = logger.setup()

    def analyze_data(self):
        self.log.info("Analyze Data")
        clusters_vote = [0]*self.number_of_styles
        for doc in self.documents:
            clusters_vote[doc.get_cluster()] += 1

        index, self.max_docs_in_style = max(enumerate(clusters_vote), key=operator.itemgetter(1))
        index, self.min_docs_in_style = min(enumerate(clusters_vote), key=operator.itemgetter(1))

    def get_number_of_styles(self):
        return str(self.number_of_styles)

    def get_max_docs_in_style(self):
        return str(self.max_docs_in_style)

    def get_min_docs_in_style(self):
        return str(self.min_docs_in_style)

    def get_documents_clustring_data(self):
        documents = [doc.get_basename() for doc in self.documents]
        styles = []
        for doc in self.documents:
            styles.append(doc.get_cluster()+1)

        data = {'Documents' : documents, 'Styles' : styles}
        return data

