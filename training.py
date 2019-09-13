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
WEIGHT_DIR = 'G:\\users\\Amir\\6\\models\\6-11[17-54]__Model\\bestModel.h5'

if LOADING == 1:
    model.load_weights(WEIGHT_DIR)


# Model description and training

now = jdatetime.datetime.today()
model_folder_name = '%s-%s[%s-%s]__Model'%(now.month,now.day,now.hour,now.minute)
os.mkdir('models\\%s'%model_folder_name)

info=input('enter train note:  ')
with open ('models\\%s\\info.txt'%model_folder_name,'w' , encoding='utf8') as file:
    file.write(info)

train_file_path = 'resources\\datasets\\new_pun\\train\\'
train_gen = data_generator.TextImageGenerator(train_file_path,p.img_w,p.img_h,p.batch_size,p.downsample_factor,max_text_len=p.max_text_len)
train_gen.build_data()

val_file_path = 'resources\\datasets\\new_pun\\valid\\'
val_gen = data_generator.TextImageGenerator(val_file_path,p.img_w,p.img_h,p.val_batch_size,p.downsample_factor,max_text_len=p.max_text_len)
val_gen.build_data()

ada = Adadelta()
adam =Adam()
early_stop = EarlyStopping(monitor='loss', min_delta=0.001, patience=4, mode='min', verbose=1)
checkpoint1 = ModelCheckpoint(filepath='models\\%s\\bestValModel.h5'%model_folder_name, monitor='val_loss', verbose=1, mode='min', period=1,save_best_only=True,save_weights_only=True)
checkpoint2 = ModelCheckpoint(filepath='models\\%s\\bestAccModel.h5'%model_folder_name, monitor='val_acc', verbose=1, mode='max', period=1,save_best_only=True,save_weights_only=True)
# the loss calc occurs elsewhere, so use a dummy lambda func for the loss
model.compile(loss={'ctc': lambda y_true, y_pred: y_pred}, optimizer=adam,metrics=['accuracy'])
model.summary()
# captures output of softmax so we can decode the output during visualization
history = model.fit_generator(generator=train_gen.next_batch(),
                    steps_per_epoch=int(train_gen.n / train_gen.batch_size),
                    epochs=EPOCHS,
                    validation_data=val_gen.next_batch(),
                    validation_steps=int(val_gen.n / val_gen.batch_size),verbose=1,callbacks=[checkpoint1,checkpoint2])
model.save_weights('models\\%s\\lastEpoch.h5'%model_folder_name)
loss_history = history.history["loss"]
val_loss_history = history.history["val_loss"]
numpy_loss_history = np.array(loss_history)
numpy_val_loss_history = np.array(val_loss_history)
np.savetxt("models\\%s\\loss_history.txt"%model_folder_name, numpy_loss_history, delimiter=",")
np.savetxt("models\\%s\\val_loss_history.txt"%model_folder_name, numpy_val_loss_history, delimiter=",")

#%%
