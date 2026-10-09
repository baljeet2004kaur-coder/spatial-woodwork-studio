import streamlit as st
import urllib.parse
from PIL import Image
import requests
from io import BytesIO
import random

st.set_page_config(page_title="Aesthetic Studio | Modern Interior Millwork", layout="wide")

st.title("✨ Gen-Vibe Aesthetic Interior & TV Unit Studio")
st.caption("Minimalist textures, organic arches, micro-fluting, and automated architectural pricing.")

# ----------------- SIDEBAR DESIGN MATRIX -----------------
st.sidebar.header("🎨 Contemporary Design Direction")

wood_style = st.sidebar.selectbox(
    "Aesthetic Architecture & Feature Style",
    [
        "Organic Wabi-Sabi Asymmetrical Curve with Micro-Slats",
        "Pill-Shaped Rounded Arch Niche with Soft Halo Backlight",
        "Cantilevered Minimalist Floating Console with Rounded Edges",
        "Japandi Split Accent: Limewash Plaster meets Ultra-Fine Fluting",
        "Curved Wave S-Partition with Integrated Floating Display Ledge",
        "Seamless Monolithic Panel with Concealed Shadow Gaps"
    ]
)

color_palette = st.sidebar.selectbox(
    "Aesthetic Material & Tonal Palette",
    [
        "Oatmilk Crema Limewash + Pale Nordic Bleached Birch",
        "Chalk White Microcement + Biscuit Smoked Oak",
        "Warm Greige Travertine + Soft Ash Micro-Slats",
        "Matte Taupe Clay + Honey Blonde Oak",
        "Earthy Sage Stone Texture + Natural Rattan & Warm Timber",
        "Minimalist Desert Sand + Fluted Muted Linen Veneer"
    ]
)

accent_trim = st.sidebar.selectbox(
    "Modern Detail Accents",
    [
        "Ultra-Slim Concealed Shadow-Gaps (Zero Trim)",
        "Brushed Champagne Micro-Edging",
        "Frosted White Acrylic Diffuser Trim",
        "Textured Raw Travertine Slab Accent"
    ]
)

vibe_theme = st.sidebar.selectbox(
    "Gen-Vibe / Mood Direction",
    [
        "Pinterest Dream Home (Bright, Airy, Soft Warm Lighting)",
        "Architectural Digest Minimalist (Sculptural Curves & Raw Stone)",
        "Serene Japandi Loft (Zen, Natural Daylight, Biophilic Warmth)",
        "Cozy Modern Scandinavian (Muted Neutrals, Calming Ambient Glow)"
    ]
)

st.sidebar.divider()
st.sidebar.header("📐 Wall Dimensions (ft)")
wall_w = st.sidebar.number_input("Width (Feet)", min_value=4.0, max_value=40.0, value=12.0, step=0.5)
wall_h = st.sidebar.number_input("Height (Feet)", min_value=6.0, max_value=16.0, value=9.5, step=0.5)

st.sidebar.divider()
st.sidebar.header("💰 Commercial Estimates (₹ INR)")
substrate = st.sidebar.selectbox(
    "Substrate & Texture System",
    [
        "HDHMR Board + PU Textured Limewash Finish (₹380/sqft)",
        "Calibrated BWP Ply + Natural Scandinavian Veneer (₹480/sqft)",
        "Custom CNC Curved Framework + Microcement Coat (₹580/sqft)"
    ]
)

rates = {
    "HDHMR Board + PU Textured Limewash Finish (₹380/sqft)": 380,
    "Calibrated BWP Ply + Natural Scandinavian Veneer (₹480/sqft)": 480,
    "Custom CNC Curved Framework + Microcement Coat (₹580/sqft)": 580
}

sqft_mat_rate = st.sidebar.number_input("Material Rate (₹/sqft)", value=rates[substrate], step=20)
sqft_labor_rate = st.sidebar.number_input("Specialized Artisan Labor (₹/sqft)", value=180, step=10)

# Calculations
sqft = wall_w * wall_h
ply_sheets = int((sqft * 1.15) // 32) + 1
slat_linear_ft = int(wall_w * (wall_h / 0.35))
led_strip_ft = wall_w * 2.2

total_mat = sqft * sqft_mat_rate
total_labor = sqft * sqft_labor_rate
total_led = led_strip_ft * 210
grand_total = total_mat + total_labor + total_led

# ----------------- MAIN INTERFACE -----------------
input_mode = st.radio("Choose Input:", ["Upload Room Photo", "Use Curated Modern Living Wall"], horizontal=True)

active_image = None

if input_mode == "Upload Room Photo":
    uploaded_file = st.file_uploader("Upload wall photo", type=["jpg", "png", "jpeg"])
    if uploaded_file is not None:
        try:
            active_image = Image.open(uploaded_file)
        except Exception:
            st.error("⚠️ Invalid image format. Please upload a standard JPG or PNG.")
else:
    preset_choice = st.selectbox(
        "Select Room Layout:",
        [
            "Modern Neutral Living Room Wall",
            "Minimalist Master Suite Bed Wall",
            "Cozy Studio Lounge Nook"
        ]
    )
    demo_urls = {
        "Modern Neutral Living Room Wall": "https://images.unsplash.com/photo-1513694203232-719a280e022f?w=900&q=80",
        "Minimalist Master Suite Bed Wall": "https://images.unsplash.com/photo-1616594039964-ae9021a400a0?w=900&q=80",
        "Cozy Studio Lounge Nook": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=900&q=80"
    }
    try:
        resp = requests.get(demo_urls[preset_choice], timeout=10)
        active_image = Image.open(BytesIO(resp.content))
    except Exception:
        st.warning("Preset offline. Please upload a photo.")

# ----------------- RENDERING & RESULTS -----------------
if active_image is not None:
    col_l, col_r = st.columns([1, 1.25])
    with col_l:
        st.subheader("Base Space Reference")
        st.image(active_image, use_container_width=True)
    with col_r:
        st.subheader("Modern Aesthetic Transformation")
        
        custom_notes = st.text_input(
            "Add Specific Design Customizations (Optional):",
            placeholder="e.g. Add organic oval mirror, travertine ledge, pampas decor, flush OLED TV"
        )
        
        custom_extra = f", featuring {custom_notes}" if custom_notes.strip() else ""

        if st.button("✨ Generate Design", type="primary"):
            with st.spinner("Curating high-aesthetic modern render..."):
                rand_seed = random.randint(100000, 9999999)
                
                prompt = (
                    f"Viral Pinterest interior aesthetic, Kinfolk style photography, {vibe_theme}, "
                    f"ultra-modern minimalist TV entertainment accent wall, featuring {wood_style}, "
                    f"finished in {color_palette}, {accent_trim}, "
                    f"sculptural organic curves, seamlessly integrated wall-mounted TV, "
                    f"floating rounded pill credenza, soft concealed 2400K indirect warm halo ambient backlight, "
                    f"soft natural morning window daylight, delicate shadows, hyper-realistic, 8k resolution, crisp architectural detail{custom_extra}"
                )
                
                encoded_prompt = urllib.parse.quote(prompt)
                image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=768&nologo=true&seed={rand_seed}"
                
                try:
                    resp = requests.get(image_url, timeout=30)
                    if resp.status_code == 200:
                        st.image(resp.content, use_container_width=True)
                        st.success("New aesthetic design generated!")
                        
                        st.download_button(
                            label="💾 Download Render (PNG)",
                            data=resp.content,
                            file_name=f"Aesthetic_Design_{rand_seed}.png",
                            mime="image/png"
                        )
                    else:
                        st.error("Service busy. Please try generating again.")
                except Exception:
                    st.error("Image request timed out. Please click generate again.")

    st.divider()
    
    # Material Breakdown
    st.subheader("📋 Modern Millwork Specs & Cut Sheet")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Wall Face Area", f"{sqft:.1f} sq.ft.")
    m2.metric("Core Board Sheets (8x4)", f"{ply_sheets} Sheets")
    m3.metric("Micro-Ribbed Battens", f"~{slat_linear_ft} RFT")
    m4.metric("Diffuse LED Halo Channels", f"~{led_strip_ft:.1f} RFT")

    # Budget Breakdown
    st.subheader("💵 Financial Estimation (INR)")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Materials & Textures", f"₹{total_mat:,.0f}")
    c2.metric("Artisan Joinery & Polish", f"₹{total_labor:,.0f}")
    c3.metric("Ambient Halo Lighting", f"₹{total_led:,.0f}")
    c4.metric("Estimated Client Cost", f"₹{grand_total:,.0f}")

    quote_text = (
        f"==========================================================\n"
        f"       MODERN AESTHETIC INTERIOR DESIGN PROPOSAL\n"
        f"==========================================================\n\n"
        f"Style & Concept    : {wood_style}\n"
        f"Palette & Finish   : {color_palette}\n"
        f"Trim & Accents     : {accent_trim}\n"
        f"Aesthetic Mood     : {vibe_theme}\n"
        f"Substrate System   : {substrate}\n\n"
        f"--- ROOM DIMENSIONS ---\n"
        f"Surface Size       : {wall_w:.1f} ft (W) x {wall_h:.1f} ft (H)\n"
        f"Total Area         : {sqft:.1f} sq.ft.\n\n"
        f"--- PRODUCTION MATERIAL REQUISITION ---\n"
        f"Core Substrate 8x4 : {ply_sheets} Sheets\n"
        f"Fine Battens/Slats : ~{slat_linear_ft} Running Feet\n"
        f"Concealed LED Track: {led_strip_ft:.1f} Running Feet\n\n"
        f"--- COST ESTIMATE (INR) ---\n"
        f"Core & Finish Cost : ₹{total_mat:,.2f}\n"
        f"Artisan Labor      : ₹{total_labor:,.2f}\n"
        f"Concealed Lighting : ₹{total_led:,.2f}\n"
        f"----------------------------------------------------------\n"
        f"ESTIMATED TOTAL    : ₹{grand_total:,.2f}\n"
        f"==========================================================\n"
    )

    st.download_button(
        label="📄 Download Client Proposal & Spec Sheet (.txt)",
        data=quote_text,
        file_name="Aesthetic_Design_Proposal.txt",
        mime="text/plain"
    )

else:
    st.info("👆 Upload an image or select a preset wall to begin.")
