import random, time, os
import streamlit as st
import threading
import subprocess
import PIL
from PIL import Image
from streamlit_drawable_canvas import st_canvas
import pandas as pd
import numpy as np

def generate(prompt, seed,ddim_steps, prompt_correction, n_iter):
    subprocess.run(f"python scripts/txt2img4webui.py --outdir outputs/ --prompt '{prompt}' --seed {seed} --ddim_steps {ddim_steps} --n_iter {n_iter} --prompt_correction '{prompt_correction}'", capture_output=False, shell=True)



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
        base_count = len(os.listdir("outputs/"))
        last_count = base_count
        now_count = base_count
        while now_count - base_count < n_iter:
            dir_list = sorted(os.listdir("outputs/"))
            now_count = len(dir_list)
            if last_count != now_count:
                try:
                    st.image(os.path.join("outputs/",dir_list[-1]),caption=dir_list[-1])
                except PIL.UnidentifiedImageError:
                    continue
                progressbar.progress((now_count - base_count)/float(n_iter))
                last_count = now_count
            time.sleep(1)
            if not t1.is_alive():
                break
        progressbar.progress(1.0)
        t1.join()
def inpaint_tab():
    # Specify canvas parameters in application
    drawing_mode = "freedraw"

    stroke_width = st.slider("Stroke width: ", 1, 100, 25)
    stroke_color = "#0F0"
    bg_color = "#EEE"
    bg_image = st.file_uploader("Background image:", type=["png", "jpg"])
    realtime_update = True
    mask_mode = st.radio(
     "Leave the masked area or leave the non-masked area",
     ('mask',"non-mask"))

    # Create a canvas component
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color=bg_color,
        background_image=Image.open(bg_image) if bg_image else None,
        update_streamlit=realtime_update,
        height=512,
        width=512,
        drawing_mode=drawing_mode,
        point_display_radius=0,
        key="canvas",
    )

    # Do something interesting with the image data and paths
    if canvas_result.image_data is not None:
        mask = np.array(Image.fromarray(canvas_result.image_data).convert("L"))
        if mask_mode == "mask":
            mask = (mask > 100)*255
        else:
            mask = (mask < 100)*255
    if st.button('Inpainting'):
        print(bg_image)
        Image.open(bg_image).save("data/inpainting.png")
        Image.fromarray(mask.astype(np.uint8)).save("data/mask.png")

        subprocess.run(f"python scripts/inpaint4webui.py --outdir outputs/ --input_name {bg_image.name} --input data/inpainting.png --mask data/mask.png", capture_output=False, shell=True)
        dir_list = sorted(os.listdir("outputs/"))
        st.image(os.path.join("outputs/",dir_list[-1]),caption=dir_list[-1])

    

def gallery_tab():
    #絶対パスを取得
    PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
    #画像保存フォルダのパスを取得
    image_dir = os.path.join(PROJECT_PATH,'../outputs/')
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
    tab1, tab2, tab3 = st.tabs(["Generator", "Inpaint","Gallery"])
    with tab1:
        generator_tab()
    with tab2:
        inpaint_tab()
    with tab3:
        gallery_tab()


