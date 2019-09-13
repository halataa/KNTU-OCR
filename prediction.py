# %%
from PIL import Image
import numpy as np
import pickle
import model
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
import itertools
import keras.backend as K
from math import log, log10
from numpy import array
from numpy import argmax
import json
import operator


miniModel = model.get_Model(training=False)
miniModel.load_weights('models\\6-11[17-54]__Model\\bestModel.h5')
with open("resources\\moinMN.txt", 'rb') as moinFile:
    moin = pickle.load(moinFile)

with open('resources\\alphabetList.txt', 'rb',) as file:
    alphabetList = pickle.load(file)
alphabetList.append('-')

alphabetDict=json.load(open('resources\\alphabetDict.txt'))


def single_test(imagePath):
    image = Image.open(imagePath)
    image = image.convert(mode='L')
    testArray = np.asarray(image.transpose(Image.FLIP_LEFT_RIGHT))
    SC = MinMaxScaler()
    testScaled = SC.fit_transform(testArray)
    testScaled = testScaled.T
    testScaled = np.expand_dims(testScaled, axis=-1)
    testScaled = np.expand_dims(testScaled, axis=0)
    return testScaled


def predict_with_dic(prediction):
    top_paths = 3
    results = []
    out = prediction
    for i in range(top_paths):
        lables = K.get_value(K.ctc_decode(out, input_length=np.ones(out.shape[0])*out.shape[1],
                                          greedy=False, beam_width=top_paths, top_paths=top_paths)[0][i])[0]
        results.append(lables)
    return results


def beam_search_decoder(data, k):
    sequences = [[list(), 1.0]]
    # walk over each step in sequence
    for row in data:
        all_candidates = list()
        # expand each current candidate
        for i in range(len(sequences)):
            seq, score = sequences[i]
            for j in range(len(row)):
                candidate = [seq + [j], score * -log(row[j])]
                all_candidates.append(candidate)
        # order all candidates by score
        ordered = sorted(all_candidates, key=lambda tup: tup[1])
        # select k best
        sequences = ordered[:k]
    return sequences


def decode_CTC(predList):
    wordList = []
    for item in predList:
        char =alphabetDict[alphabetList[item]]
        wordList.append(char)
        finalList = []
        kalame = ''
    for i in range(1, len(wordList)-1):
        if wordList[i] == wordList[i+1] and wordList[i] != wordList[i-1]:
            finalList.append(wordList[i])
        if wordList[i] != wordList[i+1] and wordList[i] != wordList[i-1]:
            finalList.append(wordList[i])
    if wordList[-1] != wordList[-2]:
        finalList.append(wordList[-1])
    for item in finalList:
        if item != '-':
            kalame += item
    return (kalame)


# %%
def predict (dir='C:\\Users\\Ali\\Documents\\Uni\\Projects\\OCR\\real ocr\\resources\\datasets\\test_dataset\\kntu45.png',photoNumber='21',dictionary_influence=1.2):
    
    testScaled = single_test(dir)
    prediction = miniModel.predict(testScaled)
    # a=predict_with_dic(prediction)
    data = prediction.squeeze()
    data = np.where(data == 1, 0.999, data)
    result = beam_search_decoder(data, 5)
    finalList = []
    probs = []
    words = []
    for list_and_prob in result:
        predList = list_and_prob[0]
        prob = -log10(list_and_prob[1])
        probs.append(prob)
        word = decode_CTC(predList)
        words.append(word)
    probs = list(map(lambda x: x/max(probs), probs))
    for i in range(len(words)):
        finalList.append([words[i], probs[i]])


    for List in finalList:
        if List[0] in moin:
            List[1]=List[1]*dictionary_influence
    finalList.sort(key=operator.itemgetter(1),reverse=True)
    return(finalList[0][0]) 


predict('resources\\for presentation\\cnn images\\kntu789.png')

#%%
testScaled = single_test('resources\\for presentation\\cnn images\\kntu48333.png')
prediction = miniModel.predict(testScaled)