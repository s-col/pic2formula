import matplotlib.pyplot as plt
import numpy as np
import sys

from .detect_edge import detect_edge
from .edges2polylines import edges2polylines
from .bspline2fourier_series import bspline2fourier_series
from .pic_formula import PicFormula, plot_pf


def generate(path, n, e=6, k=4, ml=10):
    """
    画像からPicFormulaを生成する

    Parameters
    ----------
    path : str
        画像へのパス
    n : int
        展開次数
    e : int or float
        同一の折れ線とみなす点間の最大距離(px)
    k : int
        Bスプラインの次数
    ml : int or float
        折れ線の最小長さ(これより短い折れ線はフィルタリングされる)(px)

    Returns
    -------
    [x_picf, y_picf] : list of PicFormula
    """
    # 画像からエッジを検出
    edges = detect_edge(path)

    # エッジを折れ線に変換
    polylines = edges2polylines(edges, e)
    print("the number of lines : {}".format(len(polylines)))

    # 短い折れ線を排除
    ml = max(ml, k+1)
    polylines = list(filter(lambda polyline: len(polyline) >= ml, polylines))
    polylines = sorted(polylines, key=lambda pl: pl.length())
    print("the number of lines (filterd): {}".format(len(polylines)))

    # 確認
    dic = {"y": True, "yes": True, "n": False, "no": False, "":False}
    while True:
        inp = input("ok?[y/N] ").lower()
        if inp in dic:
            inp = dic[inp]
            break
        print("Error! Input again.")
    if not inp:
        sys.exit(0)

    # 折れ線を閉じたBスプラインに変換
    bsplines = []
    for polyline in polylines:
        bs = polyline.closed_bspline(k=k)
        bsplines.append(bs)

    # Bスプラインをフーリエ変換してさらにフーリエ係数を求める
    x_fs_lst = []
    y_fs_lst = []
    for bs in bsplines:
        x_fs, y_fs = bspline2fourier_series(bs, n=n)
        x_fs_lst.append(x_fs)
        y_fs_lst.append(y_fs)
    # PicFormulaの生成
    x_picf = PicFormula(x_fs_lst)
    y_picf = PicFormula(y_fs_lst)

    return [x_picf, y_picf]
