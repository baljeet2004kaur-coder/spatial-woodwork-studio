import streamlit as st
import urllib.parse
from PIL import Image
import requests
from io import BytesIO
import random

st.set_page_config(page_title="Ultra-Luxury Dark Millwork & Studio", layout="wide")

st.title("🏛️ Dark Luxurious Architectural Millwork & TV Console Studio")
st.caption("Bespoke dark, heavy millwork, layered accent lighting, automated cut-sheets, and client pricing estimates.")

# ----------------- SIDEBAR DESIGN MATRIX -----------------
st.sidebar.header("🪵 Luxury Architectural Elements")

wood_style = st.sidebar.selectbox(
    "Heavy Custom Wall Style",
    [
        "Organic Cascading S-Curve Panels with Built-in TV Niche & Fluted Battens",
        "Arched Recessed Shelving Nook with Curved LED Borders & Accent Slats",
        "Layered Dimensional Wave Walls with Integrated TV & Floating Console",
        "Heavy Fluted Pillars & Curved Alcoves with Backlit Veneer Layers",
        "Intricate Paneling with Arc Cutouts, Fluted Inlays & Bed Frame Framing",
        "Geometric 3D Overlays with Rounded Shelves & Floating Storage Bays"
    ]
)

wood_finish = st.sidebar.selectbox(
    "Dark Luxurious Timber & Materials",
    [
        "Smoked Dark Charcoal Oak & Textured Slate Plaster",
        "Deep Royal American Walnut with Matte Backlit Panels",
        "Ebonized Black Ash with Natural Warm Timber Accents",
        "Rich Espresso Teak with Metallic Inlays & Rough Sand Plaster",
        "Antique Hand-Rubbed Rosewood with Charcoal Slat Accents"
    ]
)

metal_accent = st.sidebar.selectbox(
    "Custom Metallic Trim Highlights",
    [
        "Brushed Champagne Gold Edge Profiles",
        "Antique Burnished Bronze T-Profiles",
        "Matte Gunmetal Black Trim Highlights",
        "None (Heavy Pure Wood Layers)"
    ]
)

design_mood = st.sidebar.selectbox(
    "Interior Atmosphere & Aesthetics",
    [
        "High-End Dark Penthouse Lounge (Amber Glow, Deep Shadow Contrast)",
        "Luxury Hotel Suite (Earthy Charcoal Wood, Warm Layered Backlighting)",
        "Contemporary Architectural Digest (Dramatic Organic Curves, Rich Walnut)",
        "Modern Moody Elite (Deep Black Marquina Marble, Heavy Fluted Details)"
    ]
)

st.sidebar.divider()
st.sidebar.header("📐 Site Dimensions (ft)")
wall_w = st.sidebar.number_input("Wall Width (Feet)", min_value=4.0, max_value=40.0, value=14.0, step=0.5)
wall_h = st.sidebar.number_input("Wall Height (Feet)", min_value=6.0, max_value=16.0, value=10.0, step=0.5)

st.sidebar.divider()
st.sidebar.header("💰 Cost Estimate Rates (₹ INR)")
core_substrate = st.sidebar.selectbox(
    "Core Material Grade",
    [
        "Heavy HDHMR Board + Charcoal Veneer (₹450/sqft base)",
        "Calibrated BWP Marine Ply + Royal Walnut Veneer (₹550/sqft base)",
        "High-Grade Solid Wood & Curved Custom Framing (₹680/sqft base)"
    ]
)

base_rates = {
    "Heavy HDHMR Board + Charcoal Veneer (₹450/sqft base)": 450,
    "Calibrated BWP Marine Ply + Royal Walnut Veneer (₹550/sqft base)": 550,
    "High-Grade Solid Wood & Curved Custom Framing (₹680/sqft base)": 680
}

sqft_material_rate = st.sidebar.number_input("Material Rate (₹/sqft)", value=base_rates[core_substrate], step=25)
sqft_labor_rate = st.sidebar.number_input("Carpentry & Fine Finish Labor (₹/sqft)", value=220, step=10)

# ----------------- CALCULATIONS -----------------
sqft = wall_w * wall_h
ply_sheets = int((sqft * 1.18) // 32) + 1  # 18% waste allowance for curved cuts & layered overlays
slat_linear_ft = int(wall_w * (wall_h / 0.35))
led_linear_ft = (wall_w * 2.5)  # More intricate LED curves mean extra LED length
metal_inlay_cost = (wall_w * 4 * 220) if "None" not in metal_accent else 0

total_material_cost = sqft * sqft_material_rate
total_labor_cost = sqft * sqft_labor_rate
total_led_cost = (led_linear_ft * 250)
grand_total = total_material_cost + total_labor_cost + total_led_cost + metal_inlay_cost

# ----------------- MAIN INTERFACE -----------------
input_mode = st.radio("Choose Input:", ["Upload Room Photo", "Use Demo Preset Wall"], horizontal=True)

active_image = None

if input_mode == "Upload Room Photo":
    uploaded_file = st.file_uploader("Upload wall photo", type=["jpg", "png", "jpeg"])
    if uploaded_file is not None:
        try:
            active_image = Image.open(uploaded_file)
        except Exception:
            st.error("⚠️ Could not read image. Try a JPG or PNG.")
else:
    preset_choice = st.selectbox(
        "Select a Sample Layout:",
        ["Contemporary Living Room Wall", "Executive Bedroom Accent Wall", "Modern Foyer Nook"]
    )
    demo_urls = {
        "Contemporary Living Room Wall": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=900&q=80",
        "Executive Bedroom Accent Wall": "https://images.unsplash.com/photo-1616594039964-ae9021a400a0?w=900&q=80",
        "Modern Foyer Nook": "https://images.unsplash.com/photo-1513694203232-719a280e022f?w=900&q=80"
    }
    try:
        resp = requests.get(demo_urls[preset_choice])
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
        st.subheader("Luxury Architectural Design Transformation")
        
        custom_notes = st.text_input(
            "Add Specific Design Customizations (Optional):",
            placeholder="e.g. Add dark Italian marble backing, display shelves, curved alcove"
        )
        
        # S-Curve, Layers & Arc custom prompts
        prompt_style_details = (
            "intricate custom architectural focal accent wall featuring monumental layered curvilinear backdrops, "
            "cascading 3D organic S-curve panels, integrated recessed arched shelving alcoves, "
            "deeply textured vertical fluted timber slats, heavy wood moldings, seamless custom floating media console unit, "
            "integrated shelf displays, layered backlighting"
        )
        
        lighting_str = "intricate concealed glowing warm 2700K LED amber strip backlighting following the organic curves, indirect cove illumination emphasizing the layered 3D depth, rich ambient shadow"
        metal_str = f"interwoven with precision luxurious {metal_accent}" if "None" not in metal_accent else "high-contrast multi-tier reveals"
        custom_text = f", featuring {custom_notes}" if custom_notes.strip() else ""

        # BUTTON REPLACED AND SIMPLIFIED AS REQUESTED
        if st.button("✨ Generate Design", type="primary"):
            with st.spinner("Engineering high-contrast dark luxury concept..."):
                rand_seed = random.randint(100000, 9999999)
                
                # Full luxurious, high-end dark bespoke image prompt
                prompt = (
                    f"A prestigious Architectural Digest interior photograph, {design_mood}, "
                    f"{prompt_style_details} finished in rich, premium {wood_finish}, "
                    f"coated in silk satin protective coat, {metal_str}, {lighting_str}{custom_text}. "
                    f"Crafted with heavy bespoke joinery, deep three-dimensional overlay panels, and majestic organic curves, "
                    f"staged within an elite luxury master suite or living area. High-end natural lighting contrast, "
                    f"heavy dark aesthetic, cinematic shadows, rich natural textures, 8k resolution, flawless photorealistic masterpiece"
                )
                
                encoded_prompt = urllib.parse.quote(prompt)
                image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=768&nologo=true&seed={rand_seed}"
                
                resp = requests.get(image_url)
                if resp.status_code == 200:
                    st.image(resp.content, use_container_width=True)
                    st.success("Unique architectural render generated successfully!")
                    
                    st.download_button(
                        label="💾 Download 3D Render (PNG)",
                        data=resp.content,
                        file_name=f"Luxury_Dark_Millwork_{rand_seed}.png",
                        mime="image/png"
                    )

    st.divider()
    
    # Material Metrics
    st.subheader("📋 Bespoke Millwork Cut-Sheet & Materials Estimate")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Wall Area", f"{sqft:.1f} sq.ft.")
    m2.metric("Core Plywood / HDHMR", f"{ply_sheets} Sheets")
    m3.metric("Intricate Battens / Slats", f"~{slat_linear_ft} Running Feet")
    m4.metric("Ambient LED Channels", f"~{led_linear_ft:.1f} RFT")

    # Cost Metrics
    st.subheader("💵 Financial Proposal Summary")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Materials & Core Veneer", f"₹{total_material_cost:,.0f}")
    c2.metric("Custom Carpentry & Finishing", f"₹{total_labor_cost:,.0f}")
    c3.metric("Heavy Lighting & Inlays", f"₹{(total_led_cost + metal_inlay_cost):,.0f}")
    c4.metric("Estimated Project Value", f"₹{grand_total:,.0f}")

    # Project Proposal Exporter
    quote_text = (
        f"==========================================================\n"
        f"       ULTRA-LUXURY BESPOKE MILLWORK SPECIFICATION PROPOSAL\n"
        f"==========================================================\n\n"
        f"Wall Style Detail  : {wood_style}\n"
        f"Finish Species     : {wood_finish}\n"
        f"Design Contrast    : {design_mood}\n"
        f"Metallic Accents   : {metal_accent}\n"
        f"Core Substrate     : {core_substrate}\n\n"
        f"--- SITE SPECIFICATIONS ---\n"
        f"Surface Size       : {wall_w:.1f} ft (W) x {wall_h:.1f} ft (H)\n"
        f"Calculated Area    : {sqft:.1f} sq.ft.\n\n"
        f"--- PRODUCTION MATERIAL REQUISITION ---\n"
        f"Core Sheets (8x4)  : {ply_sheets} Boards (Includes 18% allowance for layered custom curves)\n"
        f"Decorative Battens : ~{slat_linear_ft} Running Feet\n"
        f"Custom LED Extrusion: {led_linear_ft:.1f} Running Feet (Curve detailed)\n\n"
        f"--- COMMERCIAL PROJECT ESTIMATION (INR) ---\n"
        f"Core & Veneer Cost : ₹{total_material_cost:,.2f}\n"
        f"Skilled Handcrafting: ₹{total_labor_cost:,.2f}\n"
        f"Layered LED & Tracks: ₹{total_led_cost:,.2f}\n"
        f"Inlays & Trims     : ₹{metal_inlay_cost:,.2f}\n"
        f"----------------------------------------------------------\n"
        f"GRAND ESTIMATED TOTAL : ₹{grand_total:,.2f}\n"
        f"==========================================================\n"
    )

    st.download_button(
        label="📄 Download Contractor Specification & Client Proposal (.txt)",
        data=quote_text,
        file_name="Premium_Layered_Woodwork_Quote.txt",
        mime="text/plain"
    )

else:
    st.info("👆 Upload an image or select a preset wall to begin.")
