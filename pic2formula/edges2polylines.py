import random
import math
import numpy as np
import numba as nb

from .polyline import Polyline


def edges2polylines(edges, neighborhood_size=6, max_cost=None):
    max_cost = max_cost or neighborhood_size ** 2
    pl = make_pointlist(edges)
    init_n_points = len(pl)
    line_bag = []
    count = 0
    print_progress(count, init_n_points)
    while count < init_n_points:
        pl = make_pointlist(edges)
        n_points = len(pl)
        init_idx = random.randrange(n_points)
        line = Polyline()  # 折れ線(点の順列)
        line.append(convert_imshow2plot(pl[init_idx]))
        delete_edges(edges, pl[init_idx])
        count += 1
        could_reverse = True
        while True:
            # 線の端(line[-1])の近くにある点を取得する
            nearest = search_neighbor_points(edges, line[-1], neighborhood_size)
            # 線の端に近い順に並び替え
            nearest = sorted(nearest, key=lambda p: distance(p, line[-1]))
            # 近くに点が無くなったら末端処理
            if not nearest:
                # 線の端の近くに点が無いとき
                if could_reverse:
                    # まだlineを反転していないときは反転する
                    line.reverse()
                    could_reverse = False
                    continue
                else:
                    # 近くに点もなく，既に反転済みのときは線の作成を終える
                    break
            if len(line) <= 3:
                next_point = nearest[0]
            else:
                # line[-2]とline[-3]の中点からline[-1]へ向かうベクトル
                d = (line[-1] - line[-2]) + 0.47 * (line[-2] - line[-3])
                d = d / np.linalg.norm(d)  # 正規化
                nearest = sorted(nearest, key=lambda p: cost_function(p, line[-1], d))
                # 目的関数の最小が閾値を超えたら末端処理
                if cost_function(nearest[0], line[-1], d) > max_cost:
                    if could_reverse:
                        line.reverse()
                        could_reverse = False
                        continue
                    else:
                        break
                next_point = nearest[0]
            line.append(next_point)
            delete_edges(edges, convert_plot2imshow(next_point))
            count += 1
        line_bag.append(line)
        print_progress(count, init_n_points)

    print()
    return line_bag


def cost_function(candidate, line_end, d):
    """
    目的関数
    """
    r = candidate - line_end
    r_norm = math.sqrt(np.dot(r, r))
    return r_norm ** 2 - 0.99 * np.dot(r, d)


def search_neighbor_points(edges, a, neighborhood_size):
    """
    plの中からaからneighborhood_size以内の距離にある点を抽出する
    """
    neighbor_points = []
    pl = points_inside_circle(a, neighborhood_size)
    for p in pl:
        p_img = convert_plot2imshow(p)
        if p_img[0] < 0 or p_img[1] < 0:
            continue
        try:
            if edges[p_img[0], p_img[1]] == 255:
                neighbor_points.append(p)
        except IndexError:
            continue
    return neighbor_points


def distance(a, b):
    """
    座標a, b間の距離を求める(2次元に限る)
    """
    d = math.sqrt((a[0] - b[0]) ** 2 +
                  (a[1] - b[1]) ** 2)
    return d


def make_pointlist(edges):
    """
    エッジ検出結果から点配列を作成する
    """

    xl, yl = np.where(edges == 255)
    return [np.array([x, y]) for x, y in zip(xl, yl)]

@nb.jit(nopython=True)
def points_inside_circle(center, r):
    """
    centerを中心とする半径rの円の内部または円周上にある格子点のリストを返す
    """
    pl = []
    ri = math.floor(r)
    xl = np.arange(-ri, ri + 1)
    for x in xl:
        y = math.sqrt(r ** 2 - x ** 2)
        yi = math.floor(y)
        yl = np.arange(-yi, yi + 1)
        pl.extend([np.array([x, y]) + center for y in yl])
    return pl


def delete_edges(edges, p):
    """
    edgesの指定された点を0にする
    """
    edges[p[0], p[1]] = 0


def convert_imshow2plot(p):
    """
    imshowの座標系からplotの座標系へ変換する
    """
    tmp = p.copy()
    tmp[0] = p[1]
    tmp[1] = - p[0]
    return tmp


def convert_plot2imshow(p):
    """
    plotの座標系からimshowの座標系へ変換する
    """
    tmp = p.copy()
    tmp[0] = - p[1]
    tmp[1] = p[0]
    tmp = tmp.astype(np.int64)
    return tmp


def print_progress(count, init_n_points):
    print("converting pointlist to lines ... {} / {}\r".format(
          count, init_n_points), end="")
