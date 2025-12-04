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

df = pd.read_csv(csv_path, encoding="latin-1")

st.subheader("Vista general de los datos")
st.write("Columnas detectadas en el CSV:")
st.write(list(df.columns))
st.dataframe(df.head(), hide_index=True)

# ---------------------------------------------------------
# DETECCIÓN AUTOMÁTICA DE COLUMNAS CLAVE
# ---------------------------------------------------------
def detectar_columna(df, posibles_subcadenas):
    for col in df.columns:
        cl = col.lower()
        for p in posibles_subcadenas:
            if p in cl:
                return col
    return None

CITY_COL = detectar_columna(df, ["city", "ciudad"])
MONTH_COL = detectar_columna(df, ["month", "mes"])
TEMP_COL = detectar_columna(df, ["temp", "temperatura"])

if CITY_COL is None or MONTH_COL is None or TEMP_COL is None:
    st.error(
        "No pude identificar automáticamente las columnas de **ciudad**, "
        "**mes** o **temperatura**.\n\n"
        "Revisa los nombres de las columnas que aparecen arriba y asegúrate "
        "de que alguna contenga palabras como 'city/ciudad', 'month/mes' o "
        "'temp/temperatura'."
    )
    st.stop()

st.success(
    f"Usando columnas:\n\n"
    f"- Ciudad: **{CITY_COL}**\n"
    f"- Mes: **{MONTH_COL}**\n"
    f"- Temperatura: **{TEMP_COL}**"
)

st.subheader("Vista simplificada de los datos relevantes")
st.dataframe(df[[CITY_COL, MONTH_COL, TEMP_COL]].head(), hide_index=True)

# ---------------------------------------------------------
# CONTROLES DE LA INTERFAZ
# ---------------------------------------------------------
st.sidebar.header("Parámetros de predicción")

# Aseguramos que mes sea numérico (por si viene como texto)
df[MONTH_COL] = pd.to_numeric(df[MONTH_COL], errors="coerce")

# Lista de ciudades
ciudades = sorted(df[CITY_COL].dropna().unique())
ciudad_sel = st.sidebar.selectbox("Selecciona una ciudad:", ciudades)

# Diccionario de nombres bonitos de mes
nombres_meses = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
    5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}

meses_disp = sorted(df[MONTH_COL].dropna().unique())
meses_labels = [nombres_meses.get(int(m), str(int(m))) for m in meses_disp]
mes_label_sel = st.sidebar.selectbox("Selecciona el mes:", meses_labels)

# Convertir la etiqueta elegida al número de mes
mes_sel = None
for m, label in zip(meses_disp, meses_labels):
    if label == mes_label_sel:
        mes_sel = int(m)
        break

# ---------------------------------------------------------
# CÁLCULO DE LA PREDICCIÓN (PROMEDIO HISTÓRICO)
# ---------------------------------------------------------
df_ciudad = df[df[CITY_COL] == ciudad_sel].copy()

promedios_mes = (
    df_ciudad
    .groupby(MONTH_COL)[TEMP_COL]
    .mean()
    .reset_index()
    .sort_values(MONTH_COL)
)

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
        "Prueba con otro mes o revisa la columna de mes."
    )

st.write("""
La predicción se calcula como el **promedio histórico** de la temperatura
registrada para esa ciudad en el mes seleccionado.
""")

# ---------------------------------------------------------
# GRÁFICA DE EVOLUCIÓN POR MES
# ---------------------------------------------------------
st.subheader(f"Evolución histórica promedio por mes en {ciudad_sel}")

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
