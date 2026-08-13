import os
import json
from datetime import datetime

def generate_heatmap_svg(input_path="data/contributions.json", output_path="contrib-heatmap.svg"):
    # Load contributions
    total_contributions = 0
    days = []
    if os.path.exists(input_path):
        try:
            with open(input_path, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
                if isinstance(raw_data, dict):
                    total_contributions = raw_data.get("total_contributions", 0)
                    days = raw_data.get("days", [])
                else:
                    days = raw_data
                    total_contributions = len(days) # Fallback
        except Exception as e:
            print(f"Error parsing contributions file: {e}")
    else:
        print(f"Warning: {input_path} not found. Using empty data.")

    # Sort days by date to ensure correct grid positioning
    days.sort(key=lambda x: x.get("date", ""))

    # Dimensions
    svg_width = 860
    svg_height = 205

    # Group days into weeks of 7
    weeks = [days[i:i+7] for i in range(0, len(days), 7)]

    # Styles and Palette (GitHub standard dark-theme green palette)
    palette = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
    
    # Stagger animation parameters
    base_delay = 0.012
    anim_duration = 0.4

    # Generate rects and month labels
    rects = []
    month_labels = []
    current_month = None

    for col, week in enumerate(weeks):
        if week:
            # Add month label when month changes (spaced)
            try:
                date_str = week[0]["date"]
                dt = datetime.strptime(date_str, "%Y-%m-%d")
                month_name = dt.strftime("%b")
                if month_name != current_month:
                    current_month = month_name
                    label_x = col * 15 + 40
                    month_labels.append(f'<text x="{label_x}" y="50" class="meta-text">{month_name}</text>')
            except Exception:
                pass

            for row, item in enumerate(week):
                level = item.get("level", 0)
                color = palette[min(level, 4)]
                
                x_pos = col * 15 + 40
                y_pos = row * 15 + 62
                
                # Diagonal stagger delay calculation
                delay = round((col + row) * base_delay, 3)
                
                rects.append(
                    f'    <rect x="{x_pos}" y="{y_pos}" width="11" height="11" rx="2.2" fill="{color}" opacity="0">\n'
                    f'      <animate attributeName="opacity" from="0" to="1" dur="{anim_duration}s" begin="{delay}s" fill="freeze" />\n'
                    f'      <animateTransform attributeName="transform" type="translate" from="0, 8" to="0, 0" dur="{anim_duration}s" begin="{delay}s" fill="freeze" additive="sum" />\n'
                    f'    </rect>'
                )

    rects_str = "\n".join(rects)
    months_str = "\n  ".join(month_labels)

    # SVG layout
    svg_content = f"""<svg width="{svg_width}" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <style>
    .bg {{ fill: #0d1117; rx: 10px; }}
    .border {{ stroke: #30363d; stroke-width: 1px; }}
    .title {{ font: bold 12px 'Fira Code', monospace; fill: #58a6ff; }}
    .meta-text {{ font: 9px 'Fira Code', monospace; fill: #8b949e; }}
  </style>

  <rect width="100%" height="100%" class="bg border" />

  <!-- MacOS-style terminal buttons -->
  <g transform="translate(15, 18)">
    <circle cx="0" cy="0" r="4.5" fill="#ff5f56" />
    <circle cx="12" cy="0" r="4.5" fill="#ffbd2e" />
    <circle cx="24" cy="0" r="4.5" fill="#27c93f" />
    <text x="40" y="4" class="title">yash@github: ~/contributions</text>
  </g>

  <!-- Total contributions count -->
  <text x="{svg_width - 20}" y="50" class="meta-text" text-anchor="end">{total_contributions} contributions in the last year</text>

  <!-- Month Axis Labels -->
  {months_str}

  <!-- Weekday Labels -->
  <text x="15" y="86.5" class="meta-text">Mon</text>
  <text x="15" y="116.5" class="meta-text">Wed</text>
  <text x="15" y="146.5" class="meta-text">Fri</text>

  <!-- Heatmap boxes -->
{rects_str}

  <!-- Legend -->
  <g transform="translate({svg_width - 155}, 175)">
    <text x="0" y="9" class="meta-text">Less</text>
    <rect x="35" y="0" width="11" height="11" rx="2" fill="#161b22" />
    <rect x="50" y="0" width="11" height="11" rx="2" fill="#0e4429" />
    <rect x="65" y="0" width="11" height="11" rx="2" fill="#006d32" />
    <rect x="80" y="0" width="11" height="11" rx="2" fill="#26a641" />
    <rect x="95" y="0" width="11" height="11" rx="2" fill="#39d353" />
    <text x="115" y="9" class="meta-text">More</text>
  </g>

</svg>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Successfully generated {output_path}")

if __name__ == "__main__":
    generate_heatmap_svg()