#import scipy.io as sio
import h5py



import tarfile
import os
import shutil
from urllib import request
from glob import glob

import numpy as np
from scipy.io import loadmat
from scipy import misc as spmisc
from PIL import Image

DATA_DIRECTORY = 'data'

def maybe_download(url):
    os.makedirs(DATA_DIRECTORY, exist_ok=True)
    filename = os.path.basename(url)
    filepath = os.path.join(DATA_DIRECTORY, filename)
    if not os.path.exists(filepath):
        print('Downloading {}'.format(filename))
        filepath, _ = request.urlretrieve(url, filepath)
        print('Successfully downloaded {}'.format(filename))
    return filepath


data = maybe_download("http://horatio.cs.nyu.edu/mit/silberman/nyu_depth_v2/nyu_depth_v2_labeled.mat")
data = h5py.File(data)

img = np.array(data['images'])
img = np.swapaxes(img, 1,3)
depths = np.array(data['depths'])
depths = np.swapaxes(depths, 1,2)

l = list(zip(img, depths))

def nyu_data(train_test_ratio = .8):
    cut = (int(.8*len(l)))
    train_pairs = l[:cut]
    test_pairs = l[cut:]
    return train_pairs, test_pairs