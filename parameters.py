import pickle

with open ('alphabetList.txt','rb') as file:
    alphabetList=pickle.load(file)

num_classes = len(alphabetList) + 1
img_w, img_h = 100, 32

# Network parameters
batch_size = 32
val_batch_size = 4

downsample_factor = 4
max_text_len = 30