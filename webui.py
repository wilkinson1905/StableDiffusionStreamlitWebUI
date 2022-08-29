import random, time, os
import streamlit as st
import threading
import subprocess
import PIL
from PIL import Image

def generate(prompt, seed,ddim_steps, prompt_correction, n_iter):
    subprocess.run(f"python scripts/txt2img4webui.py --prompt '{prompt}' --seed {seed} --ddim_steps {ddim_steps} --n_iter {n_iter} --prompt_correction '{prompt_correction}'", capture_output=False, shell=True)



def generator_tab():
    prompt = st.text_input('Prompt')
    with st.expander("Advanced settings"):
        prompt_correction = st.text_input('Prompt Correction(プロンプト1::重み1,プロンプト2::重み2,...)')
        n_iter = st.selectbox("n_iter", range(1,11), index=0)
        ddim_steps = st.selectbox("ddim_steps", [10,20,30,40,50], index=4)
        seed = st.number_input('seed number(-1 means random)',min_value=-1, value = -1, step=1)
    if st.button('Generate'):
        progressbar = st.progress(0.0)
        if seed == -1:
            seed = random.randint(0,9999999)
        t1 = threading.Thread(target=generate,args=(prompt, seed,ddim_steps, prompt_correction, n_iter))
        t1.start()
        base_count = len(os.listdir("outputs/txt2img-samples/samples/"))
        last_count = base_count
        now_count = base_count
        while now_count - base_count < n_iter:
            dir_list = sorted(os.listdir("outputs/txt2img-samples/samples/"))
            now_count = len(dir_list)
            if last_count != now_count:
                try:
                    st.image(os.path.join("outputs/txt2img-samples/samples/",dir_list[-1]),caption=dir_list[-1])
                except PIL.UnidentifiedImageError:
                    continue
                progressbar.progress((now_count - base_count)/float(n_iter))
                last_count = now_count
            time.sleep(1)
            if not t1.is_alive():
                break
        progressbar.progress(1.0)
        t1.join()

def gallery_tab():
    #絶対パスを取得
    PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
    #画像保存フォルダのパスを取得
    image_dir = os.path.join(PROJECT_PATH,'../outputs/txt2img-samples/samples')
    # 画像ファイルのリストを取得
    fName_list = sorted(os.listdir(image_dir))[::-1][:20]
    #画像ファイル数
    img_file_num = len(fName_list)
    for idx in range(img_file_num):
        if idx % 4 == 0:
            cols = st.columns(4)
        cols[idx % 4].image(f'{os.path.join(image_dir, fName_list[idx])}',width=150, caption=fName_list[idx])


if __name__ == "__main__":
    st.title('Stable Diffusion WebUI by aiartcreator')
    tab1, tab2 = st.tabs(["Generator","Gallery"])
    with tab1:
        generator_tab()
    with tab2:
        gallery_tab()


