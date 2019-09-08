#%% importiiing
from bidi.algorithm import get_display
import numpy as np
from PIL import ImageDraw
from PIL import Image
from PIL import ImageFont
import arabic_reshaper
import glob
import re
import pickle
import random
import cv2 
from math import sqrt
from PIL import ImageFile #we have to write this line to provide PIL default error
ImageFile.LOAD_TRUNCATED_IMAGES = True ##we have to write this line to provide PIL default error


#%%
layerName='max1'
folder='resources\\for presentation\\cnn images\\%s'%layerName
imageNumber=0
bord=3
size=Image.open('%s\\%s 1.jpg'%(folder,layerName)).size

for file in glob.glob('%s\\%s*.jpg'%(folder,layerName)):
    imageNumber+=1

if imageNumber==64:    
    width,height=8*size[0],8*size[1]
elif imageNumber==128:
    width,height=8*size[0],16*size[1] 
elif imageNumber==256:
    width,height=16*size[0],16*size[1] 
else:           
    width=int(sqrt(imageNumber)*size[0])
    height=int(sqrt(imageNumber)*size[1])

width_with_fasele=int(width+((width/size[0])-1)*bord)
height_with_fasele=int(height+((height/size[1])-1)*bord)

background=Image.new('RGB',(width_with_fasele,height_with_fasele),color='black')
background.save('resources\\blank images\\blank2.png')

x=0
y=0
for file in glob.glob('%s\\*.jpg'%folder):
    img=Image.open(file)
    imageNumber+=1
    if x<background.size[0]-10:
        background.paste(img,(x,y))
        x=x+bord+size[0]
    else:
        y=y+bord+size[1]
        x=0
    background.save('%s\\main%s.jpg'%(folder,layerName))

    








#%%
