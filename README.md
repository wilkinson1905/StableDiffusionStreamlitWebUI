# StableDiffusionStreamlitWebUI
Stable DiffusionのWebアプリをStreamlitを用いて作成しました  
[![Twitter URL](https://img.shields.io/twitter/url/https/twitter.com/aiartcreator824.svg?style=social&label=Follow%20%40aiartcreator824)](https://twitter.com/aiartcreator824)

# どんなことができるか
1. Stable Diffusionのtxt2imgをWebブラウザ上で実行できます
2. 複数枚画像を生成した場合は、できた画像から表示されていきます
3. 今までに作成した画像のギャラリーを見ることができます
4. 作成した画像のファイル名にシード値とプロンプトが記載してあるので、その値を入力するともう一度同じ画像を生成できます

# ギャラリー
![Gallery1](assets/gallery1.png)  
![Gallery2](assets/gallery2.png)

# 環境構築
1. 前提としてStable Diffusionをローカルにインストール済みであるとします
2. Stable Diffusionのフォルダのscriptsフォルダにこのリポジトリのwebui.pyとtxt2img4webui.pyをコピーします
3. Stable Diffusionの環境に追加のライブラリをインストールします( conda install streamlit==1.12.0 )

# 実行方法
Stable Diffusionのフォルダ上で
```
streamlit run scripts/webui.py
```
と実行します。  
するとWebサーバが起動するので、 http://localhost:8501 のアドレスをWebブラウザで開くとアプリが表示されます。
