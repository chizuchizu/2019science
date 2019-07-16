# -*- coding: utf-8 -*-
import os
import glob
import numpy as np
from tqdm import tqdm
from sklearn.model_selection import train_test_split
from PIL import Image

import preprocessing as pre
from preprocessing import image_count


class Preprocess:
    def __init__(self, fd, td, train_name="train_img", target_train_name="target_train_img", test_name="test_img",
                 target_test_name="target_test_img"):
        """
        1.画像のリサイズ(128x128にする)
        2.画像の水増し(18倍)
        3.画像の保存
        :param fd: str, 元のパス
        :param td: str, 保存するパス
        """
        self.from_dir = fd
        self.to_dir = td
        self.train_name = train_name
        self.target_train_name = target_train_name
        self.test_name = test_name
        self.target_test_name = target_test_name

        self.image_size = 128
        self.bai = 18
        self.count = image_count(fd)
        self.train = np.zeros((self.count * self.bai, self.image_size, self.image_size, 3))
        self.target = np.zeros(self.count * self.bai)

    def main(self):
        """
        リサイズと水増しを行う
        :return: None
        """
        os.makedirs(self.to_dir, exist_ok=True)
        i = 0
        for path_ in tqdm(glob.glob(os.path.join(self.from_dir + "/*"))):
            """親フォルダの読み込み"""
            for path in glob.glob(os.path.join(path_ + "/*.JPG")):
                """フォルダ内の画像の読み込み"""
                # resize
                img = Image.open(path)
                img = img.resize((self.image_size, self.image_size))

                # 水増し
                img = np.array(img)[:, :, ::-1]

                img = pre.Ifl.inflated_main(pre.Ifl(), img)

                # ndarrayに変換
                img = np.array(img)
                img = img[np.newaxis, ...]  # 4次元配列に変換

                folder = os.path.dirname(path)
                folds = folder[len(os.path.dirname(folder)) + 1:]
                for j in range(self.bai):
                    # print(img.shape)
                    self.train[i, ...] = img[0, j, ...]
                    self.target[i] = folds

                    i += 1

        print("Resize Done")

    def save(self):
        """
        画像データ(ndarray)とそのラベルを保存
        :return: None
        """
        X_train, X_test, y_train, y_test = train_test_split(self.train, self.target, test_size=0.2, random_state=42)
        np.save(self.to_dir + "/" + self.train_name + ".npy", X_train)
        np.save(self.to_dir + "/" + self.target_train_name + ".npy", y_train)
        np.save(self.to_dir + "/" + self.test_name + ".npy", X_test)
        np.save(self.to_dir + "/" + self.target_test_name + ".npy", y_test)
