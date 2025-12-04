import pandas as pd
import streamlit as st
import altair as alt

# ---------------------------------------------------------
# CONFIGURACIÓN DE LA APP
# ---------------------------------------------------------
st.set_page_config(page_title="Temperatura México", page_icon="🌡️")

st.title("🌡️ Predicción de temperatura en ciudades de México")
st.write("""
Esta aplicación te permite predecir la temperatura mensual estimada 
para diversas ciudades de México usando datos históricos.
""")

# ---------------------------------------------------------
# CARGA DE DATOS
# ---------------------------------------------------------
csv_path = "AmericaTemperaturesByCity.csv"

# 👀 IMPORTANTE:
# Si tu CSV usa otra codificación, ya corregimos el error de Unicode:
df = pd.read_csv(csv_path, encoding="latin-1")

# 👉 AJUSTA ESTOS NOMBRES SI EN TU CSV SON DIFERENTES
CITY_COL = "City"          # o "city", "Ciudad", etc.
MONTH_COL = "Month"        # o "Mes"
TEMP_COL = "Temperature"   # o "AvgTemperature", "Temp", etc.

# Si quieres, puedes renombrar aquí:
# df = df.rename(columns={
#     "NombreColCiudadEnTuCSV": CITY_COL,
#     "NombreColMesEnTuCSV": MONTH_COL,
#     "NombreColTempEnTuCSV": TEMP_COL
# })

st.subheader("Vista general de los datos")
st.dataframe(df[[CITY_COL, MONTH_COL, TEMP_COL]].head(), hide_index=True)

# ---------------------------------------------------------
# CONTROLES DE LA INTERFAZ
# ---------------------------------------------------------
st.sidebar.header("Parámetros de predicción")

# Lista de ciudades disponibles
ciudades = sorted(df[CITY_COL].dropna().unique())
ciudad_sel = st.sidebar.selectbox("Selecciona una ciudad:", ciudades)

# Nombres bonitos para los meses
nombres_meses = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
    5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}

# Asegurarnos de que la columna de mes es numérica
df[MONTH_COL] = pd.to_numeric(df[MONTH_COL], errors="coerce")

meses_disp = sorted(df[MONTH_COL].dropna().unique())
meses_labels = [nombres_meses.get(int(m), str(int(m))) for m in meses_disp]

mes_label_sel = st.sidebar.selectbox("Selecciona el mes:", meses_labels)

# Recuperar el número de mes a partir de la etiqueta elegida
mes_sel = None
for m, label in zip(meses_disp, meses_labels):
    if label == mes_label_sel:
        mes_sel = int(m)
        break

# ---------------------------------------------------------
# CÁLCULO DE LA "PREDICCIÓN"
# ---------------------------------------------------------
# Aquí usamos un modelo muy sencillo:
#   → promedio histórico de la temperatura para esa ciudad y ese mes.
df_ciudad = df[df[CITY_COL] == ciudad_sel].copy()

# Agrupar por mes y calcular promedio histórico
promedios_mes = (
    df_ciudad
    .groupby(MONTH_COL)[TEMP_COL]
    .mean()
    .reset_index()
    .sort_values(MONTH_COL)
)

# Buscar la temperatura estimada para el mes elegido
temp_estimada = None
fila_mes = promedios_mes[promedios_mes[MONTH_COL] == mes_sel]

if not fila_mes.empty:
    temp_estimada = float(fila_mes[TEMP_COL].values[0])

# ---------------------------------------------------------
# RESULTADO
# ---------------------------------------------------------
st.subheader("Predicción de temperatura mensual")

if temp_estimada is not None:
    st.metric(
        label=f"Temperatura estimada en {ciudad_sel} para {mes_label_sel}",
        value=f"{temp_estimada:.1f} °C"
    )
else:
    st.warning(
        "No hay datos suficientes para esa combinación de ciudad y mes. "
        "Prueba con otro mes o revisa que la columna de mes esté bien configurada."
    )

st.write("""
La predicción se calcula como el **promedio histórico** de la temperatura
registrada para esa ciudad en el mes seleccionado.
""")

# ---------------------------------------------------------
# GRÁFICA DE TODOS LOS MESES PARA LA CIUDAD ELEGIDA
# ---------------------------------------------------------
st.subheader(f"Evolución histórica promedio por mes en {ciudad_sel}")

# Agregar nombre de mes para mostrar bonito en la gráfica
promedios_mes["MesNombre"] = promedios_mes[MONTH_COL].apply(
    lambda x: nombres_meses.get(int(x), str(int(x)))
)

chart = (
    alt.Chart(promedios_mes)
    .mark_line(point=True)
    .encode(
        x=alt.X("MesNombre", title="Mes"),
        y=alt.Y(TEMP_COL, title="Temperatura promedio (°C)"),
        tooltip=["MesNombre", TEMP_COL]
    )
)

st.altair_chart(chart, use_container_width=True)



