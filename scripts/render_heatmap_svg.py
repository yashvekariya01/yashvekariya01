import json

def render_heatmap():
    try:
        with open("data/contributions.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    palette = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
    
    rects = ""
    col = 0
    row = 0
    for i, item in enumerate(data):
        level = item.get("level", 0)
        color = palette[min(level, 4)]
        x = col * 15 + 20
        y = row * 15 + 20
        rects += f'<rect x="{x}" y="{y}" width="11" height="11" rx="2" fill="{color}" />\n'
        row += 1
        if row == 7:
            row = 0
            col += 1

    svg = f"""<svg width="860" height="150" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" fill="#0d1117" rx="10" stroke="#30363d"/>
  <g transform="translate(10, 10)">
    {rects}
  </g>
</svg>"""

    with open("contrib-heatmap.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("contrib-heatmap.svg generated!")

if __name__ == "__main__":
    render_heatmap()