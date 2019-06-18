import operator


def Filter(tfidfDic, num_of_words_per_doc, model, docList):
    words = {}  # dic of highest words in all documents (key= word, value= TfIdf value)
    wordsCount = 0
    totalWordsForChunks = []
    for value in tfidfDic.values():  # each dictionary in Tf-Idf dictionary
        sorted_value = sorted(value.items(),
                              key=operator.itemgetter(1))  # sorted dictionary by value(=Tf-Idf value)
        sorted_value.reverse()  # inversed sorted dictionary -> max dictionary
        for k, val in sorted_value:
            if wordsCount < num_of_words_per_doc:  # while we did'nt get the num of words' count
                if val != 0:  # ignore the words with value 0
                    if model.exist_in_vocab(k):
                        words.update({k: val})  # update a total dictionary of all highest words from all documents
                        wordsCount += 1
        wordsCount = 0

    sorted_dic = sorted(words.items(),
                        key=operator.itemgetter(1))  # sort the 'all highest word from all documents' dic
    sorted_dic.reverse()  # inversed sorted dictionary -> max dictionary

    counter = 0
    for k, val in sorted_dic:  # choose the highest words from all documents according to 'num_of_words_per_doc'
        if counter < num_of_words_per_doc:
            totalWordsForChunks.append(k)
            counter += 1


    return totalWordsForChunks
