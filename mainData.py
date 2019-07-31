#%%
import arabic_reshaper
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import numpy as np
from bidi.algorithm import get_display
import glob
import csv



#%% create_data_file function
import wikipedia
import re
def create_data_file ():
    wikipedia.set_lang("fa")
    summaryNumber=10
    count=0
    listKol=[]
    with open ('dataFile.csv' , 'w' , encoding='utf8') as dataFile:
        for i in range (0,summaryNumber):
            summary=wikipedia.summary(wikipedia.random())
            pureSummary=re.sub(r'[^\s.،!؟?):/(٪|ء-ی|۰-۹|0-9]','',summary) #eliminate non persian characters
            pure_summary_list=pureSummary.split(' ')
            # dataFile = open('dataFile.csv', "w" , encoding='utf8')
            writer = csv.writer(dataFile)
            writer.writerow(pure_summary_list)
            print(count)
            count+=1
        
create_data_file()

    




#for text in dataset:
whit open
for file in glob.glob('D:\\UNIVERSITY\\BACHELOR PROJECT\\Most operational Fonts\\*.ttf'):
    fontName = re.findall(r'Fonts\\(B .+)\.', file)  # just B series
    fontFile = file
    font = ImageFont.truetype(fontFile, 30)
    create_image_file(text)
    resize_image_file()
    imageNumber+=1












#%%
#create image file function
dataLocation='D:\\UNIVERSITY\\BACHELOR PROJECT\\Data'
fontFile = 'D:\\UNIVERSITY\\BACHELOR PROJECT\\Most operational Fonts\\B Aseman-.ttf'
font = ImageFont.truetype(fontFile, 30)
text='من نه منم نه من منم'
imageNumber=0


def create_image_file(text,imageNumber):
    img = Image.new('L',(200,32),color = 'white')
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    draw = ImageDraw.Draw(img)
    draw.text((0,0),bidi_text,'black',font=font)
# crop_image_file():
    img.save('test%i.png'  %imageNumber)
    image=Image.open('test%i.png'  %imageNumber)
    image.load()
    image_data = np.asarray(image)
    non_empty_columns = np.where(image_data.min(axis=0)<255)[0]
    non_empty_rows = np.where(image_data.min(axis=1)<255)[0]
    cropBox = (min(non_empty_rows), max(non_empty_rows), min(non_empty_columns), max(non_empty_columns))
    image_data_new = image_data[cropBox[0]:cropBox[1]+1, cropBox[2]:cropBox[3]+1]
    new_image = Image.fromarray(image_data_new)
    new_image.save('test_cropped%i.png' %imageNumber)

def resize_image_file():
    cropped_image = Image.open('test_cropped%i.png' %imageNumber)
    cropped_image.load()
    width,height = cropped_image.size
    reshape_factor = 32/height
    new_width , new_height = int(np.ceil(reshape_factor*width)) , int(np.ceil(reshape_factor*height))
    print(new_height,new_width)
    resized_image = cropped_image.resize((new_width,new_height))
    return(resized_image.show())