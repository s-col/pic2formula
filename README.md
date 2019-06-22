# pic2formula

画僧を数式に変換する / convert a picture to fomulas

![demo.png](https://github.com/s-col/pic2formula/blob/fig_for_Readme/demo.png)

## 必要なライブラリ

* numpy
* matplotlib
* scipy
* numba
* opencv

## 使い方(クイックガイド)

1. 次のコマンドを実行：

```
python main.py path [-t]
```

```
path : 変換したい画像のパス  
-t : 画像から生成された数式を記述するtexファイルを生成する
```

2. 上のコマンドを実行すると画像のエッジ検出結果が表示される．ウィンドウ上部のバーを操作することにより，エッジ検出の具合を調節可能．
調節ができたら「OK」を押す．

3. しばらく待つと，`ok?[y/N]`と表示される．そのまま処理を続行する場合は`y`を入力してEnterを押す．中断したければ`n`を入力する．

4. 画像から生成された数式のプロットが表示される．`-t`オプションが指定されていたら，数式を記述したtexファイルも生成され`tex`ディレクトリ下に保存される．
ここで生成されるtexファイルは特に手を加えずともそのままコンパイルすることができる．コンパイルすると，画像から生成された数式を記述したPDFファイルが得られる．

5. プロットを閉じると`save?[y/N]`と表示される．`y`を入力しEnterを押すと，`picf`ディレクトリ下にpicfファイルが保存される．このファイルには画像から生成された数式の情報が保存されている．これの中身は次のコマンドを実行することにより確認できる．

```
python load_pifc.py path
```

```
path : 中身を確認したいpicfファイルのパス
```

詳細な使い方ははソースを見てください．
