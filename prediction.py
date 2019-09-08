#%%
from PIL import Image
import numpy as np
import pickle
import model
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
import itertools
import keras.backend as K

#%%
miniModel = model.get_Model(training=False)
miniModel.load_weights('models\\6-11[17-54]__Model\\bestModel.h5')

#%%
with open('resources\\alphabetList.txt','rb') as file:
    alphabetList = pickle.load(file)
#%%
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

def pred_list(rawPred):
    labels = list()
    labels.extend(alphabetList)
    labels.append('-')
    predList = list()
    rawPred = np.squeeze(rawPred)
    for i in range(rawPred.shape[0]):
        predIndex = np.argmax(rawPred[i])
        predList.append(labels[predIndex])
    return predList

def decode_label(out):
    # out : (1, 32, 42)
    out_best = list(np.argmax(out[0, 2:], axis=1))  # get max index -> len = 32
    out_best = [k for k, g in itertools.groupby(out_best)]  # remove overlap value
    outstr = ''
    for i in out_best:
        if i < len(alphabetList):
            outstr += alphabetList[i]
    return outstr

def decode_CTC(predList):
    finalList = list()
    kalame=''
    finalList.append(predList[0])
    for i in range(1,len(predList)-1):
        if predList[i] == predList[i+1] and predList[i] != predList[i-1]:
            finalList.append(predList[i])
        if predList[i] != predList[i+1] and predList[i] != predList[i-1]:
            finalList.append(predList[i])
    if predList[-1] != predList[-2]:
        finalList.append(predList[-1])
    for item in finalList:
        if item !='-':
            kalame+=item
    return kalame


def decode_predict_ctc(out, top_paths = 1):
    results = []
    beam_width = 5
    if beam_width < top_paths:
      beam_width = top_paths
    for i in range(top_paths):
      lables = K.get_value(K.ctc_decode(out, input_length=np.ones(out.shape[0])*out.shape[1],
                           greedy=False, beam_width=beam_width, top_paths=top_paths)[0][i])[0]
      results.append(lables)
    return results
#%%
testScaled = single_test('resources\\circle.png')
prediction = miniModel.predict(testScaled)
output=decode_predict_ctc(prediction)
predList = pred_list(prediction)
decode_CTC(predList)

#%%
