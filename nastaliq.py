#%%
from urllib.request import urlretrieve
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from main_dataset import crop_image,create_image,noise_image,resize_image
import numpy as np
from PIL import Image
import pickle
import sys
import random

BASE_IMAGE_SIZE = (100, 32)
driver = webdriver.Chrome()
#%%
def fetch_nastaliq(text='برای تست'):


    driver.get('http://nastaliqonline.ir/')

    selectSize = Select(driver.find_element_by_id('xcolor1'))
    selectSize.select_by_visible_text('70')
    selectFont = Select(driver.find_element_by_name('coli'))
    selectFont.select_by_value('0')  # 0 is Regular Nastaliq
    driver.find_element_by_name('shadow').click()

    inputElement = driver.find_element_by_id('matn')
    inputElement.send_keys(Keys.CONTROL, 'a')
    inputElement.send_keys(Keys.DELETE)
    inputElement.send_keys(text)

    driver.find_element_by_id('generateit').click()

    imageName = 'resources\\temprory.png'
    driver.save_screenshot(imageName)
    driver.execute_script("window.history.go(-1)")
    image = Image.open(imageName)

    return image


def adjust_nastaliq(image):

    gray_image = image.convert(mode='L')
    gray_array = np.asarray(gray_image)
    gray_copy = np.copy(gray_array)
    x0 = gray_copy.shape[0] // 2
    y0 = gray_copy.shape[1] // 2
    X = gray_copy[x0]
    X = np.where(X > 14)
    Y = gray_copy[:, y0]
    Y = np.where(Y > 14)
    cropBox = [np.min(Y), np.max(Y), np.min(X), np.max(X)]
    croppedArray = gray_copy[cropBox[0]:cropBox[1]+1, cropBox[2]:cropBox[3]+1]
    garbageCordinate = (45, croppedArray.shape[1])  # site text cordinates
    for x in range(garbageCordinate[0]):
        for y in range(garbageCordinate[1]):
            if croppedArray[x, y] < 240 and croppedArray[x, y] > 30:
                croppedArray[x, y] = 255

    newImage = Image.fromarray(croppedArray.astype('uint8'))

    return newImage

def make_nastaliq_data(word_list,num,save_dir,noise_ratio = 0.5,index=0):
    print('buldind %s images...'%num)
    toolbar_width = 40
    sys.stdout.write("[%s]" % (" " * toolbar_width))
    sys.stdout.flush()
    sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['
    # train_file = open(save_dir+'data.txt','w',encoding='utf-8')
    saved = 0
    for _ in range(num):
        while saved != num:
            word = word_list.pop(random.randrange(len(word_list)))
            word_image = adjust_nastaliq(fetch_nastaliq(word))
            word_image = crop_image(word_image,tr=100)
            random_height = np.random.randint(30, 31)
            resized_word_image = resize_image(word_image,random_height)
            background_img = Image.new('L', BASE_IMAGE_SIZE, color='white')
            rwi_size = resized_word_image.size
            if BASE_IMAGE_SIZE[0]>rwi_size[0]:
                rand_X = np.random.randint(0, BASE_IMAGE_SIZE[0] - rwi_size[0]+1)
                rand_Y = np.random.randint(0, BASE_IMAGE_SIZE[1] - rwi_size[1]+1)
                background_img.paste(resized_word_image,(rand_X,rand_Y))
                if index >= noise_ratio*num:
                    background_img.save(save_dir+'kntu'+'%s'%(str(index+1).zfill(5))+'.png')
                    # train_line = word+'\n'
                    with open(save_dir+"kntu%s.txt" %(str(index+1).zfill(5)), 'w', encoding='utf8') as txt:
                        txt.write('%s \nfont : %s' % (word, 'fontName')) 

                else:
                    final_image = noise_image(background_img,0.4)
                    final_image.save(save_dir+'kntu'+'%s'%(str(index+1).zfill(5))+'.png')
                    #  train_line = word+'\n'
                    with open(save_dir+"kntu%s.txt" %(str(index+1).zfill(5)), 'w', encoding='utf8') as txt:
                        txt.write('%s \nfont : %s' % (word, 'fontName')) 
                    


                # train_file.writelines(train_line)
                index += 1
                saved += 1
            if saved % (int(num/toolbar_width)+1)==1:
               sys.stdout.write("#")
               sys.stdout.flush()
    sys.stdout.write("]\n")
    # train_file.close()
    print('done')
#%%
if __name__ == "__main__":
    with open("resources\\nastaliq.txt", 'rb') as moinFile:
        nast_list = pickle.load(moinFile)

    make_nastaliq_data(nast_list,2000,'resources\\datasets\\nastaliq\\',noise_ratio=0.5)


#%%
