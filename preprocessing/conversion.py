from PIL import Image
import numpy as np
import os
import glob

from_dir = "/home/yuma/PycharmProjects/2019science/data/resize"
to_dir = "/home/yuma/PycharmProjects/2019science/data/ndarray"

os.makedirs(to_dir, exist_ok=True)

count = 0
# 画像データがいくつあるか測定する
for path_ in glob.glob(os.path.join(from_dir + "/*")):
    """親フォルダの読み込み"""
    for path in glob.glob(os.path.join(path_ + "/*.JPG")):
        """フォルダ内の画像の読み込み"""
        count += 1

train = np.zeros((count, 128, 128, 3))
target = np.zeros(count).astype(str)

i = 0
for path_ in glob.glob(os.path.join(from_dir + "/*")):
    """親フォルダの読み込み"""
    for path in glob.glob(os.path.join(path_ + "/*.JPG")):
        """フォルダ内の画像の読み込み"""
        # ndarrayで読み込み
        img = np.array(Image.open(path))
        # print(img.shape)
        folder = os.path.dirname(path)
        folds = folder[len(os.path.dirname(folder))+1:]

        img = img[np.newaxis, :, :, :]

        train[i, :, :, :] = img.copy()
        target[i] = folds
        i += 1


np.save("/home/yuma/PycharmProjects/2019science/data/ndarray/train_img.npy", train)
np.save("/home/yuma/PycharmProjects/2019science/data/ndarray/target_img.npy", target)
