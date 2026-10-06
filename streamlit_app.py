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


# ============================================================
# Módulo 2: Cifrado Emoji (Abecedario Emoji)
# ============================================================
import re

st.divider()
st.header("🔑 Cifrado Emoji — Tabla Decodificadora")

# Tabla oficial Letra -> Emoji
LETRA_A_EMOJI = {
    "A": "☀️", "B": "🎈", "C": "🐱", "D": "🎲", "E": "🚀",
    "F": "💥", "G": "🎸", "H": "🚁", "I": "🍦", "J": "🕹️",
    "K": "🥋", "L": "🦁", "M": "🐵", "N": "🌊", "Ñ": "🍍",
    "O": "🍕", "P": "🐼", "Q": "🧀", "R": "🤖", "S": "🔒",
    "T": "🦖", "U": "🦄", "V": "🌋", "W": "🧇", "X": "⚔️",
    "Y": "🪀", "Z": "⚡",
}
EMOJI_A_LETRA = {v: k for k, v in LETRA_A_EMOJI.items()}


def codificar_emoji(texto: str) -> str:
    """Texto plano -> emojis. Letras separadas por 1 espacio, palabras por 3 espacios."""
    texto = texto.upper().strip()
    palabras = re.split(r"\s+", texto)
    palabras_cod = []
    for pal in palabras:
        emojis = [LETRA_A_EMOJI[l] for l in pal if l in LETRA_A_EMOJI]
        # Conservar signos como ? ! . , al final sin codificar
        signos = "".join(c for c in pal if c not in LETRA_A_EMOJI and not c.isalnum())
        cod = " ".join(emojis)
        if signos:
            cod = (cod + " " + signos).strip()
        if cod:
            palabras_cod.append(cod)
    return "   ".join(palabras_cod)


def decodificar_emoji(cadena: str) -> str:
    """Emojis -> texto plano. Soporta 2+ espacios como separador de palabra."""
    if not cadena:
        return ""
    s = cadena.strip()
    # Reemplazar cada emoji por su letra (ordenar por longitud desc por VS16: ☀️, 🕹️, ⚔️)
    for emoji in sorted(EMOJI_A_LETRA, key=len, reverse=True):
        s = s.replace(emoji, EMOJI_A_LETRA[emoji])
    # Separadores alternativos: / | como corte de palabra
    s = s.replace("/", "   ").replace("|", "   ")
    # Cortar palabras por 2+ espacios, luego quitar espacios simples entre letras
    palabras = re.split(r"\s{2,}", s.strip())
    if len(palabras) == 1 and " " in s:
        # Si el usuario usó 1 solo espacio también como separador de palabra,
        # no podemos distinguirlo; se asume 1 espacio = separación de letra.
        # Se devuelve sin colapsar palabras para inspección.
        pass
    limpias = [p.replace(" ", "") for p in palabras]
    return " ".join(limpias)


# 1. Tabla de equivalencia
st.subheader("📖 Tabla de equivalencia Letra ↔ Emoji")
df_tabla = pd.DataFrame(
    [{"Letra": k, "Emoji": v} for k, v in LETRA_A_EMOJI.items()]
)
st.dataframe(df_tabla, use_container_width=True, hide_index=True)

# 2. Validación del mensaje dado
st.subheader("✉️ Validación del mensaje cifrado dado")
MENSAJE_CIFRADO = "🐱 🦄 ☀️ 🌊 🦖 🍕 🔒   🐼 ☀️ 🧀 🚀 🦖 🚀 🔒   🤖 🚀 🐱 🍕 🎸 🍦 🔒 🦖 🚀   ☀️ 🪀 🚀 🤖   🔒 🍦 🐵 🍕 🌊 ?"
ESPERADO_PALABRAS = ["CUANTOS", "PAQUETES", "RECOGISTE", "AYER", "SIMON"]

st.code(MENSAJE_CIFRADO)
palabras_cifradas = re.split(r"\s{3,}", MENSAJE_CIFRADO.strip())
resultado_val = []
for pc in palabras_cifradas:
    # quitar el "?" suelto de la última palabra para comparar
    pc_limpio = pc.replace("?", "").strip()
    resultado_val.append(decodificar_emoji(pc_limpio))

df_val = pd.DataFrame({
    "Palabra cifrada": palabras_cifradas,
    "Decodificado": resultado_val,
    "Esperado": ESPERADO_PALABRAS,
})
# cálculo simple de check
df_val["✔"] = ["✅" if d == e else "❌" for d, e in zip(resultado_val, ESPERADO_PALABRAS)]
st.dataframe(df_val, use_container_width=True, hide_index=True)

if resultado_val == ESPERADO_PALABRAS:
    st.success(f"Mensaje válido: {' '.join(resultado_val)}")
else:
    st.warning(
        f"Decodificado real: {' '.join(resultado_val)} — "
        "no coincide 100% con lo esperado."
    )
    st.info(
        "Detalle: palabra 2 decodifica como `PAQETES` (P-A-Q-E-T-E-S, 7 emojis), "
        "falta la `U (🦄)`. Para `PAQUETES` debería ser: "
        "🐼 ☀️ 🧀 🦄 🚀 🦖 🚀 🔒"
    )

st.subheader("🧪 Prueba la corrección sugerida")
correccion = "🐼 ☀️ 🧀 🦄 🚀 🦖 🚀 🔒"
st.code(correccion)
st.write(f"Decodifica como: **{decodificar_emoji(correccion)}** (esperado: PAQUETES ✅)")

# 3. Codificar: texto -> emoji
st.subheader("⌨️ Codificar (texto → emoji)")
texto_plano = st.text_input("Escribe texto (A-Z, Ñ, espacios)", value="PAQUETES")
if texto_plano:
    st.code(codificar_emoji(texto_plano))

# 4. Decodificar: input por emoji (teclado emoji + botones)
st.subheader("👆 Input por emoji (emoji → texto)")
st.caption("Pega emojis abajo O construye el mensaje tocando los botones.")

if "emoji_buffer" not in st.session_state:
    st.session_state.emoji_buffer = ""

# Botonera de emojis: 6 por fila
letras = list(LETRA_A_EMOJI.keys())
cols = st.columns(6)
for i, letra in enumerate(letras):
    emoji = LETRA_A_EMOJI[letra]
    if cols[i % 6].button(f"{emoji}\n{letra}", key=f"btn_{letra}"):
        sep = "" if st.session_state.emoji_buffer == "" or st.session_state.emoji_buffer.endswith("   ") else " "
        st.session_state.emoji_buffer += sep + emoji
        st.rerun()

c1, c2, c3 = st.columns(3)
if c1.button("➕ Espacio palabra"):
    st.session_state.emoji_buffer += "   "
    st.rerun()
if c2.button("⌫ Borrar último"):
    st.session_state.emoji_buffer = st.session_state.emoji_buffer.rstrip()[:-1].rstrip()
    st.rerun()
if c3.button("🗑️ Limpiar"):
    st.session_state.emoji_buffer = ""
    st.rerun()

entrada_emoji = st.text_area(
    "Entrada emoji (editable, también sirve pegar aquí):",
    value=st.session_state.emoji_buffer,
    height=100,
)
# sincronizar lo pegado con el buffer
st.session_state.emoji_buffer = entrada_emoji

if entrada_emoji.strip():
    st.write(f"Decodificado: **{decodificar_emoji(entrada_emoji)}**")
else:
    st.caption("Toca emojis para empezar a cifrar/descifrar.")
