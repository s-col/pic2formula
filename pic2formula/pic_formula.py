import numpy as np
import matplotlib.pyplot as plt
import numba as nb



def plot_pf(x_picf, y_picf, n=1000, show=True, **kwargs):
    DLT = 1e-8  # 不連続点に空けておく隙間の大きさ
    if x_picf.num != y_picf.num:
        raise ValueError("x and y must be the same length!")
    kwargs = kwargs or {}
    kwargs["color"] = "tab:blue"
    PI = np.pi
    num = x_picf.num
    plt.figure("N = {:d}".format(x_picf.degree))
    for ii in range(num+1):
        # 不連続点には若干の隙間を空けておく
        tt = np.linspace(2*(ii-1)+DLT, 2*ii-DLT, n) * PI
        plt.plot(x_picf(tt), y_picf(tt), **kwargs)
    plt.axis("equal")
    plt.grid(True, linestyle="--")
    plt.tight_layout()
    if show:
        plt.show()


class PicFormula:

    def __init__(self, fs_lst):
        num = len(fs_lst)
        self._fs_lst = fs_lst
        self._num = num

    def __call__(self, t, n=None):
        """
        Parameters
        ----------
        t : int or float or array-like
            変数
        n : int
            次数
        """
        PI = np.pi
        num = self._num
        t = np.array(t)
        idx = np.array(t // (2*PI), dtype=np.int64)
        idx[idx < 0] = 0
        idx[idx > num - 1] = num - 1
        res = np.zeros(t.shape)
        for idx_k in range(num):
            match = idx == idx_k
            res[match] = self._fs_lst[idx_k](t[match], n)
        return res

    def __str__(self):
        return self.str(showmax=10)

    def str(self, showmax=None):
        res = ""
        for ii, fs in enumerate(self._fs_lst):
            if ii == 0:
                res += "({})".format(fs.str(showmax=showmax))
                res += "θ(t)θ(2π - t)"
                continue
            res += " +"
            res += " ({})".format(fs.str(showmax=showmax))
            res += "θ(t - {:d}π)".format(ii * 2)
            res += "θ({:d}π - t)".format((ii + 1) * 2)
        return res


    def fraction(self, maxd=100):
        return PicFormulaFraction(self._fs_lst, maxd)

    def get_fs_lst(self):
        return self._fs_lst
    fs_lst = property(get_fs_lst)

    def get_num(self):
        return self._num
    num = property(get_num)

    def get_degree(self):
        return self._fs_lst[0].n
    degree = property(get_degree)


class PicFormulaFraction(PicFormula):

    def __init__(self, fs_lst, maxd=100):
        super().__init__(fs_lst)
        self.maxd = maxd
        # _fs_lstをfraction化する
        self._fs_lst = [fs.fraction(self.maxd) for fs in self.fs_lst]
    
    def str_desmos(self, fun_name = "f"):
        res = ""
        for ii, fs in enumerate(self._fs_lst):
            tmp = fs.latex().replace("\n","")
            res += "{:s}_{{{:d}}}(t) = {:s}".format(fun_name, ii + 1, tmp) + "\n"
        return res

    def latex(self, showmax=None):
        res = ""
        for ii, fs in enumerate(self._fs_lst):
            if ii == 0:
                res += r"\biggl\{{ {} \biggr\}}".format(fs.latex(showmax=showmax)) + "\n"
                res += r" \theta \left( t \right)"
                res += r" \theta \left( 2 \pi - t \right)" + "\n"
                continue
            res += r" +"
            res += r"\biggl\{{ {} \biggr\}}".format(fs.latex(showmax=showmax)) + "\n"
            res += r" \theta \left( t - {:d} \pi \right)".format(ii * 2)
            res += r" \theta \left( {:d} \pi - t \right)".format((ii + 1) * 2) + "\n"
        return res
