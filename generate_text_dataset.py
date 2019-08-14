#%%

import pandas as pd
import pickle
import random
import re
import labelize as lb

text_data_directory = 'D:\\UNIVERSITY\\BACHELOR PROJECT\\Data\\'
df = pd.read_excel(text_data_directory+'Persian Words.xlsx')
moinList = df['Moin'].tolist()
moinList = moinList[0:32642]
nastaliqList = []

mardudList = ['ء', 'ْ', 'ٌ', 'ٍ', 'ً', 'ُ', 'ِ', 'َ', 'ّ', 'ٰ', 'ٔ', 'ء','´']

for i in range(len(moinList)):
    moinList[i] = re.sub(r'ئ', 'ی', moinList[i])
    moinList[i] = re.sub(r'أ', 'ا', moinList[i])
    moinList[i] = re.sub(r'إ', 'ا', moinList[i])
    moinList[i] = re.sub(r'ؤ', 'و', moinList[i])
    moinList[i] = re.sub(r'ة', 'ه', moinList[i])
    moinList[i] = re.sub(r'ك', 'ک', moinList[i])

    for item in mardudList:
        moinList[i] = re.sub(r'%s' % item, '', moinList[i])
with open(text_data_directory+'alphabetList.txt','rb') as file:
    alphabetList = pickle.load(file)
for item in moinList:        
    itemTxt = lb.letterSeperator(item)
    for let in itemTxt:
        if let not in alphabetList:
            print('(%s) not in list'%let) 
            print('%s removed!'%item)
            if item in moinList:
                moinList.remove(item)
        
with open(text_data_directory+'moin.txt', 'wb') as moin:
    pickle.dump(moinList, moin)

for j in range(2642):  # create list of words
    word = moinList.pop(random.randrange(len(moinList)))
    nastaliqList.append(word)

with open(text_data_directory+'nastaliq.txt', 'wb') as nastaliqFile:
    pickle.dump(nastaliqList, nastaliqFile)

with open(text_data_directory+'moinMN.txt', 'wb') as moinMN_file:
    pickle.dump(moinList, moinMN_file)


#%%
