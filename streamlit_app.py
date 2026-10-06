import re
import pandas as pd
import streamlit as st

st.title("🔑 Cifrado Emoji")

LETRA_A_EMOJI = {
    "A": "☀️", "B": "🎈", "C": "🐱", "D": "🎲", "E": "🚀",
    "F": "💥", "G": "🎸", "H": "🚁", "I": "🍦", "J": "🕹️",
    "K": "🥋", "L": "🦁", "M": "🐵", "N": "🌊", "Ñ": "🍍",
    "O": "🍕", "P": "🐼", "Q": "🧀", "R": "🤖", "S": "🔒",
    "T": "🦖", "U": "🦄", "V": "🌋", "W": "🧇", "X": "⚔️",
    "Y": "🪀", "Z": "⚡",
}

# 1. Tabla
st.subheader("📖 Tabla Letra ↔ Emoji")
df_tabla = pd.DataFrame(
    [{"Letra": k, "Emoji": v} for k, v in LETRA_A_EMOJI.items()]
)
st.dataframe(df_tabla, use_container_width=True, hide_index=True)

# 2. Frase con emojis a descifrar
st.subheader("✉️ Mensaje a descifrar")
MENSAJE_CIFRADO = "🐱 🦄 ☀️ 🌊 🦖 🍕 🔒   🐼 ☀️ 🧀 🦄 🚀 🦖 🚀 🔒   🤖 🚀 🐱 🍕 🎸 🍦 🔒 🦖 🚀   ☀️ 🪀 🚀 🤖   🔒 🍦 🐵 🍕 🌊 ?"
st.markdown(
    f"<div style='font-size:2rem; line-height:3rem; white-space:normal; word-wrap:break-word; overflow-wrap:anywhere;'>{MENSAJE_CIFRADO}</div>",
    unsafe_allow_html=True,
)

# 3. Input + submit con validación
st.subheader("⌨️ Tu respuesta")
RESPUESTA_CORRECTA = "CUANTOS PAQUETES RECOGISTE AYER SIMON"

with st.form("form_descifrado", clear_on_submit=False):
    respuesta = st.text_input("Establece el mensaje descifrado")
    enviado = st.form_submit_button("Submit")

if enviado:
    normalizada = re.sub(r"\s+", " ", respuesta.upper().replace("¿", "").replace("?", "").replace(".", "").replace(",", "").strip())
    if normalizada == RESPUESTA_CORRECTA:
        st.balloons()
        st.success("¡Encontraste el mensaje! 🎉")
    else:
        st.error("Mensaje incorrecto, inténtalo de nuevo.")
