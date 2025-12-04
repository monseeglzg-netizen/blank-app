import pandas as pd
import streamlit as st
import altair as alt

# ---------------------------------------------------------
# CONFIGURACIÓN DE LA APP
# ---------------------------------------------------------
st.set_page_config(page_title="Temperatura México", page_icon="🌡️")

st.title("🌡️ Predicción de temperatura en ciudades de México")
st.write("""
Esta aplicación te permite predecir la temperatura estimada 
para distintas ciudades de México usando datos históricos.
""")

# ---------------------------------------------------------
# CARGA DE DATOS
# ---------------------------------------------------------
csv_path = "AmericaTemperaturesByCity.csv"

df = pd.read_csv(csv_path, encoding="latin-1")

st.subheader("Vista general de los datos (primeras filas)")
st.dataframe(df.head(), hide_index=True)

# ---------------------------------------------------------
# SELECCIÓN DE COLUMNAS (TÚ LAS ESCOGES)
# ---------------------------------------------------------
st.sidebar.header("Configuración de columnas")

cols = list(df.columns)

city_col = st.sidebar.selectbox(
    "Columna que representa la CIUDAD:",
    cols,
    index=0
)

time_col = st.sidebar.selectbox(
    "Columna que representa el MES / PERIODO:",
    cols,
    index=1 if len(cols) > 1 else 0
)

temp_col = st.sidebar.selectbox(
    "Columna que representa la TEMPERATURA:",
    cols,
    index=2 if len(cols) > 2 else 0
)

st.write(f"**Usando columnas:** ciudad = `{city_col}`, periodo = `{time_col}`, temperatura = `{temp_col}`")

# ---------------------------------------------------------
# CONTROLES DE PREDICCIÓN
# ---------------------------------------------------------
st.sidebar.header("Parámetros de predicción")

# Lista de ciudades
ciudades = sorted(df[city_col].dropna().unique())
ciudad_sel = st.sidebar.selectbox("Selecciona una ciudad:", ciudades)

# Lista de periodos (pueden ser meses, fechas, etc.)
periodos = sorted(df[time_col].dropna().unique())
periodo_sel = st.sidebar.selectbox("Selecciona el mes / periodo:", periodos)

# ---------------------------------------------------------
# CÁLCULO DE LA "PREDICCIÓN" (PROMEDIO HISTÓRICO)
# ---------------------------------------------------------
# Filtrar por ciudad
df_ciudad = df[df[city_col] == ciudad_sel].copy()

# Agrupar por periodo y calcular promedio histórico de temperatura
promedios_periodo = (
    df_ciudad
    .groupby(time_col)[temp_col]
    .mean()
    .reset_index()
    .sort_values(time_col)
)

# Buscar el valor estimado para el periodo elegido
fila_per = promedios_periodo[promedios_periodo[time_col] == periodo_sel]

if not fila_per.empty:
    temp_estimada = float(fila_per[temp_col].values[0])
else:
    temp_estimada = None

# ---------------------------------------------------------
# RESULTADO
# ---------------------------------------------------------
st.subheader("Predicción de temperatura")

if temp_estimada is not None:
    st.metric(
        label=f"Temperatura estimada en {ciudad_sel} para {periodo_sel}",
        value=f"{temp_estimada:.2f} °C"
    )
else:
    st.warning(
        "No hay datos suficientes para esa combinación de ciudad y periodo. "
        "Prueba con otro periodo o revisa la selección de columnas."
    )

st.write("""
La predicción se calcula como el **promedio histórico** de la temperatura
registrada para esa ciudad en el periodo seleccionado.
""")

# ---------------------------------------------------------
# GRÁFICA DE EVOLUCIÓN DE TEMPERATURA POR PERIODO
# ---------------------------------------------------------
st.subheader(f"Evolución histórica promedio por periodo en {ciudad_sel}")

chart = (
    alt.Chart(promedios_periodo)
    .mark_line(point=True)
    .encode(
        x=alt.X(time_col, title="Periodo (mes, fecha, etc.)"),
        y=alt.Y(temp_col, title="Temperatura promedio (°C)"),
        tooltip=[time_col, temp_col]
    )
)

st.altair_chart(chart, use_container_width=True)
