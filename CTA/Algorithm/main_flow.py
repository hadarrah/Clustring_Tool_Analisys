import logging
from Algorithm.document import Document
from Utils import logger
from Algorithm.chunk import Chunk
from Utils import configuration
from Utils.Word2VecWrapper import Model
import operator


class main(object):

    def __init__(self, config, documents, external_vec):
        self.config = config
        self.documents = (documents)
        self.num_of_words_per_doc = int(config.get("TF-IDF", "num_of_words_per_doc"))
        self.external_vec = external_vec
        self.stage = 1
        self.log = logging.getLogger(__name__ + "." + __class__.__name__)
        self.log = logger.setup()
        #self.log = logger.add_log_file(self.log, config)

    def run(self, top):
        self.log.info("NEW REGRESSION IS STARTING!")

        ################## Step 1 ##################
        self.log.info("Step 1: Get Texts")
        top.set_v_stage(self.stage)
        docCollection = {}  # all documents in one document as a dictionary
        docList = []  # list of Document objects

        #--Creating the Documents collections--#
        for d in self.documents:
            Doc1 = Document(d, self.config)
            docCollection[Doc1.get_docID()] = Doc1.getText(d)  # build dic of documents to TF-IDF
            docList.append(Doc1)  # build list of document objects to Word2Vec

        #--Creating the Tf-Idf dictionary--#
        tfidfDic = Document.compute_tfidf("" ,docCollection)

        ################## Step 2 ##################
        self.log.info("Step 2: Word2Vec")
        self.stage += 1

        if (self.external_vec):
            model = Model(self.config, filepath=self.external_vec)
        else:
            model = Model(self.config, documents=self.Documents_Collection)
        model.build_model()

        top.set_v_stage(self.stage)


        ################## Step 3 ##################
        self.log.info("Step 3: Build Chunks")
        self.stage += 1
        top.set_v_stage(self.stage)
        words = []  # list of good words
        wordsCount = 0
        for key in tfidfDic.keys():
            print(key)
            text = docList[key].get_docText().split()  # getting the doc text by key(=id)
            for value in tfidfDic.values():  # each dictionary in Tf-Idf dictionary
                sorted_value = sorted(value.items(),key=operator.itemgetter(1))  # sorted dictionary by value(=Tf-Idf value)
                sorted_value.reverse()  # inversed sorted dictionary -> max dictionary
                for k, val in sorted_value:
                    if wordsCount < self.num_of_words_per_doc:  # while we don't get the s(=num of words) count
                        if val != 0:  # ignore the words with value 0
                            if model.exist_in_vocab(k):
                                words.append(k)  # build list of s highest tf-idf value that in the vocab
                            wordsCount += 1
                wordsCount = 0
            text = ' '.join(i for i in text if i in words).split()  # delete from the original text the unnecessary words
            text = text[:self.num_of_words_per_doc]                 # resize the list into the correct size
            words = []
            print(text)
            docList[key].createChunks(text,model,self.config)       # create chunks for each document




        ################## Step 4 ##################
        self.log.info("Step 4: Build Distance Metric")
        self.stage += 1
        #raise Exception("fail in stage 4")  # example for raising exception
        top.set_v_stage(self.stage)


        ################## Step 5 ##################
        self.log.info("Step 5: PAM")
        self.stage += 1
        top.set_v_stage(self.stage)


        ################## Step 6 ##################
        self.log.info("Step 6: Silhouette")
        self.stage += 1
        top.set_v_stage(self.stage)


    def get_stage(self):
        return self.stage


if __name__ == "__main__":
    # Unitest
    config = configuration.config().setup()
    main = main(config, "blabla", None)

