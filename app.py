import streamlit as st
import urllib.parse
from PIL import Image
import requests
from io import BytesIO
import random

st.set_page_config(page_title="Gen-Vibe Interior Studio", layout="wide")
st.title("✨ Gen-Vibe Aesthetic Interior Studio")
st.caption("Minimalist curves, micro-fluting, curated spaces, and automated estimates.")

st.sidebar.header("🎨 Design Matrix")
wood_style = st.sidebar.selectbox("Feature Style", [
    "Organic S-Curve Wall with Micro-Fluted Battens & Floating Bay",
    "Pill-Shaped Rounded Arch Niche with Halo Backlight",
    "Cantilevered Minimalist Floating Console with Rounded Edges",
    "Japandi Split Accent: Limewash Plaster & Fine Fluting"
])

color_palette = st.sidebar.selectbox("Material Palette", [
    "Oatmilk Crema Limewash + Nordic Bleached Birch",
    "Chalk White Microcement + Biscuit Smoked Oak",
    "Warm Greige Travertine + Soft Ash Micro-Slats",
    "Matte Taupe Clay + Honey Blonde Oak"
])

vibe_theme = st.sidebar.selectbox("Vibe Direction", [
    "Pinterest Dream Home (Airy, Soft Warm Lighting)",
    "Architectural Digest Minimalist (Sculptural Curves & Raw Stone)",
    "Serene Japandi Loft (Biophilic Warmth & Daylight)"
])

st.sidebar.divider()
wall_w = st.sidebar.number_input("Width (ft)", min_value=4.0, max_value=30.0, value=12.0, step=0.5)
wall_h = st.sidebar.number_input("Height (ft)", min_value=6.0, max_value=15.0, value=9.5, step=0.5)
sqft_mat_rate = st.sidebar.number_input("Material Rate (₹/sqft)", value=420, step=20)
sqft_labor_rate = st.sidebar.number_input("Artisan Labor Rate (₹/sqft)", value=180, step=10)

# Calculations
sqft = wall_w * wall_h
ply_sheets = int((sqft * 1.15) // 32) + 1
slat_linear_ft = int(wall_w * (wall_h / 0.35))
led_strip_ft = wall_w * 2.2

cost_mat = sqft * sqft_mat_rate
cost_labor = sqft * sqft_labor_rate
cost_led = led_strip_ft * 210
grand_total = cost_mat + cost_labor + cost_led

# Wall Presets & Upload
input_mode = st.radio("Wall Input:", ["Curated Wall Preset", "Upload Photo"], horizontal=True)
active_image = None
chosen_room_type = "living room accent wall"

preset_catalog = {
    "Living Room (TV & Media Accent Wall)": {
        "url": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=900&q=80",
        "tag": "modern living room TV media accent wall with floating low-profile console"
    },
    "Master Bedroom (Headboard Accent Wall)": {
        "url": "https://images.unsplash.com/photo-1616594039964-ae9021a400a0?w=900&q=80",
        "tag": "luxury master bedroom feature headboard wall with fluted slats and warm ambient bed backlighting"
    },
    "Modern Kitchen & Dining (Backsplash / Feature Wall)": {
        "url": "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=900&q=80",
        "tag": "contemporary minimalist kitchen and dining accent wall with textured stone and fluted cabinetry"
    },
    "Home Office & Study (Desk Backdrop)": {
        "url": "https://images.unsplash.com/photo-1518455027359-f3f8164ba6bd?w=900&q=80",
        "tag": "executive modern home office desk background wall with built-in arched display shelves"
    },
    "Foyer & Entryway (Gallery Niche)": {
        "url": "https://images.unsplash.com/photo-1513694203232-719a280e022f?w=900&q=80",
        "tag": "luxury foyer entrance accent wall with organic archway and illuminated floating vanity ledge"
    }
}

if input_mode == "Upload Photo":
    uploaded = st.file_uploader("Upload wall photo", type=["jpg", "png", "jpeg"])
    if uploaded:
        try:
            active_image = Image.open(uploaded)
        except Exception:
            st.error("Invalid image format.")
else:
    preset_key = st.selectbox("Select Room Type:", list(preset_catalog.keys()))
    selected_preset = preset_catalog[preset_key]
    chosen_room_type = selected_preset["tag"]
    try:
        r_preset = requests.get(selected_preset["url"], timeout=10)
        active_image = Image.open(BytesIO(r_preset.content))
    except Exception:
        st.warning("Preset image offline. Please upload a photo.")

if active_image:
    c1, c2 = st.columns([1, 1.25])
    with c1:
        st.subheader("Base Space Reference")
        st.image(active_image, use_container_width=True)

    with c2:
        st.subheader("Aesthetic Concept")
        custom_notes = st.text_
