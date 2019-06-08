def compute_tfidf(docCollection):
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
            wordDic[word] += 1  # update number of word of each text i to dict
        tf = computeTf(wordDic, len(bow))  # compute tf value for each document
        tfBow.append(tf)
        wordD.append(wordDic)  # build list of dicts
    idfs = computeIDF(wordD)  # compute idf value

    """cumpute of tfidf= tf*idf"""
    for t in tfBow:
        tfidf = {}
        for word, val in t.items():
            tfidf[word] = val * idfs[word]  # val= Tf value, idfs[word]= idf value
        tfidfVal[i] = tfidf
        i = i + 1
    return tfidfVal  # return dic: key=word, value= tf idf value


def computeTf( wordDict, len):
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


def computeIDF(documents):
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