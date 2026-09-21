# import streamlit as st

# st.title("Hello Streamlit-er 👋")
# st.markdown(
#     """ 
#     This is a playground for you to try Streamlit and have fun. 

#     **There's :rainbow[so much] you can build!**
    
#     We prepared a few examples for you to get started. Just 
#     click on the buttons above and discover what you can do 
#     with Streamlit. 
#     """
# )

# if st.button("Send balloons!"):
#     st.balloons()


import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Configuración del título de la app
st.title("🎬 Análisis de Calificación vs. Ingresos en IMDb")

# Cargar el archivo de datos (Asegúrate de que el CSV esté en el mismo directorio)
@st.cache_data
def cargar_datos():
    return pd.read_csv('IMDB-Movie-Data.csv')

df = cargar_datos()

st.subheader("Hipótesis 3: Relación entre Calificación e Ingresos")

# 1. Seleccionar columnas necesarias y limpiar nulos
df_h3 = df[['Rating', 'Revenue (Millions)', 'Votes']].dropna().copy()

# 2. Crear categoría para filtrar películas con Rating alto vs normal
df_h3['Calificacion_Alta'] = df_h3['Rating'] >= 8.0

# 3. Agrupar para comparar promedios
comparativa = df_h3.groupby('Calificacion_Alta')['Revenue (Millions)'].mean().reset_index()
comparativa['Calificacion_Alta'] = comparativa['Calificacion_Alta'].map({
    True: 'Excelente (≥ 8.0)', 
    False: 'Promedio (< 8.0)'
})
comparativa.rename(columns={'Revenue (Millions)': 'Ingreso Promedio ($M)'}, inplace=True)

# --- INTERFAZ WEB EN STREAMLIT ---

# Crear dos columnas en la interfaz para mostrar la tabla y métricas
col1, col2 = st.columns([1, 1])

with col1:
    st.write("### Tabla Comparativa")
    st.dataframe(comparativa, use_container_width=True)

with col2:
    st.write("### Resumen")
    rev_excelente = comparativa[comparativa['Calificacion_Alta'] == 'Excelente (≥ 8.0)']['Ingreso Promedio ($M)'].values[0]
    rev_promedio = comparativa[comparativa['Calificacion_Alta'] == 'Promedio (< 8.0)']['Ingreso Promedio ($M)'].values[0]
    
    st.metric(label="Ingreso Promedio (Excelente)", value=f"${rev_excelente:.2f} M")
    st.metric(label="Ingreso Promedio (Promedio)", value=f"${rev_promedio:.2f} M", delta=f"{rev_excelente - rev_promedio:.2f} M")

# 4. Visualización con Matplotlib
st.write("### Gráfico de Dispersión")
fig, ax = plt.subplots(figsize=(8, 4))
ax.scatter(df_h3['Rating'], df_h3['Revenue (Millions)'], alpha=0.5, color='purple')
ax.set_title('Relación entre Calificación (Rating) e Ingresos (Revenue)')
ax.set_xlabel('Calificación IMDb')
ax.set_ylabel('Ingresos ($M)')
ax.grid(True, linestyle='--', alpha=0.6)

# Renderizar el gráfico en Streamlit
st.pyplot(fig)
