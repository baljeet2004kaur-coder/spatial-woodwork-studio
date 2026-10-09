if st.button("✨ Generate Design", type="primary"):
            with st.spinner("Curating high-aesthetic modern render..."):
                prompt = (
                    f"Aesthetic modern interior, {vibe_theme}, "
                    f"luxury minimalist TV wall, {wood_style}, "
                    f"finished in {color_palette}, {accent_trim}, "
                    f"sculptural organic curves, floating rounded credenza, "
                    f"warm 2700k indirect LED halo lighting, soft daylight, 8k resolution{custom_extra}"
                )
                
                encoded_prompt = urllib.parse.quote(prompt)
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
                
                resp = None
                # Auto-retry loop to beat temporary server traffic
                for attempt in range(3):
                    rand_seed = random.randint(1000, 99999)
                    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=800&height=800&nologo=true&seed={rand_seed}&model=flux"
                    try:
                        resp = requests.get(image_url, headers=headers, timeout=25)
                        if resp.status_code == 200 and len(resp.content) > 5000:
                            break
                    except Exception:
                        continue

                if resp and resp.status_code == 200 and len(resp.content) > 5000:
                    st.image(resp.content, use_container_width=True)
                    st.success("New aesthetic design generated!")
                    
                    st.download_button(
                        label="💾 Download Render (PNG)",
                        data=resp.content,
                        file_name=f"Aesthetic_Design_{rand_seed}.png",
                        mime="image/png"
                    )
                else:
                    st.error("The free image server is under heavy load. Please click 'Generate Design' once more.")
