from gensim.models import word2vec
from gensim.models import KeyedVectors
from gensim.test.utils import datapath


class Model(object):

    def __init__(self, config, filepath=None, documents=None):
        self.architecture = 1 if (config.get("Word2Vec", "arch") == "Skip-Gram") else 0
        self.training_model = 1 if (config.get("Word2Vec", "training_model") == "Hierarchical Softmax") else 0
        self.window = config.get("Word2Vec", "context_window")
        self.dimension = config.get("Word2Vec", "dimension")
        self.file_path = filepath
        self.sentenaces = []
        self.vectors = None
        if (documents):
            self.set_sentenaces(documents)

    def build_model(self):
        if (self.file_path):
            self.word_vectors = KeyedVectors.load_word2vec_format(datapath(self.file_path), binary=True)
        else:
            self.model = word2vec(sentences=self.sentences, size=self.dimension, sg=self.architecture,
                                  hs=self.training_model, window=self.window)
            self.model.train(self.sentences, total_examples=self.model.corpus_count, epochs=self.model.iter)
            self.word_vectors = self.model.wv

    def set_sentenaces(self, documents):
        for doc in documents:
            doc_sentences = word2vec.LineSentence(datapath(doc))
            self.sentences.extend(doc_sentences)

    def get_vector(self, word):
        return self.word_vectors[word]