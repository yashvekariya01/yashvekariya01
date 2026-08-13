#!/usr/bin/env python3
import os
import sys
from PIL import Image

def generate_ascii_svg(input_path="source-prepped.png", output_path="avi-ascii.svg"):
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found. Please run scripts/prep_photo.py first.")
        sys.exit(1)

    # Open image
    img = Image.open(input_path).convert("L")
    width_orig, height_orig = img.size

    # Target settings
    columns = 68
    rows = 45
    
    # Resize to grid
    img_resized = img.resize((columns, rows), Image.Resampling.LANCZOS)
    
    # Character ramp
    ramp = " .:-=+*cs#%@"
    num_chars = len(ramp)
    
    ascii_rows = []
    for y in range(rows):
        row_chars = []
        for x in range(columns):
            pixel_val = img_resized.getpixel((x, y))
            # Black pixel (0) -> '@' (idx 11, dense)
            # White pixel (255) -> ' ' (idx 0, empty)
            idx = int((255 - pixel_val) / 255 * (num_chars - 1))
            char = ramp[idx]
            # Escape XML special characters
            if char == '&':
                char = '&amp;'
            elif char == '<':
                char = '&lt;'
            elif char == '>':
                char = '&gt;'
            elif char == '"':
                char = '&quot;'
            elif char == "'":
                char = '&apos;'
            row_chars.append(char)
        ascii_rows.append("".join(row_chars))

    # SVG layout settings
    svg_width = 370
    svg_height = 370
    padding_left = 15
    padding_right = 15
    content_width = svg_width - padding_left - padding_right
    start_y = 52
    row_height = 6.4

    # Animation settings
    stagger_delay = 0.04  # Delay between rows
    anim_duration = 0.5   # Reveal duration per row

    # Build SVG clip-paths and text elements
    clip_paths = []
    text_elements = []

    for i, row_text in enumerate(ascii_rows):
        y_pos = start_y + i * row_height
        clip_id = f"r-{i}"
        
        # Calculate staggering delay for this row
        delay = round(i * stagger_delay, 3)
        
        # Create clip path for typing effect
        clip_paths.append(
            f'    <clipPath id="{clip_id}">\n'
            f'      <rect x="{padding_left}" y="{y_pos - row_height + 1.5}" width="0" height="{row_height + 2}">\n'
            f'        <animate attributeName="width" from="0" to="{content_width}" dur="{anim_duration}s" begin="{delay}s" fill="freeze" />\n'
            f'      </rect>\n'
            f'    </clipPath>'
        )
        
        # Create text element using that clip-path
        text_elements.append(
            f'  <text x="{padding_left}" y="{y_pos:.1f}" class="ascii" clip-path="url(#{clip_id})">{row_text}</text>'
        )

    clip_paths_str = "\n".join(clip_paths)
    text_elements_str = "\n".join(text_elements)

    svg_content = f"""<svg width="{svg_width}" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <style>
    .bg {{ fill: #0d1117; rx: 10px; }}
    .border {{ stroke: #30363d; stroke-width: 1px; }}
    .title {{ font: bold 12px 'Fira Code', monospace; fill: #58a6ff; }}
    .ascii {{ font: 7.2px 'Fira Code', monospace; fill: #4af626; white-space: pre; }}
  </style>
  
  <rect width="100%" height="100%" class="bg border" />
  
  <defs>
{clip_paths_str}
  </defs>

  <!-- MacOS-style terminal buttons -->
  <g transform="translate(15, 18)">
    <circle cx="0" cy="0" r="4.5" fill="#ff5f56" />
    <circle cx="12" cy="0" r="4.5" fill="#ffbd2e" />
    <circle cx="24" cy="0" r="4.5" fill="#27c93f" />
    <text x="40" y="4" class="title">yash@github: ~/portrait</text>
  </g>

  <!-- Animated ASCII content -->
{text_elements_str}
</svg>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Successfully generated {output_path}")

if __name__ == "__main__":
    generate_ascii_svg()
