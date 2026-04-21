import streamlit as st
import json

st.set_page_config(layout="wide")

st.title("🎮 Pixel Arena Editor (PRO)")

# =========================
# CONFIG
# =========================
col1, col2 = st.columns(2)

with col1:
    width = st.selectbox("Largura", [12, 16])
with col2:
    height = st.selectbox("Altura", [24, 32, 40])

colors = {
    "🟩 Seguro": 0,
    "🟦 Pontos": 1,
    "🟥 Perigo": 2,
    "🟪 Double": 3
}

selected = st.radio("Cor", list(colors.keys()))
selected_color = colors[selected]

mode = st.radio("Modo", ["➕ Pintar", "➖ Apagar"])

# =========================
# GRID STATE
# =========================
if "grid" not in st.session_state:
    st.session_state.grid = [[-1]*width for _ in range(height)]

if len(st.session_state.grid) != height or len(st.session_state.grid[0]) != width:
    st.session_state.grid = [[-1]*width for _ in range(height)]

# =========================
# CSS CORRIGIDO (QUADRADOS)
# =========================
st.markdown("""
<style>
div[data-testid="stButton"] button {
    width: 20px !important;
    height: 20px !important;
    padding: 0 !important;
    margin: 0 !important;
    border-radius: 0px !important;   /* 🔥 remove formato oval */
    border: 1px solid #333 !important;
    font-size: 10px !important;
    line-height: 1 !important;
}

div[data-testid="stButton"] {
    display: inline-block;
}

/* reduzir espaço entre colunas */
[data-testid="column"] {
    padding: 0px !important;
}

/* centralizar melhor */
.block-container {
    padding-top: 1rem;
}
</style>
""", unsafe_allow_html=True)

# =========================
# CENTRALIZAR GRID
# =========================
left, center, right = st.columns([1,2,1])

with center:

    # eixo X topo
    cols = st.columns([0.3] + [1]*width + [0.3])
    for i in range(width):
        cols[i+1].markdown(f"<div style='text-align:center;font-size:10px'>{i+1}</div>", unsafe_allow_html=True)

    # grid
    for y in range(height):

        row = st.columns([0.3] + [1]*width + [0.3])

        # eixo Y esquerda
        row[0].markdown(f"<div style='font-size:10px'>{y+1}</div>", unsafe_allow_html=True)

        for x in range(width):
            val = st.session_state.grid[y][x]

            color = "⬛"
            if val == 0: color = "🟩"
            elif val == 1: color = "🟦"
            elif val == 2: color = "🟥"
            elif val == 3: color = "🟪"

            if row[x+1].button(color, key=f"{x}-{y}"):

                if mode == "➕ Pintar":
                    st.session_state.grid[y][x] = selected_color
                else:
                    st.session_state.grid[y][x] = -1

        # eixo Y direita
        row[-1].markdown(f"<div style='font-size:10px'>{y+1}</div>", unsafe_allow_html=True)

    # eixo X baixo
    cols = st.columns([0.3] + [1]*width + [0.3])
    for i in range(width):
        cols[i+1].markdown(f"<div style='text-align:center;font-size:10px'>{i+1}</div>", unsafe_allow_html=True)

# =========================
# EXPORT
# =========================
def export_grid(grid):
    matrix = []
    for y, row in enumerate(grid):
        for x, val in enumerate(row):
            if val != -1:
                matrix.append([x, y, "id", {"color": val, "points": [[0,0]]}])
    return matrix

st.markdown("---")

if st.button("💾 Exportar JSON"):
    data = export_grid(st.session_state.grid)
    st.download_button(
        "Download JSON",
        json.dumps(data, indent=2),
        "level.json"
    )
