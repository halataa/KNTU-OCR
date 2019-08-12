#%%
from keras import backend as K
from keras.optimizers import Adadelta
from keras.callbacks import EarlyStopping, ModelCheckpoint
from KNTU_OCR import data_generator
from KNTU_OCR import model
from KNTU_OCR import parameters as p
K.set_learning_phase(0)

# # Model description and training

model = model.get_Model(training=True)

train_file_path = 'C:\\Users\\Ali\\Documents\\Uni\\Projects\\OCR\\resources\\data base\\train data\\'
train_gen = data_generator.TextImageGenerator(train_file_path,720,32,16,4)
train_gen.build_data()

val_file_path = 'C:\\Users\\Ali\\Documents\\Uni\\Projects\\OCR\\resources\\data base\\val data\\'
val_gen = data_generator.TextImageGenerator(val_file_path,720,32,16,4)
val_gen.build_data()


ada = Adadelta()

early_stop = EarlyStopping(monitor='loss', min_delta=0.001, patience=4, mode='min', verbose=1)
#checkpoint = ModelCheckpoint(filepath='LSTM+BN5--{epoch:02d}--{val_loss:.3f}.hdf5', monitor='loss', verbose=1, mode='min', period=1)
# the loss calc occurs elsewhere, so use a dummy lambda func for the loss
model.compile(loss={'ctc': lambda y_true, y_pred: y_pred}, optimizer=ada)

# captures output of softmax so we can decode the output during visualization
model.fit_generator(generator=train_gen.next_batch(),
                    steps_per_epoch=int(train_gen.n / train_gen.batch_size),
                    epochs=30,
                    validation_data=val_gen.next_batch(),
                    validation_steps=int(val_gen.n / val_gen.batch_size))

#%%
