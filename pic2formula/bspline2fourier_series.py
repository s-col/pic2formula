import math
import numpy as np
import numba as nb

from .fourier_series import FourierSeries


DEFAULT_NS = 2 ** 14
@nb.jit
def bspline2fourier_series(bs, n, ns=DEFAULT_NS):
    PI = math.pi
    bs_m = modify_domain(bs)  # 定義域を[0,1]から[-pi,pi]に変換
    tt = np.linspace(-PI, PI, ns)
    bs_m_arr = bs_m(tt)
    sp = np.fft.fft(bs_m_arr, axis=0)

    c = sp / ns
    r = np.absolute(c) * 2
    p = np.angle(c)

    x_r = r[:, 0]
    y_r = r[:, 1]
    x_p = p[:, 0]
    y_p = p[:, 1]

    x_fs = FourierSeries(x_r, x_p, n=n)
    y_fs = FourierSeries(y_r, y_p, n=n)
    return [x_fs, y_fs]


def modify_domain(bs):
    """
    bsplineの定義域を[0,1]から[-pi,pi]に変換する
    """
    PI = math.pi
    return lambda t: bs(t / (2 * PI) + 0.5)
