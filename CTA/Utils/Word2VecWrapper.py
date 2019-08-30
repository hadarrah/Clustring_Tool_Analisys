from gensim.models import word2vec
from gensim.models import KeyedVectors
from gensim.test.utils import datapath
import logging
import re

class Model(object):
    """
    This class supply a wrapper for word embedding technique based on word2vec module.
    Either instance of the class could be based on external word2vec file:
        model = Model(config, filepath=[*.vec])

    Or creation of new vocabulary based on documents collection:
        documents_collection = []
        model = Model(config, documents=documents_collection)

    Both ways should call to build_model function in order to finish the model setup.
    """
    def __init__(self, config, filepath=None, documents=[]):
        self.architecture = 1 if (config.get("Word2Vec", "arch") == "Skip-Gram") else 0
        self.training_model = 1 if (config.get("Word2Vec", "training_model") == "Softmax") else 0
        self.window = int(config.get("Word2Vec", "context_window"))
        self.dimension = int(config.get("Word2Vec", "dimension"))
        self.delimiter = config.get("Word2Vec", "text_delimiter")
        self.file_path = filepath
        self.sentences = []
        self.vectors = None
        self.log = logging.getLogger(__name__ + "." + __class__.__name__)
        if (documents):
            self.set_sentences(documents)

    def build_model(self):
        """
        Build the word2vec model.
        Either with external word embedding or based on document collection.
        :return:
        """
        self.log.info("Build Model")
        if (self.file_path):
            self.word_vectors = KeyedVectors.load_word2vec_format(datapath(self.file_path), limit=50000)
        else:
            self.model = word2vec.Word2Vec(sentences=self.sentences, size=self.dimension, sg=self.architecture,
                                  hs=self.training_model, window=self.window, min_count=1)
            self.log.info(self.model)
            self.model.train(self.sentences, total_examples=self.model.corpus_count, epochs=self.model.iter)
            self.word_vectors = self.model.wv

    def set_sentences(self, documents):
        """
        This function parse and build list of list which represent words in sentences in the entire document collection.
        example:
            [['You', 'love', 'me'], ['The', 'dog', 'looks', 'nice']]

        :param documents: list of paths to the document collection
        :return:
        """
        self.log.info("Set Sentences")
        for doc in documents:
            text = doc.get_docText()
            text = re.sub(r'[,:;]', '', text)                              # remove special chars
            text = re.sub(r'\s.?\s', '', text)                              # remove words with length 1
            sen_list = re.split(self.delimiter, text)                       # get sentences by delimiter
            word_sen_list = [lst.strip().split(' ') for lst in sen_list]    # separate words in sentences
            self.sentences.extend(sen for sen in word_sen_list)


    def get_vector(self, word):
        """
        Get the vector representation of the word.
        :param word: word string
        :return: if exist -> word vector, otherwise -1
        """
        try:
            vec = self.word_vectors[word]
        except Exception as e:
            self.log.error(str(e))
            vec = -1
        return vec

    def exist_in_vocab(self, word):
        return (word in self.word_vectors)

