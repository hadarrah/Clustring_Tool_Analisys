import logging
from Utils import configuration
from Utils import logger
from Algorithm import chunk


class Document(object):
    ID = 0

    def __init__(self, filepath=None):
        self.log = logging.getLogger(__name__ + "." + __class__.__name__)
        self.log = logger.setup()
        # self.log = logger.add_log_file(self.log, config)
        self.docID = None
        self.set_docID()
        self.docPath = filepath
        self.docText = self.getText(self.docPath)
        self.chunks = []
        Document.set_ID(Document.ID)
        Document.set_docCllection(self, self.docID, self.docText)

    def get_docCllection(self):
        return Document.docCollection

    def set_docCllection(self, docID, docText):
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
        with open(filepath, mode='r', encoding='utf-8', errors='ignore') as file_handler:
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

    def compute_tfidf(self):
        """
        Compute tf idf score fol all words in the documents
        :return:
        """
        wordSet = ()                                  #set of words from all texts
        bowArr = []                                   #arr of bows. each bow is a list of seperated words of each text
        wordD = []                                    #list of dicts. each dic for each text
        tfBow = []                                    # a list of all tf values
        i = 0                                         #index
        tfidfVal = {}                                 #a dict of cod index and its tfidf value
        for doc in docCollection.values():
            bowD = doc.split(" ")                     #split text to words
            wordSet = set(bowD).union(wordSet)        #build set of words
            bowArr.append(bowD)                       #build list of bows
        for bow in bowArr:
            wordDic =(dict.fromkeys(wordSet, 0))      #build dictionary of zeros for each text(bow)
            for word in bow:
                wordDic[word] += 1                    #update number of word of each text i te dict
            tf = Document.computeTf(self, wordDic, len(bow)) #compute tf value for each document
            tfBow.append(tf)
            wordD.append(wordDic)                     #build list of dicts
        idfs = Document.computeIDF(self, wordD)       #compute idf value

        """cumpute of tfidf= tf*idf"""
        for t in tfBow:
            tfidf = {}
            for word, val in t.items():
                tfidf[word] = val*idfs[word]  #val= Tf value, idfs[word]= idf value
            tfidfVal[i] = tfidf
            i = i+1
        return tfidfVal

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
            tfDict[word] = count/float(bowCount)
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
            idfDict[word] = math.log10(N/float(val))
        return idfDict



if __name__ == "__main__":
    config = configuration.config().setup()
    docCollection = {}  # all documents in one document as a dictionary
    Doc = ["C:\\Users\\Aviram Kounio\\Google Drive\\סמסטר ח\\פרויקט חלק ב\\Text\\a.txt",
           "C:\\Users\\Aviram Kounio\\Google Drive\\סמסטר ח\\פרויקט חלק ב\\Text\\b.txt"]
        #  "C:\\Users\\Aviram Kounio\\Google Drive\\סמסטר ח\\פרויקט חלק ב\\Text\\c.txt"


    for d in Doc:  # d = document path
        Doc1 = Document(d)
        docCollection[Doc1.get_docID()] = Doc1.getText(d)[1:]  # build dic of documents

   # print(docCollection.items())

    #model = Word2VecWrapper.Model(config, filepath="C:\\Users\\Aviram Kounio\\Google Drive\\סמסטר ח\\פרויקט חלק ב\\Text\\wiki.he.vec")

    #model.build_model()
    #set1 = s1.split(" ")
    #for word in set1:
     #   if(model.exist_in_vocab(word)):
      #      print(word)
       #     print("-----")
        #    print(str(model.get_vector(word)))
    h = 1
    t = Document.compute_tfidf(docCollection)
    #for y in t.items():
        #print(y)


