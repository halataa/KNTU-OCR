#%% reforming letter functions
def e_connects_with_letter_after(let):
    a= letters.connects_with_letter_after(let)
    if a ==False:
        return (let)
    else:
        return(a)
def e_connects_with_letter_before(let) :
    a=letters.connects_with_letter_before(let)
    if a==False:
        return(let)
    else:
        return(a)
def  e_connects_with_letters_before_and_after(let) :
    a=letters.connects_with_letters_before_and_after(let)
    if a==False:
        return(let)
    else:
        return(a)    

#%%
import pickle
with open('C:\\Users\\Ali\\Documents\\Uni\\Projects\\OCR\\resources\\alphabetList.txt','rb') as file:
    alphabetList = pickle.load(file)

#%%
import numpy as np
def label_IO(letter):
    label = np.zeros(len(alphabetList),dtype=int)
    if letter in alphabetList:
        alphaIndex = alphabetList.index(letter)
        label[alphaIndex] = 1
        return label
    else:
        print('(%s) not in list'%letter)
     
    

#%% letter seperator
from arabic_reshaper import letters
def letterSeperator(text):
    #creating nachasb list
    nachasb=['ا','آ','ر','ز','ژ','و','د','ذ',' '] 
    for i in range (len(nachasb)-1):
        nachasb.append(e_connects_with_letter_before(nachasb[i]))
    #labeling b and n for letters sequence
    bn_list=[]
    text=' '+text+' '
    for let in text:
        if let in nachasb:
            bn_list.append('n')    
        else:
            bn_list.append('b')
    #seperating letters
    seperatedList = []
    for i in range (1,len(text)-1):
        if bn_list[i]=='n' :
            if bn_list[i-1]=='n':
                seperatedList.append(text[i])
            else:
                seperatedList.append(e_connects_with_letter_before(text[i]))
        elif bn_list[i]=='b':
            if bn_list[i-1]=='n':
                if text[i+1]==' ':
                    seperatedList.append(text[i])
                elif text[i+1]!=' ':
                    seperatedList.append(e_connects_with_letter_after(text[i]))    
            elif bn_list[i-1]=='b':
                if text[i+1]==' ':
                    seperatedList.append(e_connects_with_letter_before(text[i]))
                elif text[i+1]!=' ':
                    seperatedList.append(e_connects_with_letters_before_and_after(text[i]))
    return seperatedList 



#%%
