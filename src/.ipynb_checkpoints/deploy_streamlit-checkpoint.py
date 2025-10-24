import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os


# --- Configuration générale ---
st.set_page_config(
    page_title="🏠 House Price Estimator",
    layout="centered",
)

# --- CSS personnalisé ---
st.markdown("""
    <style>
        body {
            background-color: #f7f9fb;
        }
        .main {
            /* Supprimer le style de rectangle blanc */
            background-color: transparent;
            border-radius: 0;
            padding: 0;
            box-shadow: none;
            max-width: 100%;
        }
        h1 {
            text-align: center;
            color: #333333;
            margin-bottom: 30px;
        }
        .stButton>button {
            width: 100%;
            background-color: #4CAF50;
            color: white;
            font-size: 18px;
            border-radius: 8px;
            height: 3em;
            transition: 0.3s;
            max-width: 480px;
            margin: 0 auto;
            display: block;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        .result-box {
            background-color: #FFF3CD;
            color: #000;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            font-weight: bold;
            font-size: 22px;
            margin-top: 15px;
            max-width: 480px;
            margin: 15px auto;
        }
        /* Centrer les autres éléments */
        .stNumberInput, .stRadio, .stSelectbox {
            max-width: 480px;
            margin: 0 auto 20px auto;
        }
    </style>
""", unsafe_allow_html=True)

# Titre principal
st.markdown("<h1>🏡 House Price Estimator</h1>", unsafe_allow_html=True)

# Conteneur principal sans le rectangle blanc
st.markdown("<div class='main'>", unsafe_allow_html=True)

area = st.number_input("Area (Square Feet)", min_value=100, value=2000, step=50)

col1, col2 = st.columns(2)
with col1:
    bhk = st.radio("Bedroom", [1, 2, 3, 4, 5], horizontal=True, index=1)
with col2:
    bath = st.radio("Bath", [1, 2, 3, 4, 5], horizontal=True, index=1)

location = st.selectbox(
    "Location",
    ["1st phase jp nagar", "2nd stage jp nagar", "5th block hbr layout", "other"],
    index=0
)

MODEL_PATHS = ["Projects_ML_DS/Project 1/banglore_home_prices_model.pickle"]
model = None
for path in MODEL_PATHS:
    if os.path.exists(path):
        try:
            with open(path, "rb") as f:
                model = pickle.load(f)
            break
        except Exception as e:
            st.warning(f"Erreur lors du chargement du modèle : {e}")

estimate = None
if st.button("Estimate Price"):
    input_data = pd.DataFrame([{
        "Area": area,
        "BHK": bhk,
        "Bath": bath,
        "Location": location
    }])

    if model:
        try:
            prediction = model.predict(input_data)[0]
            estimate = prediction
        except Exception as e:
            st.error("Erreur : les colonnes d'entrée ne correspondent pas à celles attendues par le modèle.")
            st.exception(e)
    else:
        base_price = 2.0
        estimate = (area / 1000) * base_price + (bhk - 1) * 0.5 + (bath - 1) * 0.3

if estimate is not None:
    st.markdown(f"<div class='result-box'>{estimate:.2f} Lakh</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)