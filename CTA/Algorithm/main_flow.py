import logging
from Algorithm.document import Document
from Algorithm.distance_matric import Distance_Matric
from Algorithm.cl import CL
from Algorithm.statistical_data import Statistical_Data
from Utils.Word2VecWrapper import Model
from Utils import Filtering
from Utils import tfidf
import multiprocessing
from multiprocessing.dummy import Pool as ThreadPool

class main(object):

    def __init__(self, config, documents, external_vec):
        self.config = config
        self.documents = (documents)
        self.num_of_words_per_doc = int(config.get("TF-IDF", "num_of_words_per_doc"))
        self.external_vec = external_vec
        self.stage = 1
        self.log = logging.getLogger(__name__ + "." + __class__.__name__)
        self.build_chunks = build_chunks

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

        ################## Step 7 ##################
        self.log.info("Step 7: Statistical Data")
        self.stage += 1
        self.Step7()
        top.set_v_stage(self.stage)

        # for debug
        self.print_result_to_log()

    def get_stage(self):
        return self.stage

    def get_data(self):
        return self.data

    def Step1(self):
        """
        Get and insert texts files into document object.
        :return:
        """
        self.docCollection = {}  # all documents in one document as a dictionary
        self.docList = []  # list of Document objects

        i = 0
        # --Creating the Documents collections--#
        for d in self.documents:
            Doc1 = Document(d, self.config, i)
            if Doc1.getText(d) == '':
                raise Exception("The text file '{}' is empty! Please load a new one.".format(d))
            else:
                self.docCollection[Doc1.get_docID()] = Doc1.getText(d)  # build dic of documents to TF-IDF
                self.docList.append(Doc1)  # build list of document objects to Word2Vec
                i += 1
        # --Creating the Tf-Idf dictionary--#
        self.tfidfDic = tfidf.compute_tfidf(self.docCollection)

    def Step2(self):
        """
        Create the word2vec model.
        :return:
        """
        if (self.external_vec):
            self.model = Model(self.config, filepath=self.external_vec)
            self.log.info("Using an external word embedding file")
        else:
            self.log.info("Creating a word embedding file")
            self.model = Model(self.config, documents=self.docList)
        self.model.build_model()

    def Step3(self):
        """
        Build and create chunks based on TF-IDF score.
        :return:
        """
        totalWordsForChunks = Filtering.Filter(self.tfidfDic, self.num_of_words_per_doc, self.model, self.docList)
        self.max_chunks_in_doc = 0

        num_of_cpu = int(multiprocessing.cpu_count())

        # prepare arguments
        updates_in_parallel = []
        for doc in self.docList:
            updates_in_parallel.append({"doc": doc, "model": self.model, "config": self.config, "totalWordsForChunks": totalWordsForChunks})

        # create pool
        pool = ThreadPool(num_of_cpu)
        results = pool.map(self.build_chunks, updates_in_parallel)

        # close the pool and wait for the work to finish
        pool.close()
        pool.join()

        self.max_chunks_in_doc = max(results)

    def Step4(self):
        """
        Build the distance metric.
        :return:
        """
        self.matric = Distance_Matric(self.config, self.docList)
        self.matric.build_metric()

    def Step5(self):
        """
        Generate the clustring results in range[from, to]
        :return:
        """
        self.clustering_results = CL(self.config, self.matric.get_distance_metric())
        self.clustering_results.generate_clusters()

    def Step6(self):
        """
        Get and set the best clustering result base on silhouette algorithm and then assign the chunks and
        document according to the best result
        :return:
        """
        self.best_cl, self.clusters_indicator, self.silhouette_width = self.clustering_results.get_best_clustering_result()
        # for each comparable chunk we calculate his cluster and then based on majority votes
        # assign the documents into a specific cluster

        chunks_index = self.matric.get_chunks_index()
        for i in range(0, len(self.matric.get_distance_metric())):
            chunks_index[i].set_cluster(self.clusters_indicator[i])
        for doc in self.docList:
            doc.compute_cluster(len(self.best_cl.get_clusters()))

    def Step7(self):
        """
        Analyze the statistical data from last regression.
        :return:
        """
        self.data = Statistical_Data(self.config, self.docList, len(self.best_cl.get_clusters()), self.silhouette_width,
                                     self.max_chunks_in_doc)
        self.data.analyze_data()

    def print_result_to_log(self):
        self.log.info("*********REGRESSION SUMMARY*********")
        self.log.info("Number of Documents: " + str(len(self.docList)))
        self.log.info("Number of clusters: " + str(len(self.best_cl.get_clusters())))
        self.log.info("*********Documents and Chunks*********")
        for doc in self.docList:
            self.log.info(doc)


def build_chunks(args_dict):
    doc = args_dict["doc"]
    model = args_dict["model"]
    config = args_dict["config"]
    totalWordsForChunks = args_dict["totalWordsForChunks"]

    unfiltered_text = doc.get_docText().split()  # getting the doc text by key(=id)
    text = [i for i in unfiltered_text if
            i in totalWordsForChunks]  # delete from the original text the unnecessary words
    doc.createChunks(text, model, config)  # create chunks for each document
    chunks_in_doc = len(doc.get_chunks())
    if len(doc.get_comparable_chunks()) == 0:  # none chunks exception
        raise Exception("There are not comparable chunks in several documents. Please select different "
                        "parameters in TF-IDF and Chunks sections")
    return chunks_in_doc