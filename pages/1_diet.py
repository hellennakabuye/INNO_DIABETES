import streamlit as st
import numpy as np
import joblib
from PIL import Image


#st.image('food5.jpeg')
img = Image.open("food5.jpeg")
img_resized = img.resize((400, 250))  # (width, height) in pixels

st.image(img_resized)
