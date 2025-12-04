import streamlit as st
import pandas as pd
import pickle

# -------------------------
# Cargar modelo y columnas
# -------------------------
with open("modelo_temp.pkl", "rb") as f:
    modelo = pickle.load(f)

with open("columnas.pkl", "rb") as f:
    columnas_modelo = pickle.load(f)

# -------------------------
# Cargar dataset original
# -------------------------
df = pd.read_csv("AmericaTemperaturesByCity.csv")

# IMPORTANTE:
# Ajusta ESTE nombre a como venga en tu dataset:
col_ciudad = "Location"   # <-- CAMBIAR si es necesario

df_mex = df[df["Country"] == "Mexico"].copy()

# -------------------------
# Interfaz Streamlit
# -------------------------
st.title("🌡️ Predicción de Temperatura en Ciudades de México 🇲🇽")

st.image("mexico.png", caption="Clima en México")

st.write("Selecciona los datos para obtener la temperatura estimada.")

# Ciudades disponibles
ciudades = sorted(df_mex[col_ciudad].unique())

ciudad = st.selectbox("Ciudad:", ciudades)
mes = st.number_input("Mes (1-12):", min_value=1, max_value=12, step=1)
año = st.number_input("Año:", min_value=1900, max_value=2100, step=1)

# -------------------------
# Botón para predecir
# -------------------------
if st.button("Predecir temperatura"):

    nueva = pd.DataFrame([[año, mes, ciudad]],
                         columns=["year", "month", col_ciudad])

    # Dummies de ciudad
    nueva = pd.get_dummies(nueva, columns=[col_ciudad], drop_first=False)

    # Asegurar columnas del modelo
    for col in columnas_modelo:
        if col not in nueva.columns:
            nueva[col] = 0

    nueva = nueva[columnas_modelo]

    resultado = modelo.predict(nueva)[0]

    st.subheader(f"🌞 Temperatura estimada: {resultado:.2f} °C")

