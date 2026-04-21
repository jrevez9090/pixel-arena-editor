import streamlit as st
import json

st.set_page_config(layout="wide")

st.title("🎮 Pixel Arena Editor")

# Escolher tamanho
width = st.selectbox("Largura", [12, 16])
height = st.selectbox("Altura", [24, 32, 40])

# Cores
colors = {
    "🟩": 0,
    "🟦": 1,
    "🟥": 2,
    "🟪": 3
}

selected = st.radio("Cor", list(colors.keys()))
selected_color = colors[selected]

# Criar grid
if "grid" not in st.session_state:
    st.session_state.grid = [[-1]*width for _ in range(height)]

# Reset se mudar tamanho
if len(st.session_state.grid) != height or len(st.session_state.grid[0]) != width:
    st.session_state.grid = [[-1]*width for _ in range(height)]

st.write("### Editor")

for y in range(height):
    cols = st.columns(width)
    for x in range(width):
        val = st.session_state.grid[y][x]

        emoji = "⬜"
        if val == 0: emoji = "🟩"
        if val == 1: emoji = "🟦"
        if val == 2: emoji = "🟥"
        if val == 3: emoji = "🟪"

        if cols[x].button(emoji, key=f"{x}-{y}"):
            st.session_state.grid[y][x] = selected_color

# Exportar
def export():
    matrix = []
    for y, row in enumerate(st.session_state.grid):
        for x, val in enumerate(row):
            if val != -1:
                matrix.append([x, y, "id", {"color": val, "points": [[0,0]]}])
    return matrix

if st.button("Exportar"):
    data = export()
    st.download_button("Download JSON", json.dumps(data), "level.json")
