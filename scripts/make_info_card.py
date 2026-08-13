#!/usr/bin/env python3
import os

def generate_info_card(output_path="info-card.svg"):
    # SVG Dimensions
    width = 490
    height = 280

    # Detail values
    details = [
        ("OS", "Yash Vekariya (Full-Stack Developer)"),
        ("Host", "Marwadi University (BCA)"),
        ("Kernel", "PHP, React, Next.js, Node.js, Java"),
        ("Shell", "Laravel, MongoDB, MySQL"),
        ("Uptime", "GhostMessage, MicCast, Pizzeria, Kisan Mitra"),
        ("Memory", "Web Dev, Cloud Arcade, Tech Blogging"),
    ]

    # Staggered animation values
    start_delay = 0.1
    step = 0.12
    anim_dur = 0.4

    # Build detail lines with SMIL animations
    lines_svg = []
    
    # Title and separator
    lines_svg.append(
        f'    <g>\n'
        f'      <animate attributeName="opacity" from="0" to="1" dur="{anim_dur}s" begin="0.0s" fill="freeze" />\n'
        f'      <animateTransform attributeName="transform" type="translate" from="0, -10" to="0, 0" dur="{anim_dur}s" begin="0.0s" fill="freeze" />\n'
        f'      <text x="110" y="42" class="title">yashvekariya01@github ~ $ neofetch</text>\n'
        f'    </g>'
    )
    lines_svg.append(
        f'    <g>\n'
        f'      <animate attributeName="opacity" from="0" to="1" dur="{anim_dur}s" begin="{start_delay:.2f}s" fill="freeze" />\n'
        f'      <animateTransform attributeName="transform" type="translate" from="0, -10" to="0, 0" dur="{anim_dur}s" begin="{start_delay:.2f}s" fill="freeze" />\n'
        f'      <text x="110" y="58" class="separator">------------------------</text>\n'
        f'    </g>'
    )

    # Key-value lines
    for i, (key, value) in enumerate(details):
        y_pos = 78 + i * 20
        delay = start_delay + (i + 1) * step
        
        lines_svg.append(
            f'    <g>\n'
            f'      <animate attributeName="opacity" from="0" to="1" dur="{anim_dur}s" begin="{delay:.2f}s" fill="freeze" />\n'
            f'      <animateTransform attributeName="transform" type="translate" from="0, -10" to="0, 0" dur="{anim_dur}s" begin="{delay:.2f}s" fill="freeze" />\n'
            f'      <text x="110" y="{y_pos}" class="key">{key}: <tspan class="val">{value}</tspan></text>\n'
            f'    </g>'
        )

    # Color block line at the bottom
    color_y = 208
    color_delay = start_delay + (len(details) + 1) * step
    colors_blocks = []
    
    # Standard terminal color blocks
    color_palette = ["#ff5f56", "#ffbd2e", "#27c93f", "#58a6ff", "#b392f0", "#79c0ff"]
    for i, color_hex in enumerate(color_palette):
        x_block = 110 + i * 22
        colors_blocks.append(
            f'<rect x="{x_block}" y="{color_y}" width="16" height="12" fill="{color_hex}" rx="2" />'
        )
    colors_blocks_str = "\n      ".join(colors_blocks)

    lines_svg.append(
        f'    <g>\n'
        f'      <animate attributeName="opacity" from="0" to="1" dur="{anim_dur}s" begin="{color_delay:.2f}s" fill="freeze" />\n'
        f'      <animateTransform attributeName="transform" type="translate" from="0, -10" to="0, 0" dur="{anim_dur}s" begin="{color_delay:.2f}s" fill="freeze" />\n'
        f'      {colors_blocks_str}\n'
        f'    </g>'
    )

    lines_svg_str = "\n".join(lines_svg)

    svg_content = f"""<svg fill="none" width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
  <style>
    .bg {{ fill: #0d1117; rx: 10px; }}
    .border {{ stroke: #30363d; stroke-width: 1px; }}
    .title {{ font: bold 13px 'Fira Code', monospace; fill: #4af626; }}
    .separator {{ font: 12px 'Fira Code', monospace; fill: #8b949e; }}
    .key {{ font: bold 11.5px 'Fira Code', monospace; fill: #79c0ff; }}
    .val {{ font: 11.5px 'Fira Code', monospace; fill: #c9d1d9; }}
    
    /* Logo glow effect */
    .glowing-logo {{
      filter: drop-shadow(0px 0px 4px #58a6ff);
    }}
  </style>
  
  <rect width="100%" height="100%" class="bg border" />
  
  <!-- MacOS-style terminal buttons -->
  <g transform="translate(15, 18)">
    <circle cx="0" cy="0" r="4.5" fill="#ff5f56" />
    <circle cx="12" cy="0" r="4.5" fill="#ffbd2e" />
    <circle cx="24" cy="0" r="4.5" fill="#27c93f" />
    <text x="40" y="4" font-family="'Fira Code', monospace" font-size="12" font-weight="bold" fill="#58a6ff">yash@github: ~/neofetch</text>
  </g>

  <!-- Left Column: Terminal / Developer Neon Graphic Logo -->
  <g transform="translate(25, 60)" class="glowing-logo">
    <!-- Glowing Code bracket & Slash -->
    <path d="M 15 25 L 0 40 L 15 55" stroke="#58a6ff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" />
    <path d="M 45 25 L 60 40 L 45 55" stroke="#58a6ff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" />
    <path d="M 25 15 L 35 65" stroke="#ffbd2e" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" />
    
    <!-- Outer accent rings or tech-hex shape -->
    <path d="M 30 -5 L 65 15 L 65 65 L 30 85 L -5 65 L -5 15 Z" stroke="#30363d" stroke-width="1.5" stroke-dasharray="3,3" fill="none" />
    
    <!-- User Initials / Tag -->
    <text x="30" y="115" font-family="'Fira Code', monospace" font-size="15" font-weight="bold" fill="#4af626" text-anchor="middle">&lt;YASH&gt;</text>
  </g>

  <!-- Info lines -->
{lines_svg_str}

</svg>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Successfully generated {output_path}")

if __name__ == "__main__":
    generate_info_card()