# -*- coding: utf-8 -*-
import os
import glob
from PIL import Image

"""
画像のリサイズ(128x128にする)
"""

image_size = 128

from_dir = "/home/yuma/デスクトップ/自由研究/"
to_dir = "/home/yuma/PycharmProjects/2019science/data/resize"

os.makedirs(to_dir, exist_ok=True)

for path_ in glob.glob(os.path.join(from_dir + "/*")):
    """親フォルダの読み込み"""
    for path in glob.glob(os.path.join(path_ + "/*.JPG")):
        """フォルダ内の画像の読み込み"""
        # resize
        img = Image.open(path)
        img = img.resize((image_size, image_size))
        # 子ファイルの取得
        folder = os.path.dirname(path)
        folds = folder[len(os.path.dirname(folder)):]
        # ファイル名の取得
        basename = os.path.basename(path)

        # save
        to_path = to_dir + folds
        os.makedirs(to_path, exist_ok=True)
        img.save(os.path.join(to_path, basename))
        print(path)

print("Done")
