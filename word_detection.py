#%%
from PIL import Image
import cv2
import numpy as np
import matplotlib.pyplot as plt

#%%
def detect_lines(img_path):

    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    th, threshed = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)

    pts = cv2.findNonZero(threshed)
    ret = cv2.minAreaRect(pts)

    (cx,cy), (h,w), ang = ret
    ang += 90

    M = cv2.getRotationMatrix2D((cx,cy), ang, 1.0)
    rotated = cv2.warpAffine(threshed, M, (img.shape[1], img.shape[0]))

    hist = cv2.reduce(rotated,1, cv2.REDUCE_AVG).reshape(-1)

    H,W = img.shape[:2]
    th = 3
    uppers = [y for y in range(H-1) if hist[y]<=th and hist[y+1]>th]
    lowers = [y for y in range(H-1) if hist[y]>th and hist[y+1]<=th]

    cropped = []

    for i in range(len(uppers)):
        a = lowers[i]
        b = uppers[i]
        crop = rotated[b:a+1,:]
        cropped.append(crop)

    return cropped


def get_words(line_list):

    total_lines = []
    for line_image in line_list:
        words = []
        th = 3
        threshold_in_line = 5
        hist1 = cv2.reduce(line_image,0, cv2.REDUCE_AVG).reshape(-1)
        H,W = line_image.shape
        lefts = [x for x in range(W-1) if hist1[x]<=th and hist1[x+1]>th]
        rights = [x for x in range(W-1) if hist1[x]>th and hist1[x+1]<=th]
        x,y,i,j = 1,0,0,0
        while True:
            try:
                a = lefts[i]
                if lefts[x]-rights[y] >= threshold_in_line:
                    word = line_image[:,a:rights[y]+1]
                    words.append(word)
                    i = x
                    a = lefts[i]
                    j = 0
                    x += 1
                    y += 1
                while lefts[x]-rights[y] < threshold_in_line:
                    x += 1
                    y += 1
                    i = x
                    j = 1
                if j == 1:
                    word = line_image[:,a:rights[y]+1]
                    words.append(word)
                    x += 1
                    y += 1
            except:
                word = line_image[:,a:rights[y]+1]
                words.append(word)
                break
        total_lines.append(words)
    return total_lines


def padded_words(word_image_list):
    final_list = []
    for image in word_image_list:
        back = np.zeros([32,100],dtype='uint8')
        H,W = image.shape
        try:
            nh = 32
            nw = int((32/H)*W)
            image = cv2.resize(image,(nw,nh))
            back[:,:image.shape[1]]= image
            word_padded = back
        except:
            nw = 100
            nh = int((100/W)*H)
            image = cv2.resize(image,(nw,nh))
            back[:image.shape[0],:]= image
            word_padded = back
        ret,thresh1 = cv2.threshold(word_padded,100,255,cv2.THRESH_BINARY_INV)
        final_list.append(thresh1)
    return final_list


if __name__ == "__main__":
    image_path = "line.jpg"
    lines = detect_lines(image_path)
    words = get_words(lines)
    pad = padded_words(words[1])
    cv2.imwrite("circle.png",pad[7])


#%%
