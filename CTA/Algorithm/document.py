from Algorithm import chunk
from Utils import logger
from Utils import configuration
from Utils import Word2VecWrapper
import logging
import operator
import os


class Document(object):

    def __init__(self, filepath, config, id):
        self.log = logging.getLogger(__name__ + "." + __class__.__name__)
        self.log = logger.setup()
        self.docID = id
        self.docPath = filepath
        self.basename = os.path.basename(filepath)
        self.docText = self.getText(self.docPath)
        self.chunksVec = []  # the distances vector
        self.chunks = []
        self.chunkSize = int(config.get("CHUNKS", "size"))
        self.DelayPar = int(config.get("CHUNKS", "delay"))
        self.cluster = None
        self.s = int(config.get("TF-IDF", "num_of_words_per_doc"))
        self.confog = config

    def get_chunksVec(self):
        """
        Get the chunk's vector
        :return:
        """
        return self.chunksVec

    def get_chunks(self):
        """
        Get the chunks for this document
        :return:
        """
        return self.chunks

    def get_comparable_chunks(self):
        """
        return the comparable document's chunks
        according to delay parameter
        :return:
        """
        return self.chunks[self.DelayPar:]

    def createChunks(self,text,model,config):
        """
        create chunks for each document in the collection
        :param docList:
        :return:
        """
        chunkID = 0
        words = text
        index = 0
        wordsCount = 0
        chunkList = []
        chunkCount = 0
        preChunks = []
        for w in words:
            if model.exist_in_vocab(w):
                chunkList.append(w)
                wordsCount += 1
                if wordsCount == self.chunkSize:
                    if ((chunkID + 1)> self.DelayPar):
                        preChunks = self.chunks[chunkID - self.DelayPar:chunkID]
                    ch = chunk.Chunk(config, chunkList, self.get_docID(), chunkID, model, preChunks)
                    #self.chunksVec.append(ch.chunkVec)
                    self.chunks.append(ch)
                    chunkCount += 1
                    chunkList = []
                    wordsCount = 0
                    chunkID += 1
            else:
                index += 1

    @staticmethod
    def get_docCollection():
        """
        Get the document collection
        :return:
        """
        return Document.docCollection

    @staticmethod
    def set_docCollection( docID, docText):
        """
        Insert each new document into docs collection (dictionary)
        :param docID:
        :param docText:
        :return:
        """
        Document.docCollection = {docID: docText}

    def getText(self, filepath):
        """
        Get the original text of the document
        :param filepath:
        :return:
        """
        with open(filepath, mode='r', encoding='utf-8-sig', errors='ignore') as file_handler:
            return file_handler.read()

    def get_docID(self):
        """
        Get the number of document
        :return:
         """
        return self.docID

    def get_docText(self):
        """
        return the text as a string
        :return:
        """
        return self.docText

    def compute_cluster(self, number_of_clusters):
        """
        Compute and set the cluster for this document base on majority chunks vote
        :param number_of_clusters: final number of clusters after silhouette
        :return:
        """
        # initialize array with zero to indicate the chunks votes,
        # each index in the array represents the cluster and the value the sum of vote
        chunks_vote = [0] * number_of_clusters

        # calculate the votes
        for chunk in self.get_comparable_chunks():
            chunks_vote[chunk.get_cluster()] += 1

        # get the maximum cluster's votes
        index, value = max(enumerate(chunks_vote), key=operator.itemgetter(1))

        # set the cluster
        self.cluster = index

    def get_cluster(self):
        """
        Get the cluster's id
        :return:
        """
        return self.cluster

    def get_basename(self):
        """
        Get the basename of document file
        :return:
        """
        return self.basename

    def __str__(self):
        """
        toString method
        :return:
        """
        to_print = ""
        to_print += "\n{:>34} {}".format("Document name: ", str(self.get_basename()))
        to_print += "\n{:>34} {}".format("Document ID: ", str(self.get_docID()))
        to_print += "\n{:>34} {}".format("Document total chunks: ", str(len(self.get_chunks())))
        to_print += "\n{:>34} {}".format("Document total comparable chunks: ", str(len(self.get_comparable_chunks())))
        to_print += "\n{:>34} {}".format("Document cluster: ", str(self.get_cluster() + 1))
        for chunk in self.get_chunks():
            cluster = chunk.get_cluster()
            cluster = str(cluster + 1) if (cluster is not None) else "None"
            to_print += "\n{:>34} {} <-> {} {}".format("Chunk ID: ", str(chunk.getChunkID()), "Chunk Cluster:", cluster)
        return to_print



if __name__ == "__main__":
    config = configuration.config().setup()
    model = Word2VecWrapper.Model(config,
                                  filepath="C:\\Users\\Aviram Kounio\\Google Drive\\סמסטר ח\\פרויקט חלק ב\\Text\\wiki.he.vec")
    s = int(config.get("TF-IDF", "num_of_words_per_doc"))
    model.build_model()
    wordsList = []
    docCollection = {}  # all documents in one document as a dictionary
    docList = []  # list of Document objects
    Doc = ["C:\\Users\\Aviram Kounio\\Google Drive\\סמסטר ח\\פרויקט חלק ב\\Text\\a.txt",
           "C:\\Users\\Aviram Kounio\\Google Drive\\סמסטר ח\\פרויקט חלק ב\\Text\\b.txt"]
    #  "C:\\Users\\Aviram Kounio\\Google Drive\\סמסטר ח\\פרויקט חלק ב\\Text\\c.txt"
    for d in Doc:  # d = document path
        Doc1 = Document(d, config)
        docCollection[Doc1.get_docID()] = Doc1.getText(d)  # build dic of documents
        docList.append(Doc1)  # build list of document objects
        Doc1.createChunks(["אבירם", "גר", "בבית"], model, config)
        print(Doc1)
        break
