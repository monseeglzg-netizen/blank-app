import pandas as pd
import streamlit as st

# -------------------------------------------------------
# CONFIGURACIÓN DE LA APP
# -------------------------------------------------------
st.set_page_config(page_title="Temperatura México", page_icon="🌡️")

st.title("🌡️ Predicción de temperatura en ciudades de México")
st.write("""
Esta aplicación te permite predecir la temperatura mensual estimada
para diversas ciudades de México usando datos históricos.
""")
# -------------------------------------------------------
# CARGAR ARCHIVO CSV
# -------------------------------------------------------
csv_path = "AmericaTemperaturesByCity.csv"
# -------------------------------------------------------
# FILTRAR SOLO MÉXICO
# -------------------------------------------------------
if "country" not in df.columns:


