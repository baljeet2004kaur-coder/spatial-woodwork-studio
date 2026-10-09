import streamlit as st
import urllib.parse
from PIL import Image
import requests
from io import BytesIO
import random

st.set_page_config(page_title="Dark Luxe Millwork & Architectural Woodwork", layout="wide")

st.title("🏛️ Dark Luxe Architectural Millwork & Studio Pro")
st.caption("Heavy bespoke woodwork, luxury dark finishes, automated production cut sheets, and commercial estimates.")

# ----------------- SIDEBAR DESIGN MATRIX -----------------
st.sidebar.header("🪵 Luxury Architectural Elements")

wood_style = st.sidebar.selectbox(
    "Heavy Millwork & Wall Style",
    [
        "Heavy Multi-Tier Classical Boiserie with Crown Moldings",
        "Deep Recessed Geometric Slat Paneling with Marble Nook",
        "Dramatic Fluted Pillar & Coffered Accent Wall",
        "Floating Smoked Dark TV Unit with Concealed Louver Panels",
        "Luxury Master Suite Headboard with Padded Suede & Heavy Wood Framing",
        "Gothic Contemporary Ribbed Wall with Heavy Archways"
    ]
)

wood_finish = st.sidebar.selectbox(
    "Dark & Rich Timber Species",
    [
        "Smoked Charcoal Ebonized Black Oak",
        "Dark Royal American Walnut (Deep Matte)",
        "Charred Shou Sugi Ban Wood with Satin Sheen",
        "Deep Espresso Teak with Visible Rich Grains",
        "Antique High-Gloss Rosewood & Black Stain"
    ]
)

metal_accent = st.sidebar.selectbox(
    "Metallic Inlays & Accents",
    [
        "Brushed Warm Gold / Brass Edge Trims",
        "Antique Burnished Bronze T-Profiles",
        "Matte Gunmetal Black Shadow Lines",
        "Raw Titanium Slate Inlays",
        "None (Pure Monolithic Dark Wood)"
    ]
)

design_mood = st.sidebar.selectbox(
    "Moody Aesthetic & Lighting",
    [
        "Moody High-End Penthouse Lounge (Deep Shadows, Warm Amber Glow)",
        "Ultra-Dark Modern Luxury (Monochrome Black, Razor-Sharp Lighting)",
        "Classic Heritage Cigar Club (Rich Walnut, Heavy Carvings, Sophisticated Warmth)",
        "Bespoke Italian Villa (Black Marquina Marble + Deep Ebonized Wood)"
    ]
)

st.sidebar.divider()
st.sidebar.header("💡 Lighting & Polish")
has_led = st.sidebar.checkbox("Concealed 2700K Deep Amber LED Glow Strips", value=True)
finish_type = st.sidebar.radio("Wood Finish Treatment", ["Deep Matte Velvet PU", "Satin Hand-Rubbed Oil", "Mirror High-Gloss Dark Italian Polyurethane"])

st.sidebar.divider()
st.sidebar.header("📐 Site Dimensions (ft)")
wall_w = st.sidebar.number_input("Wall Width (Feet)", min_value=4.0, max_value=40.0, value=14.0, step=0.5)
wall_h = st.sidebar.number_input("Wall Height (Feet)", min_value=6.0, max_value=16.0, value=10.5, step=0.5)

st.sidebar.divider()
st.sidebar.header("💰 Commercial Rates (₹ INR)")
core_substrate = st.sidebar.selectbox(
    "Substrate Grade",
    [
        "Heavy HDHMR Board + Natural Dark Veneer (₹450/sqft base)",
        "Calibrated Marine BWP Ply + Smoked Oak Veneer (₹520/sqft base)",
        "Solid Hardwood Battens + Dark PU Polish (₹680/sqft base)"
    ]
)

base_rates = {
    "Heavy HDHMR Board + Natural Dark Veneer (₹450/sqft base)": 450,
    "Calibrated Marine BWP Ply + Smoked Oak Veneer (₹520/sqft base)": 520,
    "Solid Hardwood Battens + Dark PU Polish (₹680/sqft base)": 680
}

sqft_material_rate = st.sidebar.number_input("Base Material Rate (₹/sqft)", value=base_rates[core_substrate], step=25)
sqft_labor_rate = st.sidebar.number_input("Skilled Joinery & Polishing Labor (₹/sqft)", value=220, step=10)

# Calculations
sqft = wall_w * wall_h
ply_sheets = int((sqft * 1.15) // 32) + 1  # 15% waste buffer for heavy moldings
slat_linear_ft = int(wall_w * (wall_h / 0.35))
led_linear_ft = (wall_w * 2) if has_led else 0.0
metal_inlay_cost = (wall_w * 4 * 220) if "None" not in metal_accent else 0

total_material_cost = sqft * sqft_material_rate
total_labor_cost = sqft * sqft_labor_rate
total_led_cost = (led_linear_ft * 250) if has_led else 0
grand_total = total_material_cost + total_labor_cost + total_led_cost + metal_inlay_cost

# ----------------- INPUT CONTROLS -----------------
input_mode = st.radio("Wall Reference:", ["Upload Room Photo", "Use Curated Dark Luxury Wall"], horizontal=True)

active_image = None

if input_mode == "Upload Room Photo":
    uploaded_file = st.file_uploader("Upload wall photo", type=["jpg", "png", "jpeg"])
    if uploaded_file is not None:
        try:
            active_image = Image.open(uploaded_file)
        except Exception:
            st.error("⚠️ Invalid image format.")
else:
    preset_choice = st.selectbox(
        "Select Room Context:",
        [
            "Dark Modern Living Room / TV Wall",
            "Executive Master Suite Accent Wall",
            "Moody Architectural Foyer / Gallery"
        ]
    )
    demo_urls = {
        "Dark Modern Living Room / TV Wall": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=900&q=80",
        "Executive Master Suite Accent Wall": "https://images.unsplash.com/photo-1616594039964-ae9021a400a0?w=900&q=80",
        "Moody Architectural Foyer / Gallery": "https://images.unsplash.com/photo-1513694203232-719a280e022f?w=900&q=80"
    }
    try:
        resp = requests.get(demo_urls[preset_choice])
        active_image = Image.open(BytesIO(resp.content))
    except Exception:
        st.warning("Demo image offline. Please upload a photo.")

# ----------------- CUSTOM RENDER ENGINE -----------------
if active_image is not None:
    c_left, c_right = st.columns([1, 1.25])
    
    with c_left:
        st.subheader("Base Room Reference")
        st.image(active_image, use_container_width=True)

    with c_right:
        st.subheader("Bespoke Dark Luxury Concept")
        
        # New Feature: Custom prompt fine-tuning
        custom_notes = st.text_input(
            "Custom Architectural Detail / Note (Optional):",
            placeholder="e.g. Add black Italian marble niche, bronze book-match inlays, low moody light"
        )
        
        num_variations = st.select_slider("Generate Variations:", options=[1, 2, 3], value=1)
        
        led_str = "concealed warm 2700K amber indirect cove illumination emphasizing wood texture" if has_led else "moody cinematic chiaroscuro directional spotlighting"
        metal_str = f"highlighted with precision {metal_accent}" if "None" not in metal_accent else ""
        custom_extra = f", {custom_notes}" if custom_notes.strip() else ""

        if st.button("🔥 Render Dark Luxury Woodwork", type="primary"):
            st.toast("Generating dark luxury concept...")
            
            concept_cols = st.columns(num_variations)
            
            for i in range(num_variations):
                rand_seed = random.randint(100000, 9999999)
                
                # Dark, heavy, moody architectural prompt engineering
                prompt = (
                    f"Architectural Digest luxury interior photography, {design_mood}, "
                    f"dramatic monumental accent wall featuring {wood_style}, "
                    f"crafted from {wood_finish} with {finish_type}, "
                    f"{metal_str}, {led_str}{custom_extra}, "
                    f"heavy bespoke carpentry, thick solid profiles, bold reveals, deep shadows, "
                    f"rich textural depth, dark aesthetic, 8k resolution, photorealistic masterpiece"
                )
                
                encoded_prompt = urllib.parse.quote(prompt)
                image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=768&nologo=true&seed={rand_seed}"
                
                resp = requests.get(image_url)
                if resp.status_code == 200:
                    with concept_cols[i]:
                        st.image(resp.content, caption=f"Dark Luxe Concept #{i+1} (ID: {rand_seed})", use_container_width=True)
                        st.download_button(
                            label=f"💾 Download Render #{i+1}",
                            data=resp.content,
                            file_name=f"Dark_Luxe_{wood_style[:12]}_{rand_seed}.png",
                            mime="image/png",
                            key=f"dl_{i}_{rand_seed}"
                        )

    st.divider()

    # ----------------- PRODUCTION & FINANCIAL METRICS -----------------
    st.subheader("📋 Heavy Millwork Cut-Sheet Requisition")
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    col_m1.metric("Wall Face Area", f"{sqft:.1f} sq.ft")
    col_m2.metric("Core Plywood / HDHMR (8x4)", f"{ply_sheets} Sheets")
    col_m3.metric("Heavy Battens / Louvers", f"~{slat_linear_ft} RFT")
    col_m4.metric("Concealed LED Channels", f"{led_linear_ft:.1f} RFT" if has_led else "None")

    st.subheader("💼 Commercial Project Budget Estimate")
    col_b1, col_b2, col_b3, col_b4 = st.columns(4)
    col_b1.metric("Substrate & Veneers", f"₹{total_material_cost:,.0f}")
    col_b2.metric("Master Joinery & PU Polish", f"₹{total_labor_cost:,.0f}")
    col_b3.metric("Lighting & Metal Inlays", f"₹{(total_led_cost + metal_inlay_cost):,.0f}")
    col_b4.metric("Total Client Quotation", f"₹{grand_total:,.0f}")

    # Proposal download
    quote_text = (
        f"==========================================================\n"
        f"       LUXURY MILLWORK SPECIFICATION & CLIENT PROPOSAL\n"
        f"==========================================================\n\n"
        f"Design Concept     : {wood_style}\n"
        f"Species & Finish   : {wood_finish} ({finish_type})\n"
        f"Metal Accents      : {metal_accent}\n"
        f"Substrate Core     : {core_substrate}\n\n"
        f"--- SITE MEASUREMENTS ---\n"
        f"Wall Dimensions    : {wall_w:.1f} ft (W) x {wall_h:.1f} ft (H)\n"
        f"Coverage Area      : {sqft:.1f} sq.ft.\n\n"
        f"--- MATERIAL REQUISITION ---\n"
        f"8x4 Substrate Core : {ply_sheets} Boards (Includes 15% heavy profile allowance)\n"
        f"Profiles & Moldings: ~{slat_linear_ft} Running Feet\n"
        f"LED Extrusions     : {led_linear_ft:.1f} Running Feet\n\n"
        f"--- COMMERCIAL BREAKDOWN (INR) ---\n"
        f"Material Subtotal  : ₹{total_material_cost:,.2f}\n"
        f"Carpentry & Polish : ₹{total_labor_cost:,.2f}\n"
        f"LED Channels       : ₹{total_led_cost:,.2f}\n"
        f"Metallic Trims     : ₹{metal_inlay_cost:,.2f}\n"
        f"----------------------------------------------------------\n"
        f"ESTIMATED TOTAL    : ₹{grand_total:,.2f}\n"
        f"==========================================================\n"
    )

    st.download_button(
        label="📄 Download Luxury Project Proposal & Cut Sheet (.txt)",
        data=quote_text,
        file_name="Dark_Luxe_Proposal.txt",
        mime="text/plain"
    )

else:
    st.info("👆 Upload a room photo or pick a sample layout above to begin.")
