# %% import moin.text
from bidi.algorithm import get_display
import numpy as np
from PIL import ImageDraw
from PIL import Image
from PIL import ImageFont
import arabic_reshaper
import re
import glob
import pickle
import random
with open("D:\\UNIVERSITY\\BACHELOR PROJECT\\Data\\moinMN.txt", 'rb') as moinFile:
    moin = pickle.load(moinFile)

# %% font select

def fontSelect(fontNumber):
    fontList = []
    for file in glob.glob('D:\\UNIVERSITY\\BACHELOR PROJECT\\Data\\fonts\\*.ttf'):
        fontName = re.findall(r'fonts\\(B .+)\.', file)  # just B series
        fontName = str(fontName[0])
        fontList.append(fontName)
    fontName = fontList[fontNumber]
    fontDir = 'D:\\UNIVERSITY\\BACHELOR PROJECT\\Data\\fonts\\%s.ttf' % fontName
    return(fontDir, fontName)


# %% create image file function

def create_image(text, imageNumber, fontDir):
    font = ImageFont.truetype(fontDir, 50)
    img = Image.new('L', (10000, 300), color='white')
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    draw = ImageDraw.Draw(img)
    draw.text((0, 150), bidi_text, 'black', font=font)
    return (img)


def crop_image(img):
    image_data = np.asarray(img)
    non_empty_columns = np.where(image_data.min(axis=0) < 255)[0]
    non_empty_rows = np.where(image_data.min(axis=1) < 255)[0]
    cropBox = (min(non_empty_rows), max(non_empty_rows),
               min(non_empty_columns), max(non_empty_columns))
    image_data_new = image_data[cropBox[0]                                :cropBox[1]+1, cropBox[2]:cropBox[3]+10]
    new_image = Image.fromarray(image_data_new)
    return new_image


def resize_image(cropped_image):
    width, height = cropped_image.size
    reshape_factor = 32/height
    new_width, new_height = int(
        np.ceil(reshape_factor*width)), int(np.ceil(reshape_factor*height))
    resized_image = cropped_image.resize((new_width, new_height))
    return resized_image


# %% mainCode
imageNumber = 0
mainList = []
failCount = 0
fontNumber = 0
x = 8
while len(moin) > 0:
    wordList = []

    if x == 7 and failCount > 1000:
        x = 8
        failCount = 0
    elif x == 8 and failCount > 1000:
        x = 7
        failCount = 0
    elif len(moin) < 100:
        x = 10
    for j in range(x):  # create list of words
        word = moin.pop(random.randrange(len(moin)))
        wordList.append(word)
    text = ' '.join(wordList)
    fontDir = fontSelect(fontNumber)[0]
    fontName = fontSelect(fontNumber)[1]
    image = resize_image(crop_image(create_image(text, imageNumber, fontDir)))
    if 500 < image.size[0] < 720:
        fontNumber = imageNumber % 19
        imageNumber += 1
        imageArray = np.copy(np.asarray(image))
        extraLen = 720-imageArray.shape[1]
        extraArray = np.full((32, extraLen), 255)
        extraimage = Image.fromarray(extraArray)
        imageArray = np.concatenate((extraArray, imageArray), axis=1)
        image = Image.fromarray(imageArray*255)
        image.save(
            "D:\\UNIVERSITY\\BACHELOR PROJECT\\Data\\mainDataset\\kntu%s.png" % imageNumber)
        with open("D:\\UNIVERSITY\\BACHELOR PROJECT\\Data\\mainDataset\\kntu%s.txt" % imageNumber, 'w', encoding='utf8') as txt:
            txt.write('%s \nfont : %s' % (text, fontName))
        mainList.append(text)
        failCount = 0
    else:
        failCount += 1
        moin.extend(wordList)
        print('\n\n failCount is %i' % failCount)
        print('x is %i ' % x)
        print('len moin is %i' % len(moin))
        print('len ax is %i' % image.size[0])
