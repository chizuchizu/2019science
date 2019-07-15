# -*- coding: utf-8 -*-
import glob
import os


def image_count(from_dir):
    """
    画像データがいくつあるかをカウントする関数です。
    :param from_dir: str, カウントしたいフォルダのパス
    :return: int, from_dir内にある画像データの個数
    """
    i = 0
    for path in glob.glob(os.path.join(from_dir + "/*")):
        for _ in glob.glob(os.path.join(path + "/*.JPG")):
            i += 1
    return i
