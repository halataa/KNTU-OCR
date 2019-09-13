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
from word_detection import *

#%%
miniModel = model.get_Model(training=False)
miniModel.load_weights('models\\bestValModel.h5')

with open("resources\\moinMN.txt", 'rb') as moinFile:
    moin = pickle.load(moinFile)

with open('resources\\alphabetList.txt', 'rb',) as file:
    alphabetList = pickle.load(file)
alphabetList.append('-')

alphabetDict=json.load(open('resources\\alphabetDict.txt'))
#%%

def single_test(image_path_or_array):
    if isinstance(image_path_or_array, str):
        image = Image.open(image_path_or_array)
        image = image.convert(mode='L')
        testArray = np.asarray(image.transpose(Image.FLIP_LEFT_RIGHT))
        # testArray = testArray/255.
        SC = MinMaxScaler()
        testScaled = SC.fit_transform(testArray)
        testScaled = testScaled.T
        testScaled = np.expand_dims(testScaled, axis=-1)
        testScaled = np.expand_dims(testScaled, axis=0)
        testScaled = [testScaled]
    else:
        testScaled = np.fliplr(image_path_or_array)
        # SC = MinMaxScaler()
        # testScaled = SC.fit_transform(testScaled)
        testScaled = testScaled/255.
        testScaled = testScaled.T
        testScaled = np.expand_dims(testScaled, axis=-1)
        testScaled = np.expand_dims(testScaled, axis=0)
    return testScaled

def raw_CTC(preds):

    raw_preds = []
    for pred in preds:
        raw_pred = []
        for t in pred:
            let_index = np.argmax(t)
            let = alphabetList[let_index]
            raw_pred.append(let)
        raw_preds.append(raw_pred)
    return raw_preds



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


def decode_CTC(raw_CTC):
    decoded = []
    for item in raw_CTC:
        finalList = []
        word = ''
        for i in range(1, len(item)-1):
            if item[i] == item[i+1] and item[i] != item[i-1]:
                finalList.append(item[i])
            if item[i] != item[i+1] and item[i] != item[i-1]:
                finalList.append(item[i])
        if item[-1] != item[-2]:
            finalList.append(item[-1])
        for item in finalList:
            if item != '-':
                word += item
        decoded.append(word)
    return decoded


def dict_assist(predictions,dictionary_influence=1.05,ret_list=False,pred_per_word = 5):
    assisteds = []
    for prediction in predictions:
        data = prediction.squeeze()
        data = np.where(data == 1, 0.999, data)
        result = beam_search_decoder(data, pred_per_word)
        finalList = []
        probs = []
        words = []
        for list_and_prob in result:
            predList =list_and_prob[0]
            prob = -log10(list_and_prob[1])
            probs.append(prob)
            wordList = []
            for item in predList:
                char = alphabetDict[alphabetList[item]]
                wordList.append(char)
            word = decode_CTC([wordList])
            words.append(word[0])
        probs = list(map(lambda x: x/max(probs), probs))
        for i in range(len(words)):
            finalList.append([words[i], probs[i]])


        for List in finalList:
            if List[0] in moin:
                List[1]=List[1]*dictionary_influence
        finalList.sort(key=operator.itemgetter(1),reverse=True)
        prediction = finalList[0][0]

        if ret_list:
            assisteds.append(finalList)
        else:
            assisteds.append(prediction)

    return assisteds 

def OCR(images,assisted=False):
    scaled_images = []
    for image in images:
        scaled_image = single_test(image)
        scaled_images.append(scaled_image[0])
    scaled_images = np.array(scaled_images)
    preds = miniModel.predict(scaled_images)
    if assisted:
        words = dict_assist(preds)
        line = ' '.join(reversed(words))
    else:
        raw_preds = raw_CTC(preds)
        words = decode_CTC(raw_preds)
        line = ' '.join(reversed(words))
    return line


#%%

g = 'D:\\line\\koori.jpg'
lines = detect_lines(g)
words = get_words(lines)
pad = padded_words(words[8])
simple = OCR(pad)
# assisted = OCR(pad,assisted=True)
print(simple)
# print(assisted)

#%%
