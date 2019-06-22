import os
import pickle
from argparse import ArgumentParser

import pic2formula


def main():
    args = get_args()
    path = args.path
    n = args.n
    e = args.e
    k = args.k
    ml = args.omit
    maxd = args.maxd
    generate_tex_flag = args.tex
    desmos_flag = args.desmos
    tex_showmax = args.showmax

    x_picf, y_picf = pic2formula.generate(path, n=n, e=e, k=k, ml=ml)
    x_picff = x_picf.fraction(maxd)
    y_picff = y_picf.fraction(maxd)

    if generate_tex_flag:
        fname = os.path.basename(path)
        fname = os.path.splitext(fname)[0]
        dir_name = "./tex/{}".format(fname)
        if not os.path.isdir(dir_name):
            os.mkdir(dir_name)
        fname += ".tex"
        fpath = os.path.join(dir_name, fname)
        generate_tex(fpath, x_picff, y_picff, showmax=tex_showmax)
    
    if desmos_flag:
        fname = os.path.basename(path)
        fname = os.path.splitext(fname)[0] + ".txt"
        dir_name = "./desmos"
        fpath = os.path.join(dir_name, fname)
        generate_desmos(fpath, x_picff, y_picff)

    pic2formula.plot_pf(x_picff, y_picff, n=5000, show=True)

    # 保存
    dic = {"y": True, "yes": True, "n": False, "no": False, "":False}
    while True:
        inp = input("save?[y/N] ").lower()
        if inp in dic:
            inp = dic[inp]
            break
        print("Error! Input again.")
    if inp:
        fname = os.path.split(path)[-1]
        fname = os.path.splitext(fname)[0]
        dir = "./picf/"
        if not os.path.isdir(dir):
            os.mkdir(dir)
        fname = "{}/{}.dump".format(dir, fname)
        with open(fname, "wb") as f:
            pickle.dump([x_picff, y_picff], f)


def get_args():
    parser = ArgumentParser()
    parser.add_argument("path", type=str,
                        help="path to an image")
    parser.add_argument("-n", type=int, default=500,
                        help="degree of fourier series approximation[500]")
    parser.add_argument("-e", type=int, default=6,
                        help="connect points which have distance less than given[6]")
    parser.add_argument("-k", type=int, default=4,
                        help="degree of B-Spline[4]")
    parser.add_argument("-o", "--omit", type=int, default=6,
                        help="omit polylines which have length less than given[6]")
    parser.add_argument("-d", "--maxd", type=int, default=100,
                        help="maximum of denominator[100]")
    parser.add_argument("-t", "--tex", action="store_true",
                        help="generate tex")
    parser.add_argument("--desmos", action="store_true",
                        help="make a text file for desmos")
    parser.add_argument("--showmax", type=int, default=20,
                        help="maximum of degree to generate tex")
    args = parser.parse_args()
    return args


def generate_tex(fname, x, y, showmax=5):
    f = open(fname, "w", encoding="utf-8")
    s = \
r"""
\documentclass[9pt,a4paper]{{jsarticle}}

\usepackage[top=5.5truemm,bottom=5.5truemm,left=5.5truemm,right=5.5truemm]{{geometry}}

\usepackage{{amsmath}}
\usepackage{{autobreak}}
\allowdisplaybreaks

\pagestyle{{empty}}

\begin{{document}}

\begin{{align*}}
\begin{{autobreak}}
x(t) =
{}
\end{{autobreak}}
\end{{align*}}

\newpage

\begin{{align*}}
\begin{{autobreak}}
y(t) =
{}
\end{{autobreak}}
\end{{align*}}

\end{{document}}
"""

    s = s.format(x.latex(showmax), y.latex(showmax))
    f.write(s)
    f.close()


def generate_desmos(fname, x, y):
    with open(fname, "w", encoding="utf-8") as f:
        f.write(x.str_desmos(fun_name="f"))
        f.write(y.str_desmos(fun_name="g"))
        for i in range(1,x.num + 1):
            f.write("(f_{{{0:d}}}(t), g_{{{0:d}}}(t))\n".format(i))


if __name__ == '__main__':
    main()
