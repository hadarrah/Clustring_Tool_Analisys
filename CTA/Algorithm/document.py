from gensim.models import word2vec
from gensim.models import KeyedVectors
from gensim.test.utils import datapath
from Utils import logger
from Utils import configuration
import logging
import re
from numpy import array


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
        Set the number of documents
        :return:
        """
        self.docID = Document.ID + 1

    def get_docID(self):
        """
        Get the number of documents
        :return:
         """
        return self.docID

    def set_ID(self):
        """
        Set the number of documents
        :return:
        """
        Document.ID = Document.ID + 1

    def get_ID(self):
        """
        Get the number of documents
        :return:
         """
        return Document.ID


if __name__ == "__main__":
    docCollection = {}  # all documents in one document as a dictionary
    Doc = ["C:\\Users\\Aviram Kounio\\Google Drive\\סמסטר ח\\פרויקט חלק ב\\Text\\a.txt",
           "C:\\Users\\Aviram Kounio\\Google Drive\\סמסטר ח\\פרויקט חלק ב\\Text\\b.txt"]

    for d in Doc:  # d = document path
        Doc1 = Document(d)
        docCollection[Doc1.get_docID()] = Doc1.getText(d)[1:]  # build dic of documents

    print(docCollection.items())

# Doc = Document("C:\\Users\\Aviram Kounio\\Google Drive\\סמסטר ח\\פרויקט חלק ב\\Text\\Yiov_chapter_A.txt")
# Doc1 = Document("C:\\Users\\Aviram Kounio\\Google Drive\\סמסטר ח\\פרויקט חלק ב\\Text\\Bamidbar_chapter_B.txt")


# print(Doc.docText)
# print("---------------")
#  print(Doc1.docText)
# print("---------------")
# print(Document.get_docCllection(Document.docCollection))
