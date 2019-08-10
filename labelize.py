from arabic_reshaper import letters
#%% create nachasb list
nachasb=['ا','آ','ر','ز','ژ','و','د','ذ',' ']
for i in range(8):
    nachasb.append(letters.connects_with_letter_before(nachasb[i]))
print(nachasb)

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



#%% creating bechasb nachasb list
text='امیر بی گزند'
bn_list=[]
text=' '+text+' '
for let in text:
    if let in nachasb:
        bn_list.append('n')    
    else:
        bn_list.append('b')

# for i in range (1,len(text)-1): # just for observe
#     bn=bn_list[i-1]+bn_list[i]+bn_list[i+1]
#     print(bn)


#%% creating real word     
realWord=''
for i in range (1,len(text)-1):

    if bn_list[i]=='n' :
        if bn_list[i-1]=='n':
            print(text[i])
            realWord=realWord+text[i]
        else:
            print(e_connects_with_letter_before(text[i]))
            realWord=realWord+e_connects_with_letter_before(text[i])
    
    elif bn_list[i]=='b':
        if bn_list[i-1]=='n':
            if text[i+1]==' ':
                print(text[i])
                realWord=realWord+text[i]
            elif text[i+1]!=' ':
                print(e_connects_with_letter_after(text[i]))    
                realWord=realWord+e_connects_with_letter_after(text[i])
        elif bn_list[i-1]=='b':
            if text[i+1]==' ':
                print(e_connects_with_letter_before(text[i]))
                realWord=realWord+e_connects_with_letter_before(text[i])
            elif text[i+1]!=' ':
                print(e_connects_with_letters_before_and_after(text[i]))
                realWord=realWord+e_connects_with_letters_before_and_after(text[i])
print('realWord is %s' %realWord)                





# BND={'bbs':letters.connects_with_letters_before_and_after(let) , 'bb-':letters.connects_with_letter_before(let),'bn':letters.connects_with_letter_before(let),'nbs':letters.connects_with_letter_after(let),'nb-':let,'nn':let}
