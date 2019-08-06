import pandas as pd
import pickle
import random
import re

text_data_directory = 'C:\\Users\\Ali\\Documents\\Uni\\Projects\\OCR\\resources\\'
df = pd.read_excel(text_data_directory+'Persian Words.xlsx')
moinList = df['Moin'].tolist()
moinList = moinList[0:32642]
nastaliqList=[]

for i in range(len(moinList)):
    moinList[i] = re.sub(r'ء','',moinList[i])

with open('moin.txt', 'wb') as moin:
    pickle.dump(moinList,moin)
    
for j in range(2642): #create list of words
    word=moinList.pop(random.randrange(len(moinList)))
    nastaliqList.append(word)

with open (text_data_directory+'nastaliq.txt', 'wb') as nastaliqFile:
    pickle.dump(nastaliqList , nastaliqFile)

with open (text_data_directory+'moinMN.txt', 'wb') as moinMN_file:
    pickle.dump(moinList , moinMN_file)  