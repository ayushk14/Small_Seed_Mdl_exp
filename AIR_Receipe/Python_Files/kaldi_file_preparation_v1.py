import pandas as pd
import os
from pydub import AudioSegment
import sys

AIR_dir = sys.argv[1]

df = pd.read_csv(AIR_dir+'/Kannada_Dataset/description.csv')

df = df.drop(columns=['Person_Name','Gender','Split_to_Sentence','Sentence_Audio_verified','Nosiy_data_checked','# sentences_found','Duration (sum_of_split_files)','Data_cleaned','Remarks'])

# This list will be created from csv file above
# files_to_use = ['15_Jan', '18_Feb', '19_Jan', '20_Jan', '7_Jan', '8_Jan']
files_to_use = ['5_Jan','7_Jan','8_Jan','10_Jan','15_Jan','19_Jan','20_Jan','23_Jan','18_Feb']
files_to_use.sort()

# This list will be generated from the csv file above
spk_list = ['FA','MA','MB','MC']

text_files_dir = AIR_dir+'/Kannada_Dataset/Transcript/Split_Text_Files(Cleaned)/'
audio_files_dir = AIR_dir+'/Kannada_Dataset/Audio/Audio_Split/'


# Folder for kaldi named files_v2
if not os.path.exists(AIR_dir+'/kaldi_files/'):
    os.makedirs(AIR_dir+'/kaldi_files/')


# List of utterance IDs
file = open(AIR_dir+'/kaldi_files/train.uttids','w')
for folder_name in files_to_use:
    open_folder_dir = text_files_dir+folder_name+'/'

    files_split_list = os.listdir(open_folder_dir)
    files_split_list.sort()

    for item in files_split_list:
        if item[0] != '.' and item[0] != '_':
            utt_id = item[:-4]+'_'+folder_name+'\n'
            file.write(utt_id)

    #print('Folder ',folder_name,' processed!!!')
file.close()


# Text
def removeSpecialCharacters(string):
    charac_list = [".","-","–","_",";",":","‘","’","“",",","”"]

    for charac in charac_list:
        if charac in string:
            string = string.replace(charac, " ")

    string = string.lstrip()
    string = string.rstrip()
    string = ' '.join(string.split())

    return string

ref_file = open(AIR_dir+'/kaldi_files/train.uttids','r')
ref_file_content = ref_file.read().split('\n')
ref_file_content.remove('')

temp_list = []
for item in ref_file_content:
    file_name = item[:6]
    folder_name = item[7:]

    split_file = open(text_files_dir+folder_name+'/'+file_name+'.txt','r')
    s_f_content = split_file.read()

    s_f_content = removeSpecialCharacters(s_f_content)

    if s_f_content[-1] == '\n':
        temp_str = item+' '+s_f_content
    else:
        temp_str = item+' '+s_f_content+'\n'

    #file.write(temp_str)
    temp_list.append(temp_str)
temp_list.sort()

file = open(AIR_dir+'/kaldi_files/train.text','w')
for item in temp_list:
    file.write(item)
file.close()
ref_file.close()
#print('All files processed!!!')


# utt2spk
ref_file = open(AIR_dir+'/kaldi_files/train.uttids','r')
ref_file_content = ref_file.read().split('\n')
ref_file_content.remove('')

temp_list = []
for item in ref_file_content:
    spk = item[:2]
    temp_str = item+' '+spk
    temp_list.append(temp_str)
temp_list.sort()

file = open(AIR_dir+'/kaldi_files/train.utt2spk','w')
for item in temp_list:
    file.write(item+'\n')
file.close()
ref_file.close()
#print('All files processed!!!')


# spk2utt
ref_file = open(AIR_dir+'/kaldi_files/train.utt2spk','r')
ref_file_content = ref_file.read().split('\n')
ref_file_content.remove('')

spk2utt_dict = {}
for spk in spk_list:
    spk2utt_dict[spk] = []

for item in ref_file_content:
    spk = item.split(' ')[1]
    spk2utt_dict[spk].append(item.split(' ')[0])

file = open(AIR_dir+'/kaldi_files/train.spk2utt','w')
for spk in spk_list:
    utt_list = spk2utt_dict[spk]

    temp_str = spk
    for utt in utt_list:
        temp_str = temp_str+' '+utt
    temp_str = temp_str+'\n'

    file.write(temp_str)
file.close()
ref_file.close()
#print('All files processed!!!')


# spk2gender
temp_list = []
for spk in spk_list:
    gender = spk[0].lower()
    temp_str = spk+' '+gender+'\n'
    temp_list.append(temp_str)
temp_list.sort()

file = open(AIR_dir+'/kaldi_files/train.spk2gender','w')
for item in temp_list:
    file.write(item)
file.close()


# wav.scp
wav_file_path = AIR_dir+'/Kannada_Dataset/Audio/Audio_Split/'

ref_file = open(AIR_dir+'/kaldi_files/train.uttids','r')
ref_file_content = ref_file.read().split('\n')
ref_file_content.remove('')

temp_list = []
for item in ref_file_content:
    file_name = item[:6]
    folder_name = item[7:]

    temp_str = item+' '+wav_file_path+folder_name+'/'+file_name+'.wav\n'

    temp_list.append(temp_str)
temp_list.sort()

file = open(AIR_dir+'/kaldi_files/train_wav.scp','w')
for item in temp_list:
    file.write(item)
file.close()
ref_file.close()
#print('All files processed!!!')


# Duration file
ref_file = open(AIR_dir+'/kaldi_files/train.uttids','r')
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

file = open(AIR_dir+'/kaldi_files/train_dur.ark','w')
for item in temp_list:
    file.write(item)
file.close()
ref_file.close()


# # stm file

# ref_file = open(AIR_dir+'/kaldi_files/dur.ark','r')
# ref_file_content = ref_file.read().split('\n')
# ref_file_content.remove('')

# temp_list = []
# for item in ref_file_content:
#     file_name = item.split(' ')[0][:6]
#     folder_name = item.split(' ')[0][7:]
#
#     uttid = item.split(' ')[0]
#     channel = 1
#     speaker_id = item[:2]
#     start_time = 0.0
#     end_time = item.split(' ')[1]
#
#     temp_file = open(text_files_dir+folder_name+'/'+file_name+'.txt','r')
#     temp_file_content = temp_file.read()
#
#     temp_str = uttid+' '+str(channel)+' '+speaker_id+' '+str(start_time)+' '+str(end_time)+' <O,M> '+temp_file_content
#
#     if temp_str[-1] == '\n':
#         temp_list.append(temp_str)
#     else:
#         temp_list.append(temp_str+'\n')

# temp_list.sort()

# str_1 = ';; LABEL "O" "Overall" "Overall"'
# str_2 = ';; LABEL "F" "Female" "Female speakers"'
# str_3 = ';; LABEL "M" "Male" "Male speakers"'

# file = open(AIR_dir+'/kaldi_files/stm','w')
#
# file.write(str_1+'\n')
# file.write(str_2+'\n')
# file.write(str_3+'\n')
#
# for item in temp_list:
#     file.write(item)

# file.close()
# ref_file.close()
