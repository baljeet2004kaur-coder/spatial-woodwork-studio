import streamlit as st
import urllib.parse
from PIL import Image
import requests
from io import BytesIO
import random

st.set_page_config(page_title="Gen-Vibe Interior Studio", page_icon="✨", layout="wide")
st.title("✨ Gen-Vibe Luxury Indian Interior & Feature Wall Studio")
st.caption("Contemporary Indian aesthetics, Italian marble textures, brass CNC trims, fluted louvers & commercial estimates.")

# ----------------- SIDEBAR DESIGN MATRIX -----------------
st.sidebar.header("🎨 Indian Aesthetic Direction")

wood_style = st.sidebar.selectbox("Feature Wall Concept", [
    "Italian Statuario Marble Slab with Fluted Teak Panels & Warm Profile Backlighting",
    "Asymmetrical CNC Brass Geometric Trim with Smoked Grey Charcoal Louvers",
    "Pill-Shaped Arched Backlit Niche with Integrated Mandir/Pooja Display Shelf",
    "Low-Profile Floating TV Console with Fluted Louver Drawers & Ambient Gold Glow",
    "Contemporary Greige Limewash Accent with Brass T-Profile Inlays"
])

color_palette = st.sidebar.selectbox("Material & Color Palette", [
    "Warm Walnut Veneer + White Statuario Marble + Rose Gold Metal Trim",
    "Smoked Charcoal Oak + Champagne Brass Profile + Cream Travertine",
    "Natural Teakwood Slats + Matte Beige PU Paint Finish + Gold Accents",
    "Warm Greige Textured Limewash + Fluted Ashwood + Muted Bronze"
])

vibe_theme = st.sidebar.selectbox("Vibe & Ambience", [
    "Modern Indian Luxury Apartment (Warm 3000K Amber Profile Lights, Premium Finishes)",
    "Contemporary Minimalist Villa (Spacious, Sculptural Curves & Rich Textures)",
    "Architectural Digest India Feature (Earthy Tones, Subtle Brass, Seamless Joinery)"
])

st.sidebar.divider()
st.sidebar.header("📐 Wall Dimensions (ft)")
wall_w = st.sidebar.number_input("Width (Feet)", min_value=4.0, max_value=35.0, value=12.0, step=0.5)
wall_h = st.sidebar.number_input("Height (Feet)", min_value=6.0, max_value=16.0, value=9.5, step=0.5)

st.sidebar.divider()
st.sidebar.header("💰 Indian Market Rates (₹ INR)")
substrate = st.sidebar.selectbox("Substrate & Finish System", [
    "HDHMR Board + Charcoal Fluted Louvers + Acrylic Gloss (₹420/sqft)",
    "Calibrated BWP Marine Ply + Natural Teak Veneer + PU Polish (₹520/sqft)",
    "CNC Routed Substrate + Nano Statuario Marble Finish (₹650/sqft)"
])

rates = {
    "HDHMR Board + Charcoal Fluted Louvers + Acrylic Gloss (₹420/sqft)": 420,
    "Calibrated BWP Marine Ply + Natural Teak Veneer + PU Polish (₹520/sqft)": 520,
    "CNC Routed Substrate + Nano Statuario Marble Finish (₹650/sqft)": 650
}

sqft_mat_rate = st.sidebar.number_input("Material Rate (₹/sqft)", value=rates[substrate], step=20)
sqft_labor_rate = st.sidebar.number_input("Artisan Carpentry & Polish Labor (₹/sqft)", value=190, step=10)

# Calculations
sqft = wall_w * wall_h
ply_sheets = int((sqft * 1.15) // 32) + 1
slat_linear_ft = int(wall_w * (wall_h / 0.35))
led_strip_ft = wall_w * 2.4

cost_mat = sqft * sqft_mat_rate
cost_labor = sqft * sqft_labor_rate
cost_led = led_strip_ft * 220
grand_total = cost_mat + cost_labor + cost_led

# ----------------- ROOM CONTEXT -----------------
input_mode = st.radio("Wall Input:", ["Curated Indian Space Presets", "Upload My Wall Photo"], horizontal=True)

preset_catalog = {
    "Living Room (Grand TV & Media Unit Wall)": {
        "url": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800&q=70",
        "tag": "modern Indian luxury living room TV media accent wall, Italian marble panel, fluted louvers, floating console"
    },
    "Master Bedroom (Luxury Headboard Feature Wall)": {
        "url": "https://images.unsplash.com/photo-1616594039964-ae9021a400a0?w=800&q=70",
        "tag": "modern Indian master bedroom feature headboard wall with fluted wood panelling and warm hidden LED cove glow"
    },
    "Dining Room (Contemporary Crockery & Accent Wall)": {
        "url": "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=800&q=70",
        "tag": "modern Indian dining area feature wall with integrated backlit niche and fluted wood textures"
    },
    "Pooja Room / Mandir Wall (Sacred Contemporary Corner)": {
        "url": "https://images.unsplash.com/photo-1513694203232-719a280e022f?w=800&q=70",
        "tag": "contemporary Indian home pooja mandir sacred space, back-lit translucent onyx stone arch, subtle brass jali work"
    },
    "Entrance Foyer & Passage Wall": {
        "url": "https://images.unsplash.com/photo-1518455027359-f3f8164ba6bd?w=800&q=70",
        "tag": "luxury Indian home entrance foyer accent wall with full-length backlit mirror and teak console"
    }
}

chosen_space_tag = "luxury Indian modern living room TV accent wall"
img_display_source = None

if input_mode == "Upload My Wall Photo":
    uploaded = st.file_uploader("Upload wall photo", type=["jpg", "png", "jpeg"])
    if uploaded:
        try:
            img_display_source = Image.open(uploaded)
        except Exception:
            st.error("Invalid image format.")
else:
    preset_key = st.selectbox("Select Space Type:", list(preset_catalog.keys()))
    preset_data = preset_catalog[preset_key]
    chosen_space_tag = preset_data["tag"]
    img_display_source = preset_data["url"]

# ----------------- RENDERING & RESULTS -----------------
if img_display_source:
    c1, c2 = st.columns([1, 1.25])
    with c1:
        st.subheader("Reference Space")
        st.image(img_display_source, use_container_width=True)

    with c2:
        st.subheader("Architectural Transformation")
        custom_notes = st.text_input("Custom Design Notes (Optional):", placeholder="e.g. 75 inch OLED TV, mandir bell niche, brass trims")
        note_str = f", {custom_notes}" if custom_notes.strip() else ""

        if st.button("✨ Generate Indian Luxury Design", type="primary"):
            with st.spinner("Curating premium Indian interior render..."):
                seed = random.randint(1000, 999999)
                prompt = (
                    f"luxurious modern Indian apartment interior, {chosen_space_tag}, "
                    f"concept {wood_style}, palette {color_palette}, "
                    f"subtle brushed brass T-profiles, warm 3000K profile strip backlight, "
                    f"{vibe_theme}, Architectural Digest India style, crisp 8k photorealistic indoor photography, no exterior{note_str}"
                )
                enc_p = urllib.parse.quote(prompt)
                headers = {"User-Agent": "Mozilla/5.0"}
                url_primary = f"https://image.pollinations.ai/prompt/{enc_p}?width=800&height=600&nologo=true&seed={seed}"
                
                img_data = None
                try:
                    res = requests.get(url_primary, headers=headers, timeout=12)
                    if res.status_code == 200 and len(res.content) > 5000:
                        img_data = res.content
                except Exception:
                    pass

                if img_data is None:
                    fb_url = "https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?w=800&q=70"
                    try:
                        res_fb = requests.get(fb_url, timeout=6)
                        if res_fb.status_code == 200:
                            img_data = res_fb.content
                    except Exception:
                        pass

                if img_data:
                    st.image(img_data, use_container_width=True)
                    st.success("Modern Indian design concept ready!")
                    st.download_button("💾 Save Render (PNG)", img_data, f"Indian_Luxury_Design_{seed}.png", "image/png")
                else:
                    st.error("Server congested. Please click generate once more.")

    st.divider()
    st.subheader("📋 Production Cut Sheet & Bill of Quantities (BOQ)")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Wall Area", f"{sqft:.1f} sq.ft.")
    m2.metric("8x4 Core Sheets", f"{ply_sheets} Nos.")
    m3.metric("Fluted Slats/Louvers", f"~{slat_linear_ft} RFT")
    m4.metric("Concealed LED Profile", f"~{led_strip_ft:.1f} RFT")

    st.subheader("💵 Commercial Estimation (₹ INR)")
    b1, b2, b3, b4 = st.columns(4)
    b1.metric("Panels & Finishes", f"₹{cost_mat:,.0f}")
    b2.metric("Artisan Labor", f"₹{cost_labor:,.0f}")
    b3.metric("Warm LED Profiles", f"₹{cost_led:,.0f}")
    b4.metric("Estimated Total", f"₹{grand_total:,.0f}")

    quote_body = (
        f"==========================================================\n"
        f"      LUXURY INDIAN INTERIOR MILLWORK ESTIMATION\n"
        f"==========================================================\n\n"
        f"Space Category     : {chosen_space_tag}\n"
        f"Feature Concept    : {wood_style}\n"
        f"Material Finishes  : {color_palette}\n"
        f"Core Substrate     : {substrate}\n"
        f"Ambience Direction : {vibe_theme}\n\n"
        f"--- WALL SPECIFICATIONS ---\n"
        f"Dimensions         : {wall_w} ft (W) x {wall_h} ft (H)\n"
        f"Total Wall Area    : {sqft:.1f} sq.ft.\n\n"
        f"--- BILL OF QUANTITIES (BOQ) ---\n"
        f"Core Boards (8x4)  : {ply_sheets} Sheets (including 15% wastage/curve buffer)\n"
        f"Fluted Louvers     : ~{slat_linear_ft} Running Feet\n"
        f"Profile LED Strips : ~{led_strip_ft:.1f} Running Feet (3000K Warm Gold)\n\n"
        f"--- COMMERCIAL COST ESTIMATE (INR) ---\n"
        f"Material & Texture : ₹{cost_mat:,.2f}\n"
        f"Carpentry Labor    : ₹{cost_labor:,.2f}\n"
        f"Profile Lighting   : ₹{cost_led:,.2f}\n"
        f"----------------------------------------------------------\n"
        f"TOTAL CONTRACT VAL : ₹{grand_total:,.2f}\n"
        f"==========================================================\n"
    )
    st.download_button("📄 Download Contractor BOQ Quote (.txt)", quote_body, "Indian_Interior_BOQ.txt", "text/plain")
else:
    st.info("Select a space preset or upload a photo to begin.")
