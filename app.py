import streamlit as st
import json
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

st.title("🎮 Pixel Arena Editor (PRO)")

# =========================
# CONFIG
# =========================
width = st.selectbox("Largura", [12, 16])
height = st.selectbox("Altura", [24, 32, 40])

colors = {
    "🟩": 0,
    "🟦": 1,
    "🟥": 2,
    "🟪": 3
}

selected = st.radio("Cor", list(colors.keys()))
selected_color = colors[selected]

# =========================
# GRID STATE
# =========================
if "grid" not in st.session_state:
    st.session_state.grid = [[-1]*width for _ in range(height)]

if len(st.session_state.grid) != height or len(st.session_state.grid[0]) != width:
    st.session_state.grid = [[-1]*width for _ in range(height)]

# =========================
# GRID VISUAL + CLICK
# =========================
def render_editor(grid, selected_color):
    grid_json = json.dumps(grid)

    html = f"""
    <style>
    .grid {{
        display: grid;
        grid-template-columns: repeat({width}, 18px);
        gap: 1px;
    }}

    .cell {{
        width: 18px;
        height: 18px;
        border: 1px solid #222;
        cursor: pointer;
    }}
    </style>

    <div class="grid" id="grid"></div>

    <script>
    const gridData = {grid_json};
    const selectedColor = {selected_color};

    function getColor(val) {{
        if(val === 0) return "green";
        if(val === 1) return "blue";
        if(val === 2) return "red";
        if(val === 3) return "purple";
        return "#111";
    }}

    const container = document.getElementById("grid");

    function drawGrid() {{
        container.innerHTML = "";
        for(let y=0; y<gridData.length; y++) {{
            for(let x=0; x<gridData[y].length; x++) {{

                let cell = document.createElement("div");
                cell.className = "cell";
                cell.style.background = getColor(gridData[y][x]);

                cell.onclick = () => {{
                    gridData[y][x] = selectedColor;
                    cell.style.background = getColor(selectedColor);
                }}

                container.appendChild(cell);
            }}
        }}
    }}

    drawGrid();
    </script>
    """

    components.html(html, height=800, scrolling=True)

render_editor(st.session_state.grid, selected_color)

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

if st.button("💾 Exportar JSON"):
    data = export_grid(st.session_state.grid)
    st.download_button("Download", json.dumps(data, indent=2), "level.json")
