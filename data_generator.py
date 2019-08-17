#%%
from PIL import Image
import os
import parameters as p
import labelize as lb
import numpy as np
import re
import random
from sklearn.preprocessing import MinMaxScaler



class TextImageGenerator:
    def __init__(self, img_dirpath, img_w, img_h,
                 batch_size, downsample_factor, max_text_len=141):
        self.img_h = img_h
        self.img_w = img_w
        self.batch_size = batch_size
        self.max_text_len = max_text_len
        self.downsample_factor = downsample_factor
        self.img_dirpath = img_dirpath                  # image dir path
        self.img_dir = os.listdir(self.img_dirpath)     # images list
        self.n = len(self.img_dir)//2                      # number of images
        self.indexes = list(range(self.n))
        self.cur_index = 0
        self.imgs = []
        self.texts = []
        


    ## samples의 이미지 목록들을 opencv로 읽어 저장하기, texts에는 label 저장
    def build_data(self):
        print(self.n, " Image Loading start...")
        imageList = []
        txtList = []
        for file in self.img_dir:
            if file[-1] == 'g':
                imageList.append(file)
            else:
                txtList.append(file)
        for i in range(len(imageList)):
            imageArrayCopy = np.asarray(Image.open(self.img_dirpath+imageList[i]).transpose(Image.FLIP_LEFT_RIGHT))
            imageArray = np.copy(imageArrayCopy)
            SC = MinMaxScaler()
            SC.fit(imageArray)
            imageArray = SC.transform(imageArray)
            self.imgs.append(imageArray)
            with open(self.img_dirpath+txtList[i], 'r' , encoding='utf8') as txtFile:
                self.texts.append(txtFile.readline().strip())
        print(self.n, " Image Loading finish...")

    def next_sample(self):      ## index max -> 0 으로 만들기
        self.cur_index += 1
        if self.cur_index >= self.n:
            self.cur_index = 0
            random.shuffle(self.indexes)
        return self.imgs[self.indexes[self.cur_index]], self.texts[self.indexes[self.cur_index]]
    
    def data_checker(self,image,text): # for checking data structure
        X_data = np.ones([self.img_w, self.img_h, 1])     # (bs, 128, 64, 1)
        Y_data = np.ones([self.max_text_len])             # (bs, 9)
        input_length = np.ones((self.batch_size, 1)) * (self.img_w // self.downsample_factor - 2)  # (bs, 1)
        label_length = np.zeros((self.batch_size, 1))           # (bs, 1)
        img = image.T
        img = np.expand_dims(img, -1)
        X_data = img
        Y_data[:len(text)] = lb.labeling(text)
        label_length = len(text)
        return X_data,Y_data,input_length,label_length



    def next_batch(self):      
        while True:
            X_data = np.ones([self.batch_size, self.img_w, self.img_h, 1])     # (bs, 128, 64, 1)
            Y_data = np.ones([self.batch_size, self.max_text_len])             # (bs, 9)
            input_length = np.ones((self.batch_size, 1)) * (self.img_w // self.downsample_factor - 2)  # (bs, 1)
            label_length = np.zeros((self.batch_size, 1))           # (bs, 1)

            for i in range(self.batch_size):
                img, text = self.next_sample()
                img = img.T
                img = np.expand_dims(img, -1)
                X_data[i] = img
                Y_data[i][:len(text)] = lb.labeling(text)
                label_length[i] = len(text)

            
            inputs = {
                'the_input': X_data,  
                'the_labels': Y_data,  
                'input_length': input_length,  
                'label_length': label_length  
            }
            outputs = {'ctc': np.zeros([self.batch_size])}
            yield (inputs, outputs)

#%%
