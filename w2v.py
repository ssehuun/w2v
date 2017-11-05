# -*- coding: UTF-8 -*-

# Word2Vec embedding

import logging
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
from gensim.models.keyedvectors import KeyedVectors
from konlpy.tag import Kkma
from konlpy.tag import Hannanum
from konlpy.tag import Komoran
from konlpy.tag import Twitter
from konlpy.tag import Mecab
from sklearn.decomposition import PCA
from matplotlib import pyplot


kkma = Kkma()
hannanum = Hannanum()
komoran = Komoran()
twitter = Twitter()
# mecab = Mecab()

# word2vec model parameters
min_count = 5
size = 50
window = 5
iter = 10
sg = 1

filename = "../w2v/101_Economy.txt"
w2vf = "../w2v/token.txt"

def read_data(filename):
    with open(filename, 'r', encoding='utf8') as f:
        data = [line.split('다.') for line in f.read().splitlines()]
        return data


def make_tokenFile(raw_file, w2vf):
    try:
        with open(raw_file, 'r', encoding='utf8') as rf:
            with open(w2vf, 'w', encoding='utf8') as wf:

                for line in rf.readlines():
                    arr_s = line.split('다.')
                    article = ""
                    for s in arr_s:
                        article += " ".join(twitter.nouns(s))
                    article += '\n'
                    wf.write(article)
                    # wf.write(" ".join(twitter.nouns(s))+"\n")

    except Exception as e:
        logging.error('Not file read: ', e)



def word2vec(filepath):
    sentences = LineSentence(filepath)
    model = Word2Vec(sentences, min_count = min_count, size = size, window = window, iter=iter, sg=1)
    print(model)
    # summarize vocabulary
    words = list(model.wv.vocab)

    print(words)
    # save model
    model.wv.save_word2vec_format('model.bin')
    # load model
    new_model = Word2Vec.load('model.bin')
    print(new_model)


    # print(model.wv.most_similar(positive=['창업'], topn=5))
    # print(model.wv.most_similar(negative=['창업'], topn=5))


    #
    # # fit a 2d PCA model to the vectors
    # X = model[model.wv.vocab]
    # pca = PCA(n_components=2)
    # result = pca.fit_transform(X)
    # # create a scatter plot of the projection
    # pyplot.scatter(result[:, 0], result[:, 1])
    # words = list(model.wv.vocab)
    # for i, word in enumerate(words):
    #     pyplot.annotate(word, xy=(result[i, 0], result[i, 1]))
    # pyplot.show()



if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    # make_tokenFile(filename, w2vf)
    word2vec(w2vf)

# making gensim model and training it on sentences
# model = Word2Vec(train_data, min_count = min_count, size = size, window = window, iter=iter, sg=1)
# # learned vocabulary of tokens
# words = list(model.wv.vocab)
# print(words)
#
# model.wv.save_word2vec_format('model.bin')
# model.wv.save_word2vec_format('model.txt', binary=False)
#
# # printing model's vocablury
# print(model.wv.vocab.keys())

# printing vector for 'learning' word





# embed_model = Word2Vec.load("first_model")






'''
embedding_model = Word2Vec.load("first")
embedding_model.wv.similarity('최태원', '회장')
# word_vectors = KeyedVectors.load_word2vec_format('same_field_101.txt', binary=False)
'''




