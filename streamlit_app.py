import pandas as pd
import streamlit as st
import altair as alt
# -------------------------------------------------------
# CONFIGURACIÓN DE LA APP
# -------------------------------------------------------
st.set_page_config(page_title="Temperatura México", page_icon="🌡️")

st.title("🌡️ Predicción de temperatura en ciudades de México")
st.write("""
Esta aplicación te permite predecir la temperatura mensual estimada
para diversas ciudades de México usando datos históricos.
""")
csv_path = "AmericaTemperaturesByCity.csv"

# Intentar leer el CSV con codificación latinoamericana
df = pd.read_csv(csv_path, encoding="latin-1")
# Si por alguna razón no funciona, prueba:
# df = pd.read_csv(csv_path, encoding="ISO-8859-1")






