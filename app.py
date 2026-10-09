import streamlit as st
import urllib.parse
from PIL import Image
import requests
from io import BytesIO
import random

# Page configuration
st.set_page_config(
    page_title="Gen-Vibe Interior Studio",
    page_icon="✨",
    layout="wide"
)

st.title("✨ Gen-Vibe Aesthetic Interior & TV Unit Studio")
st.caption("Minimalist curves, micro-fluting, limewash aesthetics, and instant contractor estimations.")

# ----------------- SIDEBAR CONTROLS -----------------
st.sidebar.header("🎨 Architectural Features")

wood_style = st.sidebar.selectbox(
    "Wall Feature Style",
    [
        "Organic S-Curve Wall with Micro-Fluted Battens & Floating TV Bay",
        "Pill-Shaped Rounded Arch Niche with Concealed Warm Halo Glow",
        "Cantilevered Curved Low-Profile Console with Vertical Louvers",
        "Japandi Split Accent: Limewash Plaster & Precision Slat Panels"
    ]
)

color_palette = st.sidebar.selectbox(
    "Material & Finish Palette",
    [
        "Oatmilk Crema Limewash + Scandinavian Bleached Birch",
        "Chalk White Microcement + Biscuit Smoked Oak",
        "Warm Greige Travertine + Soft Ash Micro-Slats",
        "Matte Taupe Clay + Honey Blonde Oak"
    ]
)

vibe_theme = st.sidebar.selectbox(
    "Atmosphere Mood",
    [
        "Pinterest Viral Modern Interior (Bright, Soft Diffused Lighting)",
        "Architectural Digest Minimalist (Sculptural Curves & Raw Stone)",
        "Serene Japandi Loft (Biophilic Warmth & Ambient Amber LED)"
    ]
)

st.sidebar.divider()
st.sidebar.header("📐 Wall Dimensions (ft)")
wall_w = st.sidebar.number_input("Width (Feet)", min_value=4.0, max_value=30.0, value=12.0, step=0.5)
wall_h = st.sidebar.number_input("Height (Feet)", min_value=6.0, max_value=15.0, value=9.5, step=0.5)

st.sidebar.divider()
st.sidebar.header("💰 Cost Rates (₹ INR)")
sqft_mat_rate = st.sidebar.number_input("Material Rate (₹/sq.ft)", value=420, step=20)
sqft_labor_rate = st.sidebar.number_input("Carpentry & Finishing Labor (₹/sq.ft)", value=180, step=10)

# Calculations
sqft = wall_w * wall_h
ply_sheets = int((sqft * 1.15) // 32) + 1
slat_linear_ft = int(wall_w * (wall_h / 0.35))
led_strip_ft = wall_w * 2.2

cost_mat = sqft * sqft_mat_rate
cost_labor = sqft * sqft_labor_rate
cost_led = led_strip_ft * 210
grand_total = cost_mat + cost_labor + cost_led

# ----------------- MAIN VIEW -----------------
input_mode = st.radio("Wall Context:", ["Curated Aesthetic Wall", "Upload My Wall"], horizontal=True)
active_image = None

if input_mode == "Upload My Wall":
    uploaded = st.file_uploader("Upload wall photo", type=["jpg", "png", "jpeg"])
    if uploaded is not None:
        try:
            active_image = Image.open(uploaded)
        except Exception:
            st.error("Invalid image format.")
else:
    demo_url = "https://images.unsplash.com/photo-1513694203232-719a280e022f?w=900&q=80"
    try:
        r_preset = requests.get(demo_url, timeout=10)
        active_image = Image.open(BytesIO(r_preset.content))
    except Exception:
        st.warning("Preset offline. Please upload an image.")

if active_image is not None:
    c1, c2 = st.columns([1, 1.25])
    
    with c1:
        st.subheader("Base Space")
        st.image(active_image, use_container_width=True)

    with c2:
        st.subheader("Aesthetic Concept")
        custom_notes = st.text_input(
            "Custom Design Notes (Optional):",
            placeholder="e.g. travertine display ledge, OLED TV, pampas vase, arched alcove"
        )
        note_str = f", {custom_notes}" if custom_notes.strip() else ""

        if st.button("✨ Generate Design", type="primary"):
            with st.spinner("Rendering bespoke architectural concept..."):
                seed = random.randint(1000, 999999)
                
                # Strict indoor architectural prompt
                prompt = (
                    f"close-up indoor architectural shot, modern living room interior, "
                    f"luxury minimalist TV entertainment feature wall, {wood_style}, "
                    f"crafted with {color_palette}, mounted slim OLED television, "
                    f"floating rounded low credenza, concealed warm 2700k LED halo backlight, "
                    f"{vibe_theme}, sharp details, 8k resolution, cinematic interior render{note_str}"
                )
                
                enc_p = urllib.parse.quote(prompt)
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
                
                urls = [
                    f"https://image.pollinations.ai/prompt/{enc_p}?width=800&height=600&nologo=true&seed={seed}",
                    f"https://image.pollinations.ai/prompt/{enc_p}?width=800&height=600&nologo=true&seed={seed}&model=flux"
                ]

                img_data =
