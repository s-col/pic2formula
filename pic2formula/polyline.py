import math
import numpy as np
from scipy import interpolate


class Polyline(list):
    @staticmethod
    def _2Dcheck(value):
        if len(value) != 2:
            raise ValueError("Value must be 2-D.")

    def __init__(self):
        super().__init__()

    def __setitem__(self, key, value):
        self._2Dcheck(value)
        value = np.array(value, np.float64)
        super().__setitem__(key, value)

    def __str__(self):
        s = ""
        for value in self:
            s += "["
            for v in value:
                s += str(v) + ", "
            s = s[:-2] + "], "
        s = "[{}]".format(s[:-2])
        return s

    def append(self, value):
        self._2Dcheck(value)
        value = np.array(value, np.float64)
        super().append(value)

    def extend(self, sequence):
        for value in sequence:
            self.append(value)

    def length(self):
        res = 0
        n = len(self)
        for i in range(n-1):
            e = self[i+1] - self[i]
            d = math.sqrt(np.dot(e, e))
            res += d
        return res

    def get_x_arr(self):
        return np.array([p[0] for p in self])

    def get_y_arr(self):
        return np.array([p[1] for p in self])

    def bspline(self, k=2):
        c = np.array(self)
        n = c.shape[0]
        if n <= k:
            msg = "The number of points must be more than {}."
            raise ValueError(msg.format(k))
        t = np.zeros(n+k+1, dtype=np.float64)
        t[n+1:] = 1
        t[k:n+1] = np.linspace(0, 1, n-k+1)
        return interpolate.BSpline(t, c, k, axis=0)

    def closed_bspline(self, epsilon=2, k=2):
        pl = self._close_polyline(epsilon=epsilon)
        c = np.array(pl)
        if np.any(c[0, :] != c[-1, :]):
            c = np.vstack((c, c[0, :]))
        c = np.vstack((c, c[1:k, :]))
        n = c.shape[0]
        dt = 1 / (n - k)
        t0 = - k * dt
        tm = 1 + k * dt
        t = np.linspace(t0, tm, n+k+1)
        return interpolate.BSpline(t, c, k, axis=0)

    def _close_polyline(self, epsilon):
        """
        折れ線を閉じる
        """
        res = self.copy()
        r = self[-1] - self[0]
        delta = math.sqrt(r[0] ** 2 + r[1] ** 2)

        if delta < epsilon:
            res.append(self[0])
        else:
            tmp = res[:-1]
            tmp.reverse()
            res.extend(tmp)
        return res
