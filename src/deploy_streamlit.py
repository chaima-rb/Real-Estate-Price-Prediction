import streamlit as st
import pandas as pd
import pickle
import os

# --- Configuration de la page ---
st.set_page_config(page_title=" House Price Estimator", layout="centered")

# --- Titre principal ---
st.title(" House Price Estimator")

# --- Entrées principales ---

# Bloc du milieu : Area
area = st.number_input("Area (Square Feet)", min_value=100, value=2000, step=50)
# --- Bedroom au-dessus de Bath (empilés verticalement) ---
st.subheader("Bedroom")
bhk = st.radio("", [1, 2, 3, 4, 5], horizontal=True, index=1, key="bhk_radio")

st.subheader("Bath")
bath = st.radio("", [1, 2, 3, 4, 5], horizontal=True, index=1, key="bath_radio")

# --- Localisation ---
location = st.selectbox(
    "Location",
    ["1st phase jp nagar", "2nd stage jp nagar", "5th block hbr layout", "other"],
    index=0
)

# --- Chargement du modèle ---
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

# --- Prédiction ---
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

# --- Résultat ---
if estimate is not None:
    st.success(f"Estimated Price: {estimate:.2f} Lakh")
