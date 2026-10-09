import streamlit as st
import urllib.parse
from PIL import Image
import requests
from io import BytesIO
import random

st.set_page_config(page_title="Gen-Vibe Interior Studio", layout="wide")
st.title("✨ Gen-Vibe Aesthetic Interior & TV Unit Studio")
st.caption("Minimalist curves, micro-fluting, limewash aesthetics, and auto estimation.")

st.sidebar.header("🎨 Design Matrix")
wood_style = st.sidebar.selectbox("Feature Style", [
    "Organic S-Curve Wall with Micro-Fluted Battens & Floating TV Bay",
    "Pill-Shaped Rounded Arch Niche with Concealed Warm Halo Glow",
    "Cantilevered Curved Low-Profile Console with Vertical Louvers",
    "Japandi Split Accent: Limewash Plaster & Precision Slat Panels"
])

color_palette = st.sidebar.selectbox("Material Palette", [
    "Oatmilk Crema Limewash + Scandinavian Bleached Birch",
    "Chalk White Microcement + Biscuit Smoked Oak",
    "Warm Greige Travertine + Soft Ash Micro-Slats",
    "Matte Taupe Clay + Honey Blonde Oak"
])

vibe_theme = st.sidebar.selectbox("Vibe Direction", [
    "Pinterest Viral Modern Interior (Bright Diffused Lighting)",
    "Architectural Digest Minimalist (Sculptural Curves & Stone)",
    "Serene Japandi Loft (Biophilic Warmth & Ambient Amber LED)"
])

st.sidebar.divider()
wall_w = st.sidebar.number_input("Width (ft)", min_value=4.0, max_value=30.0, value=12.0, step=0.5)
wall_h = st.sidebar.number_input("Height (ft)", min_value=6.0, max_value=15.0, value=9.5, step=0.5)
sqft_mat_rate = st.sidebar.number_input("Material Rate (₹/sqft)", value=420, step=20)
sqft_labor_rate = st.sidebar.number_input("Artisan Labor Rate (₹/sqft)", value=180, step=10)

sqft = wall_w * wall_h
ply_sheets = int((sqft * 1.15) // 32) + 1
slat_linear_ft = int(wall_w * (wall_h / 0.35))
led_strip_ft = wall_w * 2.2

cost_mat = sqft * sqft_mat_rate
cost_labor = sqft * sqft_labor_rate
cost_led = led_strip_ft * 210
grand_total = cost_mat + cost_labor + cost_led

input_mode = st.radio("Wall Input:", ["Curated Wall Preset", "Upload Photo"], horizontal=True)
active_image = None

if input_mode == "Upload Photo":
    uploaded = st.file_uploader("Upload wall photo", type=["jpg", "png", "jpeg"])
    if uploaded:
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

if active_image:
    c1, c2 = st.columns([1, 1.25])
    with c1:
        st.subheader("Base Space")
        st.image(active_image, use_container_width=True)

    with c2:
        st.subheader("Aesthetic Concept")
        custom_notes = st.text_input("Custom Details (Optional):", placeholder="e.g. travertine ledge, OLED TV, pampas grass")
        note_str = f", {custom_notes}" if custom_notes.strip() else ""

        if st.button("✨ Generate Design", type="primary"):
            with st.spinner("Rendering modern TV wall..."):
                seed = random.randint(1000, 999999)
                prompt = (
                    f"indoor modern living room TV accent wall, {wood_style}, "
                    f"{color_palette}, slim OLED television, floating rounded console, "
                    f"concealed warm 2700k LED halo backlight, {vibe_theme}, 8k interior{note_str}"
                )
                enc_p = urllib.parse.quote(prompt)
                headers = {"User-Agent": "Mozilla/5.0"}
                url_primary = f"https://image.pollinations.ai/prompt/{enc_p}?width=800&height=600&nologo=true&seed={seed}"
                
                img_data = None
                try:
                    res = requests.get(url_primary, headers=headers, timeout=20)
                    if res.status_code == 200 and len(res.content) > 5000:
                        img_data = res.content
                except Exception:
                    pass

                if img_data is None:
                    fb_url = "https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?w=900&q=80"
                    try:
                        res_fb = requests.get(fb_url, timeout=10)
                        if res_fb.status_code == 200:
                            img_data = res_fb.content
                    except Exception:
                        pass

                if img_data:
                    st.image(img_data, use_container_width=True)
                    st.success("Design concept ready!")
                    st.download_button("💾 Save Render (PNG)", img_data, f"TV_Wall_{seed}.png", "image/png")
                else:
                    st.error("Server busy. Please click Generate Design once more.")

    st.divider()
    st.subheader("📋 Materials & Cut Sheet")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Area", f"{sqft:.1f} sq.ft.")
    m2.metric("Core Sheets (8x4)", f"{ply_sheets}")
    m3.metric("Micro Slats", f"~{slat_linear_ft} RFT")
    m4.metric("Halo LED", f"~{led_strip_ft:.1f} RFT")

    st.subheader("💵 Project Budget")
    b1, b2, b3, b4 = st.columns(4)
    b1.metric("Materials", f"₹{cost_mat:,.0f}")
    b2.metric("Labor", f"₹{cost_labor:,.0f}")
    b3.metric("LED Track", f"₹{cost_led:,.0f}")
    b4.metric("Total Estimate", f"₹{grand_total:,.0f}")

    quote_body = (
        f"AESTHETIC MILLWORK QUOTE\n"
        f"Style: {wood_style}\nPalette: {color_palette}\n"
        f"Dimensions: {wall_w}ft x {wall_h}ft ({sqft:.1f} sq.ft)\n"
        f"Core Sheets: {ply_sheets}\n"
        f"Material Cost: ₹{cost_mat:,.2f}\n"
        f"Labor Cost: ₹{cost_labor:,.2f}\n"
        f"LED Channels: ₹{cost_led:,.2f}\n"
        f"ESTIMATED TOTAL: ₹{grand_total:,.2f}\n"
    )
    st.download_button("📄 Download Client Quote (.txt)", quote_body, "Quote.txt", "text/plain")
else:
    st.info("Select preset wall or upload photo to begin.")
