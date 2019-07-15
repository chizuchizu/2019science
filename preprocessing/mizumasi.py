#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# usage: ./increase_picture.py hogehoge.jpg
#
import cv2
import numpy as np


class Inflated:
    def __init__(self):
        # ルックアップテーブルの生成
        self.min_table = 50
        self.max_table = 205
        self.diff_table = self.max_table - self.min_table
        self.gamma1 = 0.75
        self.gamma2 = 1.5

        self.LUT_HC = np.arange(256, dtype='uint8')
        self.LUT_LC = np.arange(256, dtype='uint8')
        self.LUT_G1 = np.arange(256, dtype='uint8')
        self.LUT_G2 = np.arange(256, dtype='uint8')

        # 平滑化用
        self.average_square = (10, 10)

        # ハイコントラストLUT作成
        for i in range(self.min_table):
            self.LUT_HC[i] = 0

        for i in range(self.min_table, self.max_table):
            self.LUT_HC[i] = 255 * (i - self.min_table) / self.diff_table

        for i in range(self.max_table, 255):
            self.LUT_HC[i] = 255

        # その他LUT作成
        for i in range(256):
            self.LUT_LC[i] = self.min_table + i * self.diff_table / 255
            self.LUT_G1[i] = 255 * pow(float(i) / 255, 1.0 / self.gamma1)
            self.LUT_G2[i] = 255 * pow(float(i) / 255, 1.0 / self.gamma2)

        self.LUTs = [self.LUT_HC, self.LUT_LC, self.LUT_G1, self.LUT_G2]

    def inflated_main(self, img):
        trans_img = [img]

        # LUT変換
        for i, LUT in enumerate(self.LUTs):
            trans_img.append(cv2.LUT(img, LUT))

        # 平滑化
        trans_img.append(cv2.blur(img, self.average_square))

        # ヒストグラム均一化
        trans_img.append(self.equalizeHistRGB(img))

        # ノイズ付加
        trans_img.append(self.addGaussianNoise(img))
        trans_img.append(self.addSaltPepperNoise(img))

        # 反転
        flip_img = [cv2.flip(x, 1) for x in trans_img]
        trans_img.extend(flip_img)

        return trans_img

    # ヒストグラム均一化
    def equalizeHistRGB(self, src):
        RGB = cv2.split(src)
        Blue = RGB[0]
        Green = RGB[1]
        Red = RGB[2]
        for i in range(3):
            cv2.equalizeHist(RGB[i])

        img_hist = cv2.merge([RGB[0], RGB[1], RGB[2]])
        return img_hist

    # ガウシアンノイズ
    def addGaussianNoise(self, src):
        row, col, ch = src.shape
        mean = 0
        var = 0.1
        sigma = 15
        gauss = np.random.normal(mean, sigma, (row, col, ch))
        gauss = gauss.reshape(row, col, ch)
        noisy = src + gauss

        return noisy

    # salt&pepperノイズ
    def addSaltPepperNoise(self, src):
        row, col, ch = src.shape
        s_vs_p = 0.5
        amount = 0.004
        out = src.copy()
        # Salt mode
        num_salt = np.ceil(amount * src.size * s_vs_p)
        coords = [np.random.randint(0, i - 1, int(num_salt))
                  for i in src.shape]
        out[coords[:-1]] = (255, 255, 255)

        # Pepper mode
        num_pepper = np.ceil(amount * src.size * (1. - s_vs_p))
        coords = [np.random.randint(0, i - 1, int(num_pepper))
                  for i in src.shape]
        out[coords[:-1]] = (0, 0, 0)
        return out
