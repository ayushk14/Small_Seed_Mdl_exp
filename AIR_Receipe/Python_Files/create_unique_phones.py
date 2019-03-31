import os
import sys

AIR_dataset_dir = sys.argv[1]

file = open(AIR_dataset_dir+'/kaldi_files/lexicon_for_phones.txt','r')
f_content = file.read().split('\n')
f_content.remove('')

unique_phone_list = []
for item in f_content:
    item = item.replace(' 32','')

    phone_list = item.split(';')[1].split(' ')
    phone_list = set(phone_list)

    for i in phone_list:
        if i not in unique_phone_list:
            unique_phone_list.append(i)
file.close()

file = open(AIR_dataset_dir+'/kaldi_files/phones.txt','w')
for item in unique_phone_list:
    file.write(item+'\n')
file.close()
