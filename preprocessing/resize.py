# -*- coding: utf-8 -*-
import os
import glob
from PIL import Image
import numpy as np

import preprocessing as pre
from preprocessing import image_count


class Preprocess:
    def __init__(self, fd, td, train_name="train_img", target_name="target_img"):
        """
        1.画像のリサイズ(128x128にする)
        2.画像の水増し(18倍)
        3.画像の保存
        :param fd: str, 元のパス
        :param td: str, 保存するパス
        :param train_name: str, 画像データのファイル名
        :param target_name: str, 画像データのラベルのファイル名
        """
        self.from_dir = fd
        self.to_dir = td
        self.train_name = train_name
        self.target_name = target_name

        self.image_size = 128
        self.count = image_count(fd)
        self.train = np.zeros((self.count, self.image_size, self.image_size, 3))
        self.target = np.zeros(self.count)

    def main(self):
        """
        リサイズと水増しを行う
        :return: None
        """
        os.makedirs(self.to_dir, exist_ok=True)
        i = 0
        for path_ in glob.glob(os.path.join(self.from_dir + "/*")):
            """親フォルダの読み込み"""
            for path in glob.glob(os.path.join(path_ + "/*.JPG")):
                """フォルダ内の画像の読み込み"""
                # resize
                img = Image.open(path)
                img = img.resize((self.image_size, self.image_size))

                # 水増し
                img = pre.Ifl.inflated_main(pre.Ifl(), img)

                # ndarrayに変換
                img = np.array(img)
                img = img[np.newaxis, ...]  # 4次元配列に変換
                self.train[i, ...] = img.copy()

                folder = os.path.dirname(path)
                folds = folder[len(os.path.dirname(folder)) + 1:]
                self.target[i] = folds

                i += 1

        print("Resize Done")

    def save(self):
        """
        画像データ(ndarray)とそのラベルを保存
        :return: None
        """
        np.save(self.to_dir + self.train_name + ".npy", self.train)
        np.save(self.to_dir + self.target_name + ".npy", self.target)
