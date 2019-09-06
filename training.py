#%%
from keras import backend as K
from keras.optimizers import Adadelta,Adam
from keras.callbacks import EarlyStopping, ModelCheckpoint
import data_generator
import model
import parameters as p
import numpy as np
import os
import jdatetime

K.set_learning_phase(0)
model = model.get_Model(training=True)

EPOCHS = 150

# load weight from previous trainings
LOADING = 0
WEIGHT_DIR = 'models\\6-2[18-22]__Model\\bestModel.h5'

if LOADING == 1:
    model.load_weights(WEIGHT_DIR)


# Model description and training

train_file_path = 'resources\\mainDataset\\smallTrain\\'
train_gen = data_generator.TextImageGenerator(train_file_path,720,32,16,4)
train_gen.build_data()

val_file_path = 'resources\\mainDataset\\smallValid\\'
val_gen = data_generator.TextImageGenerator(val_file_path,720,32,16,4)
val_gen.build_data()

ada = Adadelta()
adam =Adam()
early_stop = EarlyStopping(monitor='loss', min_delta=0.001, patience=4, mode='min', verbose=1)
checkpoint = ModelCheckpoint(filepath='models\\%s\\bestModel.h5'%model_folder_name, monitor='val_loss', verbose=1, mode='min', period=1,save_best_only=True,save_weights_only=True)
# the loss calc occurs elsewhere, so use a dummy lambda func for the loss
model.compile(loss={'ctc': lambda y_true, y_pred: y_pred}, optimizer=ada)
model.summary()
# captures output of softmax so we can decode the output during visualization
history = model.fit_generator(generator=train_gen.next_batch(),
                    steps_per_epoch=int(train_gen.n / train_gen.batch_size),
                    epochs=100,
                    validation_data=val_gen.next_batch(),
                    validation_steps=int(val_gen.n / val_gen.batch_size),verbose=1)
model.save('D:\\UNIVERSITY\\BACHELOR PROJECT\\model\\model1.h5')
#%%
