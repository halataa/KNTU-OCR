

#%%
import arabic_reshaper
from bidi.algorithm import get_display
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import numpy as np
import wikipedia
import re

wikipedia.set_lang("fa")
#%%
summaryNumber=1
for i in range (0,summaryNumber):
    summary=wikipedia.summary(wikipedia.random())
    pureSummary=re.sub('[^\s.،!؟?):/(٪|ء-ی|۰-۹|0-9]','',summary)  #eliminate english characters
pure_summary_list=pureSummary.split(' ')

#%%
# Creating image file

fontFile = 'C:\\Users\\Ali\\Documents\\Uni\\Projects\\OCR\\fonts\\B Font\\B Sara.ttf'
font = ImageFont.truetype(fontFile, 30)

img = Image.new('L',(200,32),color = 'white')

text = 'سلام ایران'
reshaped_text = arabic_reshaper.reshape(text)
bidi_text = get_display(reshaped_text)

draw = ImageDraw.Draw(img)
draw.text((0,0),bidi_text,'black',font=font)

img.save('test.png')
#%%
# Croping

image=Image.open('test.png')
image.load()
image_data = np.asarray(image)
non_empty_columns = np.where(image_data.min(axis=0)<255)[0]
non_empty_rows = np.where(image_data.min(axis=1)<255)[0]
cropBox = (min(non_empty_rows), max(non_empty_rows), min(non_empty_columns), max(non_empty_columns))
image_data_new = image_data[cropBox[0]:cropBox[1]+1, cropBox[2]:cropBox[3]+1]
new_image = Image.fromarray(image_data_new)
new_image.save('test_cropped.png')

#%%
# Resizing

cropped_image = Image.open('test_cropped.png')
cropped_image.load()
width,height = cropped_image.size
reshape_factor = 32/height
new_width , new_height = int(np.ceil(reshape_factor*width)) , int(np.ceil(reshape_factor*height))
print(new_height,new_width)
resized_image = cropped_image.resize((new_width,new_height))
resized_image.show()










#%%
