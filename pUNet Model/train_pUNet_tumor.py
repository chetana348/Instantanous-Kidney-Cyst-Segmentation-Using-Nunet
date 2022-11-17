import os

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
from tensorflow.python.client import device_lib

print(device_lib.list_local_devices())

from pUnet.net_modelbase import BLVnet2dModule
import pandas as pd
import numpy as np


def train():
    '''
    Preprocessing for dataset
    '''
    # Read  data set (Train data from CSV file)
    csvdata = pd.read_csv('dataprocess\\data/traintumor.csv')
    maskdata = csvdata.iloc[:, 1].values
    imagedata = csvdata.iloc[:, 0].values
    # shuffle imagedata and maskdata together
    perm = np.arange(len(imagedata))
    np.random.shuffle(perm)
    imagedata = imagedata[perm]
    maskdata = maskdata[perm]

    punet2d = BLVnet2dModule(512, 512, channels=1, costname=("dice coefficient",))
    punet2d.train(imagedata, maskdata, "BLVNet2ddiceloss.pd", "log\\tumor\\diceVnet2d\\", 0.001, 0.5, 20, 2)


train()
