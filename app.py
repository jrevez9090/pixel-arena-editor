import streamlit as st
import json
import streamlit.components.v1 as components

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
# CLICK HANDLER
# =========================
params = st.query_params

if "click" in params:
    try:
        y, x = map(int, params["click"].split(","))

        if mode == "➕ Pintar":
            st.session_state.grid[y][x] = selected_color
        else:
            st.session_state.grid[y][x] = -1

        # limpar param
        st.query_params.clear()

        # 💥 força refresh
        st.rerun()

    except:
        pass

# =========================
# GRID VISUAL
# =========================
def render_editor(grid):
    grid_json = json.dumps(grid)

    html = f"""
    <style>
    .wrapper {{
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
    }}

    .editor {{
        display: grid;
        grid-template-columns: 40px repeat({width}, 18px) 40px;
        grid-template-rows: 20px repeat({height}, 18px) 20px;
        gap: 1px;
        background: #111;
        padding: 10px;
    }}

    .cell {{
        width: 18px;
        height: 18px;
        border: 1px solid #222;
        cursor: pointer;
    }}

    .axis {{
        font-size: 10px;
        color: #aaa;
        display: flex;
        justify-content: center;
        align-items: center;
    }}
    </style>

    <div class="wrapper">
        <div class="editor" id="editor"></div>
    </div>

    <script>
    const gridData = {grid_json};
    const width = {width};
    const height = {height};

    function getColor(val) {{
        if(val === 0) return "green";
        if(val === 1) return "blue";
        if(val === 2) return "red";
        if(val === 3) return "purple";
        return "#111";
    }}

    const container = document.getElementById("editor");

    function draw() {{
        container.innerHTML = "";

        for(let y = -1; y <= height; y++) {{
            for(let x = -1; x <= width; x++) {{

                let div = document.createElement("div");

                if((x === -1 && y === -1) || (x === width && y === -1) ||
                   (x === -1 && y === height) || (x === width && y === height)) {{
                    div.className = "axis";
                }}

                else if(y === -1 && x >= 0 && x < width) {{
                    div.className = "axis";
                    div.innerText = x + 1;
                }}

                else if(y === height && x >= 0 && x < width) {{
                    div.className = "axis";
                    div.innerText = x + 1;
                }}

                else if(x === -1 && y >= 0 && y < height) {{
                    div.className = "axis";
                    div.innerText = y + 1;
                }}

                else if(x === width && y >= 0 && y < height) {{
                    div.className = "axis";
                    div.innerText = y + 1;
                }}

                else {{
                    div.className = "cell";
                    div.style.background = getColor(gridData[y][x]);

                    div.onclick = () => {{
                        const url = new URL(window.parent.location);
                        url.searchParams.set("click", y + "," + x);
                        window.parent.location.href = url.toString();
                    }}
                }}

                container.appendChild(div);
            }}
        }}
    }}

    draw();
    </script>
    """

    components.html(html, height=900, scrolling=True)

render_editor(st.session_state.grid)

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
