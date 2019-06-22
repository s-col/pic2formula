import numpy as np
from fractions import Fraction


class FourierSeries:

    def __init__(self, r, p, n=None):
        """
        Parameters
        ----------
        r : list of int or float
            振幅
        p : list of int or float
            位相
        n : int
            次数
        """
        if len(r) != len(p):
            raise ValueError("r and p must be the same length!")
        if n:
            r = r[:n+1]
            p = p[:n+1]
        self.r = r
        self.p = p
        self.n = len(r) - 1

    def __call__(self, t, n=None):
        """
        Parameters
        ----------
        t : int or float or array-like
            変数
        n : int
            次数
        """
        t = np.array(t)
        if n and n < self.n:
            r = self.r[:n+1].copy()
            p = self.p[:n+1].copy()
            omega_lst = np.arange(n+1)
        else:
            r = self.r.copy()
            p = self.p.copy()
            omega_lst = np.arange(self.n+1)
        r[0] /= 2  # 定数項の振幅は半分にしておく
        o_t = np.outer(t, omega_lst) + p
        cos_mat = np.cos(o_t)
        return cos_mat.dot(r)

    def __str__(self):
        return self.str(showmax=10)

    def str(self, showmax):
        r = self.r
        p = self.p
        omega_lst = np.arange(self.n+1)
        if showmax and showmax < self.n:
            r_e = r[:showmax+1]
            p_e = p[:showmax+1]
            omega_lst_e = omega_lst[:showmax]
        else:
            r_e = r.copy()
            p_e = p.copy()
            omega_lst_e = omega_lst.copy()
        if p_e[0] == 0:
            s = "{:.3f}".format(r_e[0]/2)
        else:
            s = "- {:.3f}".format(r_e[0]/2)
        for rk, pk, omegak in zip(r_e[1:], p_e[1:], omega_lst_e[1:]):
            s += " + {:.3f} cos({}t{:+.3f})".format(rk, omegak, pk)
        if showmax and showmax < self.n:
            rk = r[-1]
            pk = p[-1]
            omegak = omega_lst[-1]
            s += " ... "
            s += " + {:.3f} cos({}t{:+.3f})".format(rk, omegak, pk)
        return s

    def fraction(self, maxd=100):
        return FourierSeriesFraction(self.r, self.p, self.n, maxd)


class FourierSeriesFraction(FourierSeries):

    @staticmethod
    def _ndarray2fractions(arr, max_denominator):
        # 最初の項(定数項)の振幅は半分にするので分母の最大値も半分にする
        tmp = [Fraction(arr[0]).limit_denominator(int(max_denominator/2))]
        tmp += [Fraction(i).limit_denominator(max_denominator) for i in arr[1:]]
        return tmp

    @staticmethod
    def _fractions2ndarray(fracs):
        tmp = [float(frac) for frac in fracs]
        return np.array(tmp)

    @staticmethod
    def _frac2latex(frac, omit=True):
        # omitがTrueなら1を省略する
        if frac.denominator == 1:
            if omit and frac.numerator == 1:
                s = ""
            else:
                s = r"{}".format(frac.numerator)
        else:
            s = r"\frac{{{}}}{{{}}}".format(frac.numerator, frac.denominator)
        return s

    def __init__(self, r, p, n=None, maxd=100):
        """
        Parameters
        ----------
        r : list of int or float
            振幅
        p : list of int or float
            位相
        n : int
            次数
        maxd : int
            分母の最大値
        """
        super().__init__(r, p, n)
        self.maxd = maxd
        self.r_f = self._ndarray2fractions(self.r, maxd)
        self.p_f = self._ndarray2fractions(self.p, maxd)
        self.r = self._fractions2ndarray(self.r_f)
        self.p = self._fractions2ndarray(self.p_f)

    def __str__(self):
        return self.str(showmax=10)

    def str(self, showmax=None):
        r_f = self.r_f
        p_f = self.p_f
        omega_lst = np.arange(self.n+1)
        if showmax and showmax < self.n:
            r_e = r_f[:showmax+1]
            p_e = p_f[:showmax+1]
            omega_lst_e = omega_lst[:showmax+1]
        else:
            r_e = r_f.copy()
            p_e = p_f.copy()
            omega_lst_e = omega_lst.copy()
        if p_e[0] == 0:
            s = "{}".format(r_e[0]/2)
        else:
            s = "- {}".format(r_e[0]/2)
        for rk, pk, omegak in zip(r_e[1:], p_e[1:], omega_lst_e[1:]):
            if pk >= 0:
                s += " + {} cos({}t + {})".format(rk, omegak, pk)
            else:
                s += " + {} cos({}t - {})".format(rk, omegak, -pk)
        if showmax and showmax < self.n:
            s += " + ..."
            if p_f[-1] >= 0:
                s += " + {} cos({}t + {})".format(r_f[-1], omega_lst[-1], p_f[-1])
            else:
                s += " + {} cos({}t + {})".format(r_f[-1], omega_lst[-1], -p_f[-1])
        return s

    def latex(self, showmax=None):
        r_f = self.r_f
        p_f = self.p_f
        fl = self._frac2latex
        omega_lst = np.arange(self.n+1)
        if showmax and showmax < self.n:
            r_e = r_f[:showmax+1]
            p_e = p_f[:showmax+1]
            omega_lst_e = omega_lst[:showmax+1]
        else:
            r_e = r_f.copy()
            p_e = p_f.copy()
            omega_lst_e = omega_lst.copy()
        if p_e[0] == 0:
            s = r"{}".format(fl(r_e[0]/2)) + "\n"
        else:
            s = r"- {}".format(fl(r_e[0]/2)) + "\n"
        for rk, pk, omegak in zip(r_e[1:], p_e[1:], omega_lst_e[1:]):
            if rk != 0:
                if pk == 0:
                    s += r" + {} \cos \left( {}t \right)".format(fl(rk), fl(omegak)) + "\n"
                elif pk >= 0:
                    s += r" + {} \cos \left( {}t + {} \right)".format(fl(rk), fl(omegak), fl(pk, False)) + "\n"
                else:
                    s += r" + {} \cos \left( {}t - {} \right)".format(fl(rk), fl(omegak), fl(-pk, False)) + "\n"
        if showmax and showmax < self.n:
            r_np = self._fractions2ndarray(r_f)
            non_zero = np.where(r_np != 0)[0]
            if non_zero[-1] <= showmax:
                return s
            rk = r_f[non_zero[-1]]
            pk = p_f[non_zero[-1]]
            omegak = omega_lst[non_zero[-1]]
            s += r" + \cdots " + "\n"
            if pk == 0:
                s += r" + {} \cos \left( {}t \right)".format(fl(rk), fl(omegak))
            elif pk >= 0:
                s += r" + {} \cos \left( {}t + {} \right)".format(fl(rk), fl(omegak), fl(pk, False))
            else:
                s += r" + {} \cos \left( {}t - {} \right)".format(fl(rk), fl(omegak), fl(-pk, False))
        return s
