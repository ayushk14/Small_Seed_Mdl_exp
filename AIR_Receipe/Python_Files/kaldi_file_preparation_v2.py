import pandas as pd
from pydub import AudioSegment
import os
from random import shuffle
from sklearn.model_selection import train_test_split
import sys

AIR_dir = sys.argv[1]

df = pd.read_csv(AIR_dir+'/Kannada_Dataset/description.csv')
df = df.drop(columns=['Person_Name','Gender','Split_to_Sentence','Sentence_Audio_verified','Noisy_data_checked','# sentences_found','Duration(sum_of_split_files)in_min','Duration(sum_of_split_files)in_sec','Data_cleaned','Remarks'])

spk_list = df['Utterence_ID(used)'].unique().tolist()
spk_list.sort()

text_files_dir = AIR_dir+'/Kannada_Dataset/Transcript/Cleaned_Split_Text/'
audio_files_dir = AIR_dir+'/Kannada_Dataset/Audio/Audio_Split/'

split_cat = ['dev']


# # Folder for kaldi named files_train_test
if not os.path.exists(AIR_dir+'/kaldi_files/'):
    os.makedirs(AIR_dir+'/kaldi_files/')


# # Text
# Before running from here, make sure train.uttids and test.uttids is copied from dataset folder to kaldi files folder
'''
def removeSpecialCharacters(string):
    charac_list = [".","-","–","_",";",":","‘","’","“",",","”","'","`","?"]

    for charac in charac_list:
        if charac in string:
            string = string.replace(charac, " ")

    string = string.lstrip()
    string = string.rstrip()
    string = ' '.join(string.split())

    return string

for x in split_cat:
    ref_file = open(AIR_dir+'/kaldi_files/'+x+'.uttids','r')
    ref_file_content = ref_file.read().split('\n')
    ref_file_content.remove('')

    temp_list = []
    for item in ref_file_content:
        file_name = item[:6]
        folder_name = item[7:]

        split_file = open(text_files_dir+folder_name+'/'+file_name+'.txt','r',encoding='utf8')
        s_f_content = split_file.read()

        s_f_content = removeSpecialCharacters(s_f_content)

        if s_f_content[-1] == '\n':
            temp_str = item+' '+s_f_content
        else:
            temp_str = item+' '+s_f_content+'\n'

        temp_list.append(temp_str)
    temp_list.sort()

    file = open(AIR_dir+'/kaldi_files/'+x+'.text','w',encoding='utf8')
    for item in temp_list:
        file.write(item)
    file.close()
    ref_file.close()
'''

# # utt2spk
for x in split_cat:
    ref_file = open(AIR_dir+'/kaldi_files/'+x+'.uttids','r')
    ref_file_content = ref_file.read().split('\n')
    ref_file_content.remove('')

    temp_list = []
    for item in ref_file_content:
        spk = item[:2]
        temp_str = item+' '+spk
        temp_list.append(temp_str)
    temp_list.sort()

    file = open(AIR_dir+'/kaldi_files/'+x+'.utt2spk','w')
    for item in temp_list:
        file.write(item+'\n')
    file.close()
    ref_file.close()

for x in split_cat:
    ref_file = open(AIR_dir+'/kaldi_files/'+x+'.utt2spk','r')
    ref_file_content = ref_file.read().split('\n')
    ref_file_content.remove('')

    spk2utt_dict = {}
    for spk in spk_list:
        spk2utt_dict[spk] = []

    for item in ref_file_content:
        spk = item.split(' ')[1]
        spk2utt_dict[spk].append(item.split(' ')[0])

    file = open(AIR_dir+'/kaldi_files/'+x+'.spk2utt','w')
    for spk in spk_list:
        utt_list = spk2utt_dict[spk]

        temp_str = spk
        for utt in utt_list:
            temp_str = temp_str+' '+utt
        temp_str = temp_str+'\n'

        file.write(temp_str)
    file.close()
    ref_file.close()


# # spk2gender
temp_list = []
for spk in spk_list:
    gender = spk[0].lower()
    temp_str = spk+' '+gender+'\n'
    temp_list.append(temp_str)
temp_list.sort()

for x in split_cat:
    file = open(AIR_dir+'/kaldi_files/'+x+'.spk2gender','w')
    for item in temp_list:
        file.write(item)
    file.close()


# # wav.scp
wav_file_path = AIR_dir+'/Kannada_Dataset/Audio/Audio_Split/'

for x in split_cat:
    ref_file = open(AIR_dir+'/kaldi_files/'+x+'.uttids','r')
    ref_file_content = ref_file.read().split('\n')
    ref_file_content.remove('')

    temp_list = []
    for item in ref_file_content:
        file_name = item[:6]
        folder_name = item[7:]

        temp_str = item+' '+wav_file_path+folder_name+'/'+file_name+'.wav\n'

        temp_list.append(temp_str)
    temp_list.sort()

    file = open(AIR_dir+'/kaldi_files/'+x+'_wav.scp','w')
    for item in temp_list:
        file.write(item)
    file.close()
    ref_file.close()


# # Duration file
for x in split_cat:
    ref_file = open(AIR_dir+'/kaldi_files/'+x+'.uttids','r')
    ref_file_content = ref_file.read().split('\n')
    ref_file_content.remove('')

    temp_list = []
    for item in ref_file_content:
        file_name = item[:6]
        folder_name = item[7:]

        audio_file = AudioSegment.from_wav(audio_files_dir+folder_name+'/'+file_name+'.wav')

        temp_str = item+' '+str(audio_file.duration_seconds)+'\n'
        temp_list.append(temp_str)
    temp_list.sort()

    file = open(AIR_dir+'/kaldi_files/'+x+'_dur.ark','w')
    for item in temp_list:
        file.write(item)
    file.close()
    ref_file.close()
