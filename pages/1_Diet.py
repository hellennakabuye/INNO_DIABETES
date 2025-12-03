import streamlit as st
import numpy as np
import base64
import joblib
from PIL import Image


st.set_page_config(page_title="Recommended Diet", layout="centered")
st.title("🍏Expert Recommended Diet")

st.sidebar.write("   ")
st.sidebar.write("   ")
st.sidebar.title("About Diabetes")
st.sidebar.markdown('<a href="https://idf.org/our-network/regions-and-members/africa/members/uganda/" target="_blank">Diabetes in Uganda</a>',
            unsafe_allow_html=True)
st.sidebar.markdown('<a href="https://makir.mak.ac.ug/items/6b129844-bd56-4a05-81f8-7e1b3996a9e5" target="_blank">Diabetes Risk Factors</a>',
            unsafe_allow_html=True)
st.sidebar.write("   ")
st.sidebar.write("   ")
st.sidebar.write("   ")

st.sidebar.image("main.png")

st.sidebar.write("   ")
st.sidebar.write('**Developer: Hellen Nakabuye**<br>'
                 '**Bioinformatics Scientist**<br>'
                 '**hellennakabuye23@gmail.com**', unsafe_allow_html=True)


st.markdown('**Diet Guidelines:** low added sugar, high fiber, balanced carbs, lean proteins, and healthy fats.<br>'
            '<br>'  
            ' **General Principles:** Focus on slow-digesting carbs, include protein in every meal, avoid processed foods, and aim for portion control<br>'
            '<br>'
            ' **Breakfasts:** Katogo(Matooke, Beans, Ddodo/Nakati), Combo(Tea, 2 Bread slices, 1 Boiled egg), Fruity(1 Banana, 1 Boiled egg, 2 spoons of Gnuts)<br>'
            '<br>'
            ' **Lunch:** Classic(Posho, Beans, Nakati), Sweet(SweetPotatoes, Peas, Avocado), Heavy(Kalo, Chicken, Ddodo)<br>'
            '<br>'
            ' **Dinner:** Poa(Matooke, Gnuts Paste, Spinach), Color(Pumpkin, Beans, Bugga), <br>Rola(1 Chapati, 2 eggs, Avocado)<br>'
            '<br>'  
            '**Snacks:** Fruits(Fruits(Bananas, Half Mango, Apple, Orange ), Boiled eggs, <br>Roasted Gnuts/Soya/Simsim, Plain Yorgurt)<br>',unsafe_allow_html=True)


# Convert local image to base64
def get_base64_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

img_base64 = get_base64_image("diet.jpg")  # ← put your image file here

st.markdown(
    f"""
    <style>
    .bottom-right-image {{
        position: fixed;
        bottom: 0px;
        right: 20px;
        height: 350px;   /* length */
        width: 350px;    /* width */
        object-fit: cover;
        z-index: 999;
    }}
    </style>

    <img src="data:image/png;base64,{img_base64}" class="bottom-right-image">
    """,
    unsafe_allow_html=True
)
