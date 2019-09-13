# %% import moin.text
from bidi.algorithm import get_display
from PIL import ImageDraw
from PIL import Image
from PIL import ImageFont
from scipy import ndimage
import sys
import arabic_reshaper
import numpy as np
import random
import pickle
import glob
import re
import os

with open("resources\\moinMN.txt", 'rb') as moinFile:
    moin = pickle.load(moinFile)

BASE_IMAGE_SIZE = (100, 32)
# %% font select


def font_select(font_number):
    font_list = []
    for file in glob.glob('resources\\fonts\\*.ttf'):
        font_name = re.findall(r'fonts\\(B .+)\.', file)  # just B series
        font_name = str(font_name[0])
        font_list.append(font_name)
    font_name = font_list[font_number]
    font_dir = 'resources\\fonts\\%s.ttf' % font_name
    return(font_dir, font_name)


# %% create image file function

def create_image(text, font_dir):
    font = ImageFont.truetype(font_dir, 50)
    img = Image.new('L', (1000, 300), color='white')
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    draw = ImageDraw.Draw(img)
    draw.text((0, 150), bidi_text, 'black', font=font)
    return (img)


def crop_image(img,tr=255):
    image_data = np.asarray(img)
    non_empty_columns = np.where(image_data.min(axis=0) < tr)[0]
    non_empty_rows = np.where(image_data.min(axis=1) < tr)[0]
    cropBox = (min(non_empty_rows), max(non_empty_rows),
               min(non_empty_columns), max(non_empty_columns))
    image_data_new = image_data[cropBox[0]
        :cropBox[1]+1, cropBox[2]:cropBox[3]+1]
    new_image = Image.fromarray(image_data_new)
    return new_image


def resize_image(img, target_height):
    width, height = img.size
    reshape_factor = target_height/height
    new_width, new_height = int(
        np.ceil(reshape_factor*width)), int(np.ceil(reshape_factor*height))
    resized_image = img.resize((new_width, new_height))
    return resized_image


def padding_image(img, max_len, pad_value=255):
    image_array = np.copy(np.asarray(img))
    assert image_array.shape[1] < max_len, 'image lenght is more than max_len'
    extraLen = max_len-image_array.shape[1]
    # 32 is defult height for padding
    extraArray = np.full((32, extraLen), 255, dtype='uint8')
    image_array = np.concatenate((extraArray, image_array), axis=1)
    image_array.astype('uint8')
    image = Image.fromarray(image_array)
    return image

def noise_image(img,intensity=0.6): # image arrray values shoulde be between 0 and 1
    img = np.array(img)
    max_array = np.max(img)
    img = img/max_array
    severity = np.random.uniform(0, intensity)
    blur = ndimage.gaussian_filter(np.random.randn(*img.shape) * severity, 1)
    img_speck = (img + blur)
    img_speck[img_speck > 1] = 1
    img_speck[img_speck <= 0] = 0
    img_speck = img_speck*255
    img_speck = img_speck.astype('uint8')
    final_image = Image.fromarray(img_speck)
    return final_image


def make_data(word_list,num,save_dir,noise_ratio = 0.5,index=0):

    print('buldind %s images...'%num)
    toolbar_width = 40
    sys.stdout.write("[%s]" % (" " * toolbar_width))
    sys.stdout.flush()
    sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['
    saved = 0
    pun = ['،','.']
    for _ in range(num):
        while saved != num:
            word = word_list.pop(random.randrange(len(word_list)))
            j = random.randrange(1,11)
            if j % 10 == 2:
                s = random.choice(pun)
                word = word+s     
            font_index = index % 19
            word_image = create_image(word, font_select(font_index)[0])
            word_image = crop_image(word_image)
            random_height = np.random.randint(20, 31)
            resized_word_image = resize_image(word_image, random_height)
            background_img = Image.new('L', BASE_IMAGE_SIZE, color='white')
            rwi_size = resized_word_image.size
            if BASE_IMAGE_SIZE[0]>rwi_size[0]:
                rand_X = np.random.randint(0, BASE_IMAGE_SIZE[0] - rwi_size[0])
                rand_Y = np.random.randint(0, BASE_IMAGE_SIZE[1] - rwi_size[1])
                background_img.paste(resized_word_image,(rand_X,rand_Y))
                if saved >= noise_ratio*num:
                    background_img.save(save_dir+'kntu'+'%s'%(str(index+1).zfill(6))+'.png')
                    with open(save_dir+"kntu%s.txt" %(str(index+1).zfill(6)), 'w', encoding='utf8') as txt:
                        if j % 10 == 2:
                            pass
                        txt.write('%s \nfont : %s' % (word, 'fontName')) 
                else:
                    final_image = noise_image(background_img)
                    final_image.save(save_dir+'kntu'+'%s'%(str(index+1).zfill(6))+'.png')
                    with open(save_dir+"kntu%s.txt" %(str(index+1).zfill(6)), 'w', encoding='utf8') as txt:
                        if j % 10 == 2:
                            pass
                        txt.write('%s \nfont : %s' % (word, 'fontName')) 
                index += 1
                saved += 1
            if saved % int(num/toolbar_width)==0:
               sys.stdout.write("#")
               sys.stdout.flush()
    sys.stdout.write("]\n")
    print('done')


#%%
if __name__ == "__main__":
    make_data(moin,20000,'resources\\datasets\\new_pun\\train\\',0.5)


