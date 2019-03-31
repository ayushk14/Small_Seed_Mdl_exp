#!/bin/bash

#GIVE ALL SHELL SCRIPTS EXECUTABLE PERMISSION IN STARTING

export USER=$(whoami)

cp -a ~/kaldi/egs/timit ~/kaldi/egs/AIR_Seed_PER

rm ~/kaldi/egs/AIR_Seed_PER/s5/run.sh
cp -a AIR_Receipe/run.sh ~/kaldi/egs/AIR_Seed_PER/s5/run.sh

rm ~/kaldi/egs/AIR_Seed_PER/s5/cmd.sh
cp -a AIR_Receipe/cmd.sh ~/kaldi/egs/AIR_Seed_PER/s5/cmd.sh

rm ~/kaldi/egs/AIR_Seed_PER/s5/local/timit_prepare_dict.sh
cp -a AIR_Receipe/timit_prepare_dict.sh ~/kaldi/egs/AIR_Seed_PER/s5/local/timit_prepare_dict.sh

rm ~/kaldi/egs/AIR_Seed_PER/s5/steps/make_mfcc.sh
cp -a AIR_Receipe/make_mfcc.sh ~/kaldi/egs/AIR_Seed_PER/s5/steps/make_mfcc.sh

rm ~/kaldi/egs/AIR_Seed_PER/s5/local/nnet/run_dnn.sh
cp -a AIR_Receipe/run_dnn.sh ~/kaldi/egs/AIR_Seed_PER/s5/local/nnet/run_dnn.sh

cp -a AIR_Receipe/local_custom ~/kaldi/egs/AIR_Seed_PER/s5/local_custom
cp -a AIR_Receipe/Python_Files ~/kaldi/egs/AIR_Seed_PER/s5/Python_Files
cp -a AIR_Receipe/steps_fa ~/kaldi/egs/AIR_Seed_PER/s5/steps_fa

mkdir -p ~/kaldi/egs/AIR_Seed_PER/s5/data/local/

cp -a AIR_Receipe/data_files ~/kaldi/egs/AIR_Seed_PER/data
cp -a AIR_Receipe/dict_files ~/kaldi/egs/AIR_Seed_PER/dict
