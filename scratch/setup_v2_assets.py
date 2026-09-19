import os
import shutil

BRAIN_DIR = r"C:\Users\HP\.gemini\antigravity-ide\brain\6229c69f-169e-41a2-ba8e-60d64e8156d7"
BASE_DIR = r"d:\PROJECTS\PERSONALPROJECTS\Portfolio_improved\portfolio-an"

# Ensure directories exist
os.makedirs(os.path.join(BASE_DIR, "media", "profile"), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "media", "projects", "gallery"), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "static", "img", "branding"), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "static", "img", "patterns"), exist_ok=True)

# File mappings from conversation uploads
file_map = {
    # Message 1 uploads
    "media__1789809954015.png": [
        os.path.join(BASE_DIR, "static", "img", "branding", "joseph-kiarie-logo.png"),
        os.path.join(BASE_DIR, "static", "img", "branding", "logo.png"),
    ],
    "media__1789809955004.jpg": [
        os.path.join(BASE_DIR, "media", "profile", "joseph-car.jpg"),
        os.path.join(BASE_DIR, "static", "img", "joseph-car.jpg"),
    ],
    "media__1789809955079.jpg": [
        os.path.join(BASE_DIR, "media", "projects", "gallery", "agriflow-login.jpg"),
        os.path.join(BASE_DIR, "static", "img", "agriflow-login.jpg"),
    ],
    "media__1789809955124.jpg": [
        os.path.join(BASE_DIR, "media", "projects", "gallery", "agriflow-home.jpg"),
        os.path.join(BASE_DIR, "static", "img", "agriflow-home.jpg"),
    ],
    "media__1789809955339.jpg": [
        os.path.join(BASE_DIR, "media", "profile", "joseph-portrait.jpg"),
        os.path.join(BASE_DIR, "media", "profile", "jose.jpg"),
        os.path.join(BASE_DIR, "static", "img", "joseph-portrait.jpg"),
    ],
    
    # Pattern images from message 3
    "media__1789810135122.png": [
        os.path.join(BASE_DIR, "static", "img", "patterns", "bg-pattern-topographic-raw.png"),
    ],
    "media__1789810135155.png": [
        os.path.join(BASE_DIR, "static", "img", "patterns", "bg-pattern-dot-grid-raw.png"),
    ],
    "media__1789810135201.png": [
        os.path.join(BASE_DIR, "static", "img", "patterns", "bg-pattern-arc-rings-raw.png"),
    ],
}

print("Copying asset files...")
for src_name, dst_paths in file_map.items():
    src_path = os.path.join(BRAIN_DIR, src_name)
    if os.path.exists(src_path):
        for dst in dst_paths:
            shutil.copy2(src_path, dst)
            print(f"Copied {src_name} -> {dst}")
    else:
        print(f"Warning: {src_name} not found in {BRAIN_DIR}")

# Create clean SVG vector patterns for resolution-independent styling
arc_rings_svg = """<svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <g fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.8">
    <circle cx="100" cy="100" r="80" stroke-dasharray="180 30" />
    <circle cx="100" cy="100" r="60" stroke-dasharray="140 20" />
    <circle cx="100" cy="100" r="40" />
    <circle cx="100" cy="100" r="18" fill="currentColor" opacity="0.3" />
    <circle cx="0" cy="0" r="50" />
    <circle cx="200" cy="0" r="50" />
    <circle cx="0" cy="200" r="50" />
    <circle cx="200" cy="200" r="50" />
  </g>
</svg>"""

dot_grid_svg = """<svg width="24" height="24" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
  <circle cx="12" cy="12" r="1.5" fill="currentColor" opacity="0.7"/>
</svg>"""

topographic_svg = """<svg width="300" height="300" viewBox="0 0 300 300" xmlns="http://www.w3.org/2000/svg">
  <path d="M 0,30 Q 75,50 150,30 T 300,30 M 0,80 Q 75,60 150,80 T 300,80 M 0,130 Q 75,150 150,130 T 300,130 M 0,180 Q 75,160 150,180 T 300,180 M 0,230 Q 75,250 150,230 T 300,230 M 0,280 Q 75,260 150,280 T 300,280" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.7"/>
</svg>"""

with open(os.path.join(BASE_DIR, "static", "img", "patterns", "bg-pattern-arc-rings.svg"), "w") as f:
    f.write(arc_rings_svg)

with open(os.path.join(BASE_DIR, "static", "img", "patterns", "bg-pattern-dot-grid.svg"), "w") as f:
    f.write(dot_grid_svg)

with open(os.path.join(BASE_DIR, "static", "img", "patterns", "bg-pattern-topographic.svg"), "w") as f:
    f.write(topographic_svg)

# Extract SVG logo mark matching Joseph's logo
logo_mark_svg = """<svg width="60" height="60" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg">
  <rect width="60" height="60" rx="12" fill="#D89379" />
  <g fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round">
    <path d="M 12 28 A 20 12 0 0 1 48 28" />
    <path d="M 17 23 A 16 10 0 0 1 43 23" />
    <path d="M 12 34 A 20 12 0 0 0 48 34" />
    <path d="M 17 39 A 16 10 0 0 0 43 39" />
  </g>
</svg>"""

with open(os.path.join(BASE_DIR, "static", "img", "branding", "logo-mark.svg"), "w") as f:
    f.write(logo_mark_svg)

print("All asset files and SVG patterns prepared successfully!")
