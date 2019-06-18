
class config(object):
    """
    This class implemented the configparser module.
    For each variable the user can get and set a new value.
    """
    def __init__(self):
        self.logfile = "CTA_Regression.log"
        self.size = "2"
        self.delay = "4"
        self._from = "2"
        self.to = "5"
        self.num_of_words_per_doc = "4"
        self.arch = "Skip-Gram"
        self.training_model = "Softmax"
        self.context_window = "5"
        self.dimension = "300"
        self.text_delimiter = r'\[.*?\]'

    def get(self, section, variable):
        if (section == "GENERAL"):
            return self.get_general_val(variable)
        elif(section == "CHUNKS"):
            return self.get_chunk_val(variable)
        elif (section == "CLUSTER"):
            return self.get_cluster_val(variable)
        elif (section == "TF-IDF"):
            return self.get_tfidf_val(variable)
        elif (section == "Word2Vec"):
            return self.get_word2vec_val(variable)
        else:
            raise Exception("Invalid section")

    def get_general_val(self, variable):
        if (variable == "logfile"):
            return self.logfile
        else:
            raise Exception("Invalid variable")

    def get_chunk_val(self, variable):
        if (variable == "size"):
            return self.size
        elif (variable == "delay"):
            return self.delay
        else:
            raise Exception("Invalid variable")

    def get_cluster_val(self, variable):
        if (variable == "from"):
            return self._from
        elif (variable == "to"):
            return self.to
        else:
            raise Exception("Invalid variable")

    def get_tfidf_val(self, variable):
        if (variable == "num_of_words_per_doc"):
            return self.num_of_words_per_doc
        else:
            raise Exception("Invalid variable")

    def get_word2vec_val(self, variable):
        if (variable == "arch"):
            return self.arch
        elif (variable == "training_model"):
            return self.training_model
        elif (variable == "context_window"):
            return self.context_window
        elif (variable == "dimension"):
            return self.dimension
        elif (variable == "text_delimiter"):
            return self.text_delimiter
        else:
            raise Exception("Invalid variable")

    def set(self, section, variable, value):
        if (section == "GENERAL"):
            self.set_general_val(variable, value)
        elif(section == "CHUNKS"):
            self.set_chunk_val(variable, value)
        elif (section == "CLUSTER"):
            self.set_cluster_val(variable, value)
        elif (section == "TF-IDF"):
            self.set_tfidf_val(variable, value)
        elif (section == "Word2Vec"):
            self.set_word2vec_val(variable, value)
        else:
            raise Exception("Invalid section")

    def set_general_val(self, variable, value):
        if (variable == "logfile"):
            self.logfile = value
        else:
            raise Exception("Invalid variable")

    def set_chunk_val(self, variable, value):
        if (variable == "size"):
            self.size = value
        elif (variable == "delay"):
            self.delay = value
        else:
            raise Exception("Invalid variable")

    def set_cluster_val(self, variable, value):
        if (variable == "from"):
            self._from = value
        elif (variable == "to"):
            self.to = value
        else:
            raise Exception("Invalid variable")

    def set_tfidf_val(self, variable, value):
        if (variable == "num_of_words_per_doc"):
            self.num_of_words_per_doc = value
        else:
            raise Exception("Invalid variable")

    def set_word2vec_val(self, variable, value):
        if (variable == "arch"):
            self.arch = value
        elif (variable == "training_model"):
            self.training_model = value
        elif (variable == "context_window"):
            self.context_window = value
        elif (variable == "dimension"):
            self.dimension = value
        elif (variable == "text_delimiter"):
            self.text_delimiter = value
        else:
            raise Exception("Invalid variable")