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
    testScaled = testArray*255
    testScaled = testScaled.T
    testScaled = np.expand_dims(testScaled, axis=-1)
    testScaled = np.expand_dims(testScaled, axis=0)
    return testScaled

model = get_Model(False)
model.load_weights('models\\6-21[12-28]__Model\\bestValModel.h5')
def ax (layer_name = 'conv1',chanta=64):
    img=single_test('resources\\for presentation\\cnn images\\kntu48333.png')
    intermediate_layer_model = Model(inputs=model.input,outputs=model.get_layer(layer_name).output)
    intermediate_output = intermediate_layer_model.predict(img)
    for number in range (0,chanta):
        array=intermediate_output[0,:,:,number]
        array=array.astype('uint8')
        array=array.T
        img=Image.fromarray(array,mode='L')
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
        img.save('resources\\for presentation\\cnn images\\%s\\%s %s.jpg' %(layer_name,layer_name, number))

ax('conv2')

#%%from keras.models import Model
from model import get_Model
from keras.utils import plot_model

model = get_Model(False)
plot_model(model, to_file='model.png')

#%%
list1=[]
list2=[]
import pickle
import matplotlib.pyplot as plt
import matplotlib.style as style
with open ('models\\6-20[21-25]__Model\\loss_history.txt','r') as file:
    for line in file:
        amir=line.strip()
        list1.append(float(amir))
with open ('models\\6-20[21-25]__Model\\val_loss_history.txt','r') as file:
    for line in file:
        amir2=line.strip()
        list2.append(float(amir2))
style.available

style.use('seaborn')        
plt.plot(list1,label='Train Loss')
plt.plot(list2,label='Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('')
plt.legend()
plt.show()

#%%
