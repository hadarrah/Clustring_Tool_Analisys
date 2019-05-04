from Algorithm import chunk
from Utils import logger
from Utils import configuration
from Utils import Word2VecWrapper
import logging
import operator
import os


class Document(object):
    ID = -1

    def __init__(self, filepath, config):
        self.log = logging.getLogger(__name__ + "." + __class__.__name__)
        self.log = logger.setup()
        self.log = logger.add_log_file(self.log, config)
        self.docID = None
        self.set_docID()
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
        Document.set_ID(self)

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
        #print(words)
        for w in words[index:]:
            if model.exist_in_vocab(w):
                chunkList.append(w)
                wordsCount += 1
                if wordsCount == self.chunkSize:
                    if ((chunkID + 1)> self.DelayPar):
                        preChunks = self.chunks[chunkID - self.DelayPar:chunkID]
                    ch = chunk.Chunk(config, chunkList, self.get_docID(), chunkID, model, preChunks)
                    self.chunksVec.append(ch.chunkVec)
                    self.chunks.append(ch)
                    chunkCount += 1
                    chunkList = []
                    wordsCount = 0
                    chunkID += 1
            else:
                index += 1
        #print(self.chunksVec)
        if chunkCount < self.DelayPar:
            print("Number of chunks incorrect")

    def get_docCollection(self):
        """
        Get the document collection
        :return:
        """
        return Document.docCollection

    def set_docCollection(self, docID, docText):
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

    def set_docID(self):
        """
        Set the number of document
        :return:
        """
        self.docID = Document.ID + 1

    def get_docID(self):
        """
        Get the number of document
        :return:
         """
        return self.docID

    def set_ID(self):
        """
        Set the global ID
        :return:
        """
        Document.ID = Document.ID + 1

    def get_ID(self):
        """
        Get the global ID
        :return:
         """
        return Document.ID

    def get_docText(self) -> object:
        """
        return the text as a string
        :return:
        """
        return self.docText

    def compute_tfidf(self, docCollection):
        """
        Compute tf idf score fol all words in the documents
        :return:
        """
        wordSet = ()  # set of words from all texts
        bowArr = []  # arr of bows. each bow is a list of seperated words of each text
        wordD = []  # list of dicts. each dic for each text
        tfBow = []  # a list of all tf values
        i = 0  # index
        tfidfVal = {}  # a dict of cod index and its tfidf value
        for doc in docCollection.values():
            bowD = doc.split(" ")  # split text to words
            wordSet = set(bowD).union(wordSet)  # build set of words
            bowArr.append(bowD)  # build list of bows
        for bow in bowArr:
            wordDic = (dict.fromkeys(wordSet, 0))  # build dictionary of zeros for each text(bow)
            for word in bow:
                wordDic[word] += 1  # update number of word of each text i te dict
            tf = Document.computeTf(self, wordDic, len(bow))  # compute tf value for each document
            tfBow.append(tf)
            wordD.append(wordDic)  # build list of dicts
        idfs = Document.computeIDF(self, wordD)  # compute idf value

        """cumpute of tfidf= tf*idf"""
        for t in tfBow:
            tfidf = {}
            for word, val in t.items():
                tfidf[word] = val * idfs[word]  # val= Tf value, idfs[word]= idf value
            tfidfVal[i] = tfidf
            i = i + 1
        return tfidfVal  # return dic: key=word, value= tf idf value

    def computeTf(self, wordDict, len):
        """
            Compute de Tf function
        :param wordDict:
        :param len:
        :return:
        """
        tfDict = {}
        bowCount = len
        for word, count in wordDict.items():
            tfDict[word] = count / float(bowCount)
        return tfDict

    def computeIDF(self, documents):
        '''
        Compute the Idf function
        :param documents:
        :return:
        '''
        import math
        idfDict = {}
        N = len(documents)
        idfDict = dict.fromkeys(documents[0].keys(), 0)
        for doc in documents:
            for word, val in doc.items():
                if val > 0:
                    idfDict[word] += 1
        for word, val in idfDict.items():
            idfDict[word] = math.log10(N / float(val))
        return idfDict

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
        to_print += "\nDocument name: " + str(self.get_basename())
        to_print += "\nDocument ID: " + str(self.get_docID())
        to_print += "\nDocument total chunks: " + str(len(self.get_chunks()))
        to_print += "\nDocument total comparable chunks: " + str(len(self.get_comparable_chunks()))
        to_print += "\nDocument cluster: " + str(self.get_cluster())
        to_print += "\n\tDocument chunks summary:"
        for chunk in self.get_chunks():
            cluster = chunk.get_cluster()
            cluster = str(cluster) if (cluster is not None) else "None"
            to_print += "\n\tChunk ID: " + str(chunk.getChunkID()) + "  Chunk Cluster: " + cluster
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
