import altair as alt
import pandas as pd
import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Temperatura Mexico", page_icon="🎬")
st.title("Temperatura Mexico")
st.write("""
En esta página podrás predecir las temperaturas de las ciudades de Mexico.
""")
# Ruta del archivo CSV
csv_path = "AmericaTemperaturesByCity.csv"

# Cargar el archivo CSV
df = pd.read_csv(csv_path)

# FILTRAR SOLO MÉXICO
df = df[df["country"] == "Mexico"].copy()

# Verificar columnas disponibles
# IMPORTANTE: no todos los archivos tienen “city”, así que revisamos el nombre correcto
print(df.columns)
