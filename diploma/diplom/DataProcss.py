import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
import matplotlib
matplotlib.use('Agg')
from tensorflow.keras.models import load_model
from django.conf import settings
import numpy as np
import pandas as pd
import soundfile as sf
from matplotlib import pyplot as plt
import librosa
from librosa import display
from pathlib import Path
from os.path import join
from tensorflow.keras.utils import Sequence
from matplotlib.image import imread
import math


class AccentRec():
    def __init__(self, data_path, mint_t = 0.05):
        self.data_path = data_path
        self.min_time = mint_t
        self.sample, self.rate = librosa.load(Path(self.data_path))

    def save_spectogramm(self,name, samples, sample_rate, save_dir):
        fig = plt.figure(figsize=(180 / 96, 180 / 96))
        fig.add_subplot(1, 1, 1)
        try:
            samples = np.mean(samples, axis=1)
        except IndexError:
            samples = samples
        S = librosa.feature.melspectrogram(y=samples, sr=sample_rate)
        display.specshow(librosa.power_to_db(S))
        plt.savefig(join(save_dir, name + '.png'))
        plt.close('all')



    def energy(self, threshold):
        y = self.sample
        rate = self.rate
        min_time = self.min_time * y.shape[0]
        window = int(min_time)
        mask = []
        yy = pd.Series(y).pow(2)
        roll = yy.rolling(window, 1, True).sum()
        for j in roll:
            if j / window > threshold:
                mask.append(1)
            else:
                mask.append(0)
        return np.array(mask)

    def index_selecting(self, mask):  # calculate indexed os useful data by using mask
        mask[0] = 0
        SS_array = []
        for i in range(1, mask.shape[0] - 1):
            if (mask[i - 1] == 0) and (mask[i] == 1):
                SS_array.append(i)
            if (mask[i] == 1) and (mask[i + 1] == 0):
                SS_array.append(i)
        return np.array(SS_array)

    def delete_to_short(self, indexes):  # delete indexes of data, witch could make to short audio files
        selected_indexes = []
        rate = self.rate
        for i in range(0, indexes.shape[0], 2):
            if indexes[i + 1] - indexes[i] > 0.02 * rate:
                selected_indexes.append(indexes[i])
                selected_indexes.append(indexes[i + 1])
        return np.array(selected_indexes)

    def setense_split(self, indexs, file_name):  # slices the origin wav file in many small audio files
        rate = self.rate
        my_data = self.sample
        for i in range(0, indexs.shape[0], 2):
            difference = int(rate*20 - len(my_data[indexs[i]:indexs[i + 1]]))
            recc = np.concatenate((my_data[indexs[i]:indexs[i + 1]], np.zeros((difference))))
            self.save_spectogramm(file_name + "_" + str(int(i / 2)),recc ,rate, join(settings.MEDIA_ROOT,'spectogram'))
            plt.close('all')
        return None

def my_data_gen(list_dir):
    with list_dir as entry:
        for file in entry:
            yield imread(file)


class Image_bath_gen(Sequence):
    def __init__(self, X, batch_size, dir):
        self.data = np.array(X)
        self.lables = np.zeros(len(X))
        self.batch_size = batch_size
        self.dir = dir

    def __len__(self):
        return math.ceil(self.data.shape[0] / self.batch_size)

    def __getitem__(self, idx):
        batch_x = self.data[idx * self.batch_size:(idx + 1) *
                                                  self.batch_size]
        batch_y = self.lables[idx * self.batch_size:(idx + 1) *
                                                    self.batch_size]

        return np.array([imread(join(self.dir,filename)) / 255 for filename in batch_x]), np.array(batch_y)












