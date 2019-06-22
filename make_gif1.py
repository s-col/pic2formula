import pickle
import os
from datetime import datetime
from argparse import ArgumentParser
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# このファイルがあるディレクトリ
dir_base = os.path.dirname(os.path.abspath(__file__))

def main():
    args = get_args()
    path = args.path

    with open(path, "rb") as f:
        x_picf, y_picf = pickle.load(f)

    ani = generate_animation(x_picf, y_picf)

    fname = os.path.split(path)[-1]
    fname = os.path.splitext(fname)[0]
    fname += "_" + datetime.now().strftime(r"%Y%m%d%H%M%S")
    dir_gif = os.path.join(dir_base, "gif")
    if not os.path.isdir(dir_gif):
        os.mkdir(dir_gif)
    fname += ".gif"
    fpath = os.path.join(dir_gif, fname)
    ani.save(fpath, writer="imagemagick")


def get_args():
    parser = ArgumentParser()
    parser.add_argument("path", type=str,
                        help="path to picf-file")
    args = parser.parse_args()
    return args


def generate_animation(x_picf, y_picf):

    PI = np.pi

    def update_plot(n):
        ii = 0
        for x_fs, y_fs in zip(x_fs_lst, y_fs_lst):
            lines[ii].set_data(x_fs(tt, n), y_fs(tt, n))
            ii += 1
        ax.set_title("n = {}".format(n))
        print("n = {}\r".format(n), end="")

    def init():
        for x_fs, y_fs in zip(x_fs_lst, y_fs_lst):
            line, = ax.plot(x_fs(tt), y_fs(tt), color="tab:blue")
            lines.append(line)
        ax.set_title("n = {}".format(1))
        ax.axis("equal")
        ax.grid(True, linestyle="--")

    fig, ax = plt.subplots()
    fig.set_tight_layout(True)
    x_fs_lst = x_picf.fs_lst
    y_fs_lst = y_picf.fs_lst
    tt = np.linspace(0, 2, 5000) * PI
    lines = []

    n_lst = list(range(1, 100)) + list(range(100, 501, 5))
    ani = animation.FuncAnimation(fig, update_plot, n_lst, interval=150,
                                  repeat=True, repeat_delay=5000, init_func=init)
    return ani


if __name__ == '__main__':
    main()
