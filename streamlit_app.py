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

# 2. Mensajes a descifrar (misma dinámica que el anterior)
MENSAJES = [
    {
        "titulo": "Mensaje 1",
        "cifrado": "🐱 🦄 ☀️ 🌊 🦖 🍕 🔒   🐼 ☀️ 🧀 🦄 🚀 🦖 🚀 🔒   🤖 🚀 🐱 🍕 🎸 🍦 🔒 🦖 🚀   ☀️ 🪀 🚀 🤖   🔒 🍦 🐵 🍕 🌊 ?",
        "respuesta": "CUANTOS PAQUETES RECOGISTE AYER SIMON",
    },
    {
        "titulo": "Mensaje 2 — Parte 1",
        "cifrado": "🦖 🦄   🌊 🍕 🐵 🎈 🤖 🚀",
        "respuesta": "TU NOMBRE",
    },
    {
        "titulo": "Mensaje 3 — Parte 2",
        "cifrado": "🦖 🦄   🎲 🚀 🐼 🍕 🤖 🦖 🚀   💥 ☀️ 🌋 🍕 🤖 🍦 🦖 🍕",
        "respuesta": "TU DEPORTE FAVORITO",
    },
    {
        "titulo": "Mensaje 4 — Parte 3",
        "cifrado": "🐱 🦄 ☀️ 🦁   🚀 🔒   🦖 🦄   🐼 🚀 🦁 🍦 🐱 🦄 🦁 ☀️   💥 ☀️ 🌋 🍕 🤖 🍦 🦖 ☀️",
        "respuesta": "CUAL ES TU PELICULA FAVORITA",
    },
]

for idx, m in enumerate(MENSAJES, start=1):
    st.subheader(f"✉️ {m['titulo']}")
    st.markdown(
        f"<div style='font-size:2rem; line-height:3rem; white-space:normal; word-wrap:break-word; overflow-wrap:anywhere;'>{m['cifrado']}</div>",
        unsafe_allow_html=True,
    )
    with st.form(f"form_descifrado_{idx}", clear_on_submit=False):
        respuesta = st.text_input("Establece el mensaje descifrado", key=f"resp_{idx}")
        enviado = st.form_submit_button("Submit")
    if enviado:
        normalizada = re.sub(r"\s+", " ", respuesta.upper().replace("¿", "").replace("?", "").replace(".", "").replace(",", "").strip())
        if normalizada == m["respuesta"]:
            st.balloons()
            st.success("¡Encontraste el mensaje! 🎉")
        else:
            st.error("Mensaje incorrecto, inténtalo de nuevo.")
