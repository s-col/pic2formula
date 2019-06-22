import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button



def detect_edge(path):
    """
    Canny法で画像のエッジ検出を行い結果を返す
    """

    MIN_INIT = 100
    MAX_INIT = 200

    # 画像の読み込み
    img = cv2.imread(path)

    # オリジナルの表示
    plt.figure(1)
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(rgb_img)
    plt.title("Original Image")
    #plt.xticks([]), plt.yticks([])


    # エッジ検出の表示
    fig = plt.figure(2)
    # 初期値で一旦描画
    threshold = [MIN_INIT, MAX_INIT]  # しきい値[min, max]
    edges = cv2.Canny(img, MIN_INIT, MAX_INIT, L2gradient=True)
    ai = plt.imshow(edges, cmap="gray")
    #plt.xticks([]), plt.yticks([])

    # minValスライダーの設定
    axmin = plt.axes([0.2, 0.90, 0.6, 0.03])
    smin = Slider(axmin, "minVal", 0, 1000,
                  valinit=MIN_INIT, valstep=1, valfmt="%d")
    update_min = lambda value: _update_base(value, 0, threshold, img, ai, fig)
    smin.on_changed(update_min)  # スライダーが操作されるとupdate_minが実行される

    # maxValスライダーの設定
    axmax = plt.axes([0.2, 0.95, 0.6, 0.03])
    smax = Slider(axmax, "maxVal", 0, 1000,
                  valinit=MAX_INIT, valstep=1, valfmt="%d")
    update_max = lambda value: _update_base(value, 1, threshold, img, ai, fig)
    smax.on_changed(update_max)  # スライダーが操作されるとupdate_manが実行される

    # OKボタンの設定
    axok = plt.axes([0.85, 0.05, 0.1, 0.05])
    bok = Button(axok, "OK", )

    def end_plot(event):
        plt.close("all")
    bok.on_clicked(end_plot)  # ボタンがクリックされるとend_plotが実行される

    plt.show()

    edges = cv2.Canny(img, threshold[0], threshold[1], L2gradient=True)
    return edges


def _update_base(value, index, threshold, img, ai, fig):
    threshold[index] = value
    edges = cv2.Canny(img, threshold[0], threshold[1], L2gradient=True)
    ai.set_data(edges)
    fig.canvas.draw_idle()
