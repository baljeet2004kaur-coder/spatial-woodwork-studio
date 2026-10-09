import streamlit as st
import urllib.parse
from PIL import Image
import requests
from io import BytesIO
import random

st.set_page_config(page_title="Spatial Woodwork Studio", layout="wide")

st.title("🏛️ Custom Woodwork & Interior Studio")
st.caption("Upload a wall photo or choose a preset room to generate custom finishes, cut sheets, and client budgets.")

# ----------------- SIDEBAR CONTROLS -----------------
st.sidebar.header("🪵 Design Settings")

wood_style = st.sidebar.selectbox(
    "Wall Style",
    [
        "Vertical Fluted Slats",
        "Geometric Paneling",
        "Floating Bed Headboard",
        "Classic Wainscoting",
        "Curved Ribbed Wall Feature"
    ]
)

wood_finish = st.sidebar.selectbox(
    "Wood Type",
    [
        "Warm Natural Teak",
        "Smoked Dark Walnut",
        "Scandinavian White Oak",
        "Charcoal Ebonized Ash",
        "Rich Honey Rosewood"
    ]
)

design_mood = st.sidebar.selectbox(
    "Interior Vibe / Aesthetic",
    [
        "Luxury Hotel Suite",
        "Minimalist Japandi Zen",
        "Contemporary Architectural Digest",
        "Warm Moody Modern"
    ]
)

has_led = st.sidebar.checkbox("Add Concealed Warm LED Strip", value=True)

st.sidebar.divider()
st.sidebar.subheader("📐 Wall Dimensions (ft)")
wall_w = st.sidebar.number_input("Width (Feet)", min_value=4.0, max_value=30.0, value=12.0, step=0.5)
wall_h = st.sidebar.number_input("Height (Feet)", min_value=6.0, max_value=15.0, value=9.5, step=0.5)

st.sidebar.divider()
st.sidebar.subheader("💰 Pricing Rates (₹ INR)")
sqft_material_rate = st.sidebar.number_input("Material Rate (per sq.ft)", min_value=100, max_value=2000, value=350, step=25)
sqft_labor_rate = st.sidebar.number_input("Carpenter Labor (per sq.ft)", min_value=50, max_value=1000, value=120, step=10)

# Calculations
sqft = wall_w * wall_h
ply_sheets = int((sqft * 1.10) // 32) + 1
slat_ft = int(wall_w * (wall_h / 0.5)) if "Slats" in wood_style or "Ribbed" in wood_style else int(wall_w * 4)
led_channel = f"{wall_w:.1f} Feet" if has_led else "None"

total_material_cost = sqft * sqft_material_rate
total_labor_cost = sqft * sqft_labor_rate
led_cost = (wall_w * 150) if has_led else 0
grand_total = total_material_cost + total_labor_cost + led_cost

# ----------------- MAIN INPUT SELECTION -----------------
input_mode = st.radio("Choose Input Method:", ["Upload Custom Photo", "Use Demo Preset Wall"], horizontal=True)

active_image = None

if input_mode == "Upload Custom Photo":
    uploaded_file = st.file_uploader("Upload wall photo", type=["jpg", "png", "jpeg"])
    if uploaded_file is not None:
        try:
            active_image = Image.open(uploaded_file)
        except Exception:
            st.error("⚠️ Could not read image file. Please upload a standard JPG or PNG.")
else:
    preset_choice = st.selectbox(
        "Select a Sample Wall:",
        ["Modern Plain White Wall", "Minimalist Master Bedroom Wall", "Living Room TV Background Wall"]
    )
    demo_urls = {
        "Modern Plain White Wall": "https://images.unsplash.com/photo-1513694203232-719a280e022f?w=800&q=80",
        "Minimalist Master Bedroom Wall": "https://images.unsplash.com/photo-1616594039964-ae9021a400a0?w=800&q=80",
        "Living Room TV Background Wall": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800&q=80"
    }
    try:
        resp = requests.get(demo_urls[preset_choice])
        active_image = Image.open(BytesIO(resp.content))
    except Exception:
        st.warning("Could not load preset image. Please upload a photo instead.")

# ----------------- RENDERING & RESULTS -----------------
if active_image is not None:
    col_l, col_r = st.columns(2)
    with col_l:
        st.subheader("Original Selected Wall")
        st.image(active_image, use_container_width=True)
    with col_r:
        st.subheader("Architectural Renovation")
        
        led_text = "with concealed warm ambient 3000k LED strip lighting" if has_led else "natural balanced daylight"
        
        # Fresh random seed generated every time button is pressed
        rand_seed = random.randint(1000, 999999)
        
        prompt = (
            f"High-end interior design photograph, {design_mood} aesthetic, "
            f"accent wall featuring custom architectural {wood_style} crafted from {wood_finish}, "
            f"{led_text}, master carpenter detailing, dramatic shadow play, photorealistic, 8k resolution"
        )
        
        if st.button("✨ Generate New Woodwork Variation", type="primary"):
            with st.spinner("Rendering unique design variation..."):
                encoded_prompt = urllib.parse.quote(prompt)
                image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=800&height=600&nologo=true&seed={rand_seed}"
                resp = requests.get(image_url)
                
                if resp.status_code == 200:
                    st.image(resp.content, use_container_width=True)
                    st.success(f"Generated design variation (Seed #{rand_seed})")
                    
                    st.divider()
                    st.subheader("📥 Export Deliverables")
                    d1, d2 = st.columns(2)
                    with d1:
                        st.download_button(
                            label="💾 Download Render (PNG)",
                            data=resp.content,
                            file_name=f"{wood_style}_{wood_finish}_{rand_seed}.png",
                            mime="image/png"
                        )
                    with d2:
                        quote_sheet = (
                            f"=========================================\n"
                            f"    COMMERCIAL WOODWORK ESTIMATE & CUT SHEET\n"
                            f"=========================================\n\n"
                            f"Style: {wood_style}\n"
                            f"Finish: {wood_finish}\n"
                            f"Theme: {design_mood}\n"
                            f"Lighting: {led_channel}\n\n"
                            f"Dimensions: {wall_w:.1f} ft x {wall_h:.1f} ft ({sqft:.1f} sq.ft.)\n\n"
                            f"--- BILL OF MATERIALS ---\n"
                            f"Plywood Core (8x4): {ply_sheets} Sheets\n"
                            f"Profiles / Slats : ~{slat_ft} Linear Feet\n\n"
                            f"--- BUDGET BREAKDOWN (INR) ---\n"
                            f"Material Cost    : ₹{total_material_cost:,.2f}\n"
                            f"Labor Cost       : ₹{total_labor_cost:,.2f}\n"
                            f"Electrical/LED   : ₹{led_cost:,.2f}\n"
                            f"Estimated Total  : ₹{grand_total:,.2f}\n"
                        )
                        st.download_button(
                            label="📄 Download Estimate & Cut Sheet",
                            data=quote_sheet,
                            file_name=f"Woodwork_Quote_{rand_seed}.txt",
                            mime="text/plain"
                        )

    st.divider()
    
    # Material Metrics
    st.subheader("📋 Craftsman Cutting & Material Estimate")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Wall Area", f"{sqft:.1f} sq.ft.")
    m2.metric("Core Plywood (8x4)", f"{ply_sheets} Sheets")
    m3.metric("Linear Profiles / Slats", f"~{slat_ft} Feet")
    m4.metric("LED Channel", led_channel)

    # Cost Metrics
    st.subheader("💵 Financial Budget Summary")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Material Cost", f"₹{total_material_cost:,.0f}")
    c2.metric("Carpentry Labor", f"₹{total_labor_cost:,.0f}")
    c3.metric("Lighting & Misc", f"₹{led_cost:,.0f}")
    c4.metric("Total Project Cost", f"₹{grand_total:,.0f}")

else:
    st.info("👆 Upload an image or select a preset wall to begin.")
