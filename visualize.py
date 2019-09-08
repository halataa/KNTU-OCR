#%%
from keras import backend as K
from keras.models import Model
from model import get_Model
from PIL import Image
import numpy as np
from sklearn.preprocessing import MinMaxScaler
def single_test(imagePath):
    image = Image.open(imagePath)
    image = image.convert(mode='L')
    testArray = np.asarray(image.transpose(Image.FLIP_LEFT_RIGHT))
    SC = MinMaxScaler()
    testScaled = SC.fit_transform(testArray)
    testScaled = testScaled.T
    testScaled = np.expand_dims(testScaled, axis=-1)
    testScaled = np.expand_dims(testScaled, axis=0)
    return testScaled,SC

model = get_Model(False)
model.load_weights('models\\6-11[17-54]__Model\\bestModel.h5')
def ax (layer_name = 'conv1',chanta=64):
    img,sc=single_test('resources\\for presentation\\cnn images\\kntu48333.png')
    intermediate_layer_model = Model(inputs=model.input,outputs=model.get_layer(layer_name).output)
    intermediate_output = intermediate_layer_model.predict(img)
    for number in range (0,chanta):
        array=intermediate_output[0,:,:,number]
        array = array.T
        array = array*255
        array=array.astype('uint8')
        img=Image.fromarray(array,mode='L')
        img=img.transpose(Image.FLIP_LEFT_RIGHT)
        img.save('resources\\for presentation\\cnn images\\%s\\%s %s.jpg' %(layer_name,layer_name, number))

ax('conv5',256)
ax('max1')

#%%from keras.models import Model
from model import get_Model
from keras.utils import plot_model

model = get_Model(False)
plot_model(model, to_file='model.png')

#%%
