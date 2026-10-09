import streamlit as st
import urllib.parse
from PIL import Image
import requests
from io import BytesIO
import random

st.set_page_config(page_title="Spatial Woodwork Studio Pro", layout="wide")

st.title("🏛️ Architectural Woodwork & Millwork Studio Pro")
st.caption("AI-powered architectural woodworking, automated cut-sheets, and commercial project budgeting.")

# ----------------- SIDEBAR DESIGN MATRIX -----------------
st.sidebar.header("🪵 Architectural Elements")

wood_style = st.sidebar.selectbox(
    "Wall Style & Millwork",
    [
        "Vertical Fluted Slats (Batten)",
        "Chevron Herringbone Parquet Paneling",
        "Floating Bed Headboard with Integrated Nightstands",
        "Minimalist Floating TV Console with Slat Backing",
        "Curved Fluted Wall with Concealed Alcoves",
        "Traditional French Wainscoting & Bolection Moldings",
        "Parametric Wave 3D Wood Paneling"
    ]
)

wood_finish = st.sidebar.selectbox(
    "Timber Species & Finish",
    [
        "Warm Natural Burma Teak",
        "Smoked American Walnut",
        "Scandinavian Bleached White Oak",
        "Charcoal Ebonized Ash",
        "Rich Sheesham / Indian Rosewood"
    ]
)

metal_accent = st.sidebar.selectbox(
    "Inlay / Trim Accents",
    [
        "None (Pure Wood)",
        "Brushed Champagne Gold T-Profiles",
        "Matte Black Anodized Slim Trims",
        "Antique Rose Brass Strips"
    ]
)

design_mood = st.sidebar.selectbox(
    "Spatial Vibe & Lighting Theme",
    [
        "Minimalist Japandi Serenity",
        "Ultra-Luxury Penthouse Suite",
        "Architectural Digest Editorial",
        "Moody Dark Luxe Lounge"
    ]
)

st.sidebar.divider()
st.sidebar.header("💡 Lighting & Polish")
has_led = st.sidebar.checkbox("Concealed 3000K Warm LED Strip Channels", value=True)
finish_type = st.sidebar.radio("Coating Finish", ["Natural Matte PU", "Silky Satin", "Deep High-Gloss Italian Polyurethane"])

st.sidebar.divider()
st.sidebar.header("📐 Site Dimensions (ft)")
wall_w = st.sidebar.number_input("Wall Width (Feet)", min_value=4.0, max_value=40.0, value=14.0, step=0.5)
wall_h = st.sidebar.number_input("Wall Height (Feet)", min_value=6.0, max_value=16.0, value=10.0, step=0.5)

st.sidebar.divider()
st.sidebar.header("💰 Commercial Pricing (₹ INR)")
core_substrate = st.sidebar.selectbox(
    "Substrate Grade",
    [
        "Standard BWP Marine Plywood (₹320/sqft base)",
        "Action TESA HDHMR Board (₹280/sqft base)",
        "Premium Calibrated Plywood + Natural Veneer (₹480/sqft base)"
    ]
)

base_rates = {
    "Standard BWP Marine Plywood (₹320/sqft base)": 320,
    "Action TESA HDHMR Board (₹280/sqft base)": 280,
    "Premium Calibrated Plywood + Natural Veneer (₹480/sqft base)": 480
}

sqft_material_rate = st.sidebar.number_input("Base Material Rate (₹/sqft)", value=base_rates[core_substrate], step=20)
sqft_labor_rate = st.sidebar.number_input("Skilled Carpentry & Polish Labor (₹/sqft)", value=160, step=10)

# Calculations
sqft = wall_w * wall_h
ply_sheets = int((sqft * 1.12) // 32) + 1  # 12% cutting waste buffer
slat_linear_ft = int(wall_w * (wall_h / 0.4)) if "Slats" in wood_style or "Wave" in wood_style else int(wall_w * 5)
led_linear_ft = wall_w if has_led else 0.0
metal_inlay_cost = (wall_w * 4 * 180) if metal_accent != "None (Pure Wood)" else 0

total_material_cost = sqft * sqft_material_rate
total_labor_cost = sqft * sqft_labor_rate
total_led_cost = (led_linear_ft * 220) if has_led else 0
grand_total = total_material_cost + total_labor_cost + total_led_cost + metal_inlay_cost

# ----------------- INPUT CONTROLS -----------------
input_mode = st.radio("Wall Source:", ["Upload Room Photo", "Use Curated Demo Wall"], horizontal=True)

active_image = None

if input_mode == "Upload Room Photo":
    uploaded_file = st.file_uploader("Upload bare wall photo", type=["jpg", "png", "jpeg"])
    if uploaded_file is not None:
        try:
            active_image = Image.open(uploaded_file)
        except Exception:
            st.error("⚠️ Invalid image format. Please upload a standard JPG or PNG.")
else:
    preset_choice = st.selectbox(
        "Choose an interior wall layout:",
        [
            "Empty Modern Living Room Wall",
            "Master Bedroom Plain Headboard Wall",
            "Luxury Foyer / Passage Nook"
        ]
    )
    demo_urls = {
        "Empty Modern Living Room Wall": "https://images.unsplash.com/photo-1513694203232-719a280e022f?w=800&q=80",
        "Master Bedroom Plain Headboard Wall": "https://images.unsplash.com/photo-1616594039964-ae9021a400a0?w=800&q=80",
        "Luxury Foyer / Passage Nook": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800&q=80"
    }
    try:
        resp = requests.get(demo_urls[preset_choice])
        active_image = Image.open(BytesIO(resp.content))
    except Exception:
        st.warning("Sample image offline. Please upload a local photo.")

# ----------------- DESIGN GENERATION -----------------
if active_image is not None:
    c_left, c_right = st.columns([1, 1.2])
    
    with c_left:
        st.subheader("Base Wall")
        st.image(active_image, use_container_width=True)

    with c_right:
        st.subheader("Architectural Transformation")
        
        num_variations = st.select_slider("Generate Concepts:", options=[1, 2, 3], value=1)
        
        led_prompt_text = "recessed ambient 3000k indirect LED strip glow" if has_led else "pure natural sun rays casting soft directional shadows"
        accent_prompt_text = f"detailed with luxury {metal_accent}" if metal_accent != "None (Pure Wood)" else ""

        if st.button("🚀 Render Custom Woodwork Concepts", type="primary"):
            st.toast("Generating custom designs...")
            
            concept_cols = st.columns(num_variations)
            
            for i in range(num_variations):
                rand_seed = random.randint(10000, 999999)
                prompt = (
                    f"Award-winning interior architecture photograph, {design_mood}, "
                    f"accent wall showcasing custom millwork {wood_style} finished in authentic {wood_finish} with {finish_type}, "
                    f"{accent_prompt_text}, {led_prompt_text}, pristine craftsmanship, sharp flutes and reveals, "
                    f"8k resolution, architectural catalog quality"
                )
                
                encoded_prompt = urllib.parse.quote(prompt)
                image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=800&height=600&nologo=true&seed={rand_seed}"
                
                resp = requests.get(image_url)
                if resp.status_code == 200:
                    with concept_cols[i]:
                        st.image(resp.content, caption=f"Option #{i+1} (ID: {rand_seed})", use_container_width=True)
                        st.download_button(
                            label=f"💾 Save Render #{i+1}",
                            data=resp.content,
                            file_name=f"Woodwork_Option_{i+1}_{rand_seed}.png",
                            mime="image/png",
                            key=f"dl_{i}_{rand_seed}"
                        )

    st.divider()

    # ----------------- DELIVERABLES & SPECS -----------------
    st.subheader("📋 Production Cut Sheet & Engineering Schedule")
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    col_m1.metric("Wall Area", f"{sqft:.1f} sq.ft")
    col_m2.metric("Core Sheets (8x4 ft)", f"{ply_sheets} Sheets")
    col_m3.metric("Linear Battens/Profiles", f"~{slat_linear_ft} RFT")
    col_m4.metric("Concealed LED Channels", f"{led_linear_ft:.1f} RFT" if has_led else "None")

    st.subheader("💼 Commercial Project Budget Estimate")
    col_b1, col_b2, col_b3, col_b4 = st.columns(4)
    col_b1.metric("Raw Materials & Core", f"₹{total_material_cost:,.0f}")
    col_b2.metric("Carpentry & Finishing", f"₹{total_labor_cost:,.0f}")
    col_b3.metric("Lighting & Accents", f"₹{(total_led_cost + metal_inlay_cost):,.0f}")
    col_b4.metric("Estimated Client Quote", f"₹{grand_total:,.0f}")

    # Project Quote Exporter
    quote_text = (
        f"==========================================================\n"
        f"       ARCHITECTURAL MILLWORK PROPOSAL & CUT SHEET\n"
        f"==========================================================\n\n"
        f"Style & Detail     : {wood_style}\n"
        f"Timber / Species   : {wood_finish}\n"
        f"Top Polish         : {finish_type}\n"
        f"Accent Trims       : {metal_accent}\n"
        f"Substrate Material : {core_substrate}\n\n"
        f"--- SITE SPECIFICATIONS ---\n"
        f"Surface Dimensions : {wall_w:.1f} ft (W) x {wall_h:.1f} ft (H)\n"
        f"Total Area         : {sqft:.1f} sq.ft.\n\n"
        f"--- ESTIMATED MATERIAL REQUISITION ---\n"
        f"Substrate Sheets   : {ply_sheets} Sheets (8ft x 4ft calibrated, incl 12% buffer)\n"
        f"Molding / Battens  : ~{slat_linear_ft} Running Feet\n"
        f"LED Aluminum Track : {led_linear_ft:.1f} Running Feet\n\n"
        f"--- FINANCIAL SUMMARY (INR) ---\n"
        f"Material Subtotal  : ₹{total_material_cost:,.2f}\n"
        f"Skilled Labor/PU   : ₹{total_labor_cost:,.2f}\n"
        f"Lighting Channels  : ₹{total_led_cost:,.2f}\n"
        f"Metal Profiles     : ₹{metal_inlay_cost:,.2f}\n"
        f"----------------------------------------------------------\n"
        f"ESTIMATED TOTAL    : ₹{grand_total:,.2f}\n"
        f"==========================================================\n"
    )

    st.download_button(
        label="📄 Download Contractor Specification & Client Proposal (.txt)",
        data=quote_text,
        file_name="Millwork_Project_Proposal.txt",
        mime="text/plain"
    )

else:
    st.info("👆 Select a demo wall or upload a photo to launch the designer.")
