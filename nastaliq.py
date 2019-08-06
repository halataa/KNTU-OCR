from urllib.request import urlretrieve
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import numpy as np
from PIL import Image


def fetchNastaliq(text='برای تست'):

    driver = webdriver.Chrome()
    driver.get('http://nastaliqonline.ir/')

    selectSize = Select(driver.find_element_by_id('xcolor1'))
    selectSize.select_by_visible_text('50')
    selectFont = Select(driver.find_element_by_name('coli'))
    selectFont.select_by_value('0')  # 0 is Regular Nastaliq
    driver.find_element_by_name('shadow').click()

    inputElement = driver.find_element_by_id('matn')
    inputElement.send_keys(Keys.CONTROL, 'a')
    inputElement.send_keys(Keys.DELETE)
    inputElement.send_keys(text)

    driver.find_element_by_id('generateit').click()

    imageName = 'temprory.png'
    driver.save_screenshot(imageName)
    driver.close()
    image = Image.open(imageName)

    return image


def adjustNastaliq(image):

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
    garbageCordinate = (45, 310)  # site text cordinates
    for x in range(garbageCordinate[0]):
        for y in range(garbageCordinate[1]):
            if croppedArray[x, y] < 240 and croppedArray[x, y] > 30:
                croppedArray[x, y] = 255

    newImage = Image.fromarray(croppedArray)

    return newImage
