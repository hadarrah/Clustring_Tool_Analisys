import logging
from Algorithm.document import Document
from Algorithm.distance_matric import Distance_Matric
from Algorithm.cl import CL
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
        self.Step1()
        top.set_v_stage(self.stage)

        ################## Step 2 ##################
        self.log.info("Step 2: Word2Vec")
        self.stage += 1
        self.Step2()
        top.set_v_stage(self.stage)

        ################## Step 3 ##################
        self.log.info("Step 3: Build Chunks")
        self.stage += 1
        self.Step3()
        top.set_v_stage(self.stage)

        ################## Step 4 ##################
        self.log.info("Step 4: Build Distance Metric")
        self.stage += 1
        self.Step4()
        top.set_v_stage(self.stage)

        ################## Step 5 ##################
        self.log.info("Step 5: PAM")
        self.stage += 1
        self.Step5()
        top.set_v_stage(self.stage)

        ################## Step 6 ##################
        self.log.info("Step 6: Silhouette")
        self.stage += 1
        self.Step6()
        top.set_v_stage(self.stage)

        # for debug
        self.print_result_to_log()


    def get_stage(self):
        return self.stage

    def Step1(self):
        self.docCollection = {}  # all documents in one document as a dictionary
        self.docList = []  # list of Document objects

        # --Creating the Documents collections--#
        for d in self.documents:
            Doc1 = Document(d, self.config)
            self.docCollection[Doc1.get_docID()] = Doc1.getText(d)  # build dic of documents to TF-IDF
            self.docList.append(Doc1)  # build list of document objects to Word2Vec

        # --Creating the Tf-Idf dictionary--#
        self.tfidfDic = Document.compute_tfidf("", self.docCollection)

    def Step2(self):
        if (self.external_vec):
            self.model = Model(self.config, filepath=self.external_vec)
        else:
            self.model = Model(self.config, documents=self.docList)
        self.model.build_model()

    def Step3(self):
        words = []  # list of good words
        wordsCount = 0
        for key in self.tfidfDic.keys():
            print(key)
            text = self.docList[key].get_docText().split()  # getting the doc text by key(=id)
            for value in self.tfidfDic.values():  # each dictionary in Tf-Idf dictionary
                sorted_value = sorted(value.items(),
                                      key=operator.itemgetter(1))  # sorted dictionary by value(=Tf-Idf value)
                sorted_value.reverse()  # inversed sorted dictionary -> max dictionary
                for k, val in sorted_value:
                    if wordsCount < self.num_of_words_per_doc:  # while we don't get the s(=num of words) count
                        if val != 0:  # ignore the words with value 0
                            if self.model.exist_in_vocab(k):
                                words.append(k)  # build list of s highest tf-idf value that in the vocab
                            wordsCount += 1
                wordsCount = 0
            text = ' '.join(
                i for i in text if i in words).split()  # delete from the original text the unnecessary words
            text = text[:self.num_of_words_per_doc]  # resize the list into the correct size
            words = []
            print(text)
            self.docList[key].createChunks(text, self.model, self.config)  # create chunks for each document

    def Step4(self):
        self.matric = Distance_Matric(self.config, self.docList)
        self.matric.build_metric()

    def Step5(self):
        self.clustring_results = CL(self.config, self.matric.get_distance_metric())
        self.clustring_results.generate_clusters()

    def Step6(self):
        self.best_cl, self.clusters_indicator = self.clustring_results.get_best_clustering_result()
        # for each comparable chunk we calculate his cluster and then based on majority votes
        # assign the documents into a specific cluster

        chunks_index = self.matric.get_chunks_index()
        for i in range(0, len(self.matric.get_distance_metric())):
            chunks_index[i].set_cluster(self.clusters_indicator[i])
        for doc in self.docList:
            doc.compute_cluster(len(self.best_cl.get_clusters()))

    def print_result_to_log(self):
        self.log.info("*********REGRESSION SUMMARY*********")
        self.log.info("Number of Documents: " + str(len(self.docList)))
        self.log.info("Number of clusters: " + str(len(self.best_cl.get_clusters())))
        self.log.info("*********Documents and Chunks*********")
        for doc in self.docList:
            print (doc)


if __name__ == "__main__":
    # Unitest
    config = configuration.config().setup()
    main = main(config, "blabla", None)

