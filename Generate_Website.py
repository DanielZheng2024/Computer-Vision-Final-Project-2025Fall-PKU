import streamlit as st
import os

st.set_page_config(layout="wide", page_title="Visual Cognitive Illusions Demo")

st.title("Visual Cognitive Illusions Project Demo")
st.markdown("### Interactive visualization of Tangram, Cylinder, and Anamorphic illusions")

import base64

def show_demo_section(title, image_path, gif_path, key_suffix):
    """
    Helper function to create a demo section with toggle functionality.
    """
    st.header(title)
    
    # Check file existence to avoid errors
    if not os.path.exists(image_path):
        st.error(f"Image not found at: {image_path}")
        return
    if not os.path.exists(gif_path):
        st.error(f"GIF not found at: {gif_path}")
        return

    # Use session state to keep track of what to show (Image or GIF)
    session_key = f"show_gif_{key_suffix}"
    if session_key not in st.session_state:
        st.session_state[session_key] = False

    # Layout: Image/GIF on the left, Controls/Description on the right
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if st.session_state[session_key]:
            # Show GIF using base64 and HTML to force browser animation
            try:
                with open(gif_path, "rb") as f:
                    contents = f.read()
                    data_url = base64.b64encode(contents).decode("utf-8")
                
                st.markdown(
                    f'<img src="data:image/gif;base64,{data_url}" style="width:100%; border-radius: 5px;">',
                    unsafe_allow_html=True,
                )
                st.caption(f"{title} - Animation")
            except Exception as e:
                st.error(f"Error loading GIF: {e}")
        else:
            # Show Static Image
            st.image(image_path, caption=f"{title} - Static View", use_column_width=True)

    with col2:
        st.write(f"**Control for {title}**")
        if st.session_state[session_key]:
            if st.button("⏹️ Stop Animation", key=f"stop_{key_suffix}"):
                st.session_state[session_key] = False
                st.rerun()
        else:
            if st.button("▶️ Play Animation", key=f"play_{key_suffix}"):
                st.session_state[session_key] = True
                st.rerun()
    
    st.divider()

# Base paths
base_pic_path = "Supplementary_Details/pictures"
base_demo_path = "Supplementary_Details/demos"

# 1. Learnable Tangram
# Image: tangram_text.png
# GIF: learnable_tangram_demo.gif
show_demo_section(
    "1. Learnable Tangram",
    os.path.join(base_pic_path, "tangram_image.png"),
    os.path.join(base_demo_path, "learnable_tangram_demo.gif"),
    "tangram"
)

# 2. Cylinder Reflection
# Image: Cylindrical_1.png
# GIF: cylinder_reflection_demo.gif
show_demo_section(
    "2. Cylinder Reflection",
    os.path.join(base_pic_path, "Cylindrical_1.png"),
    os.path.join(base_demo_path, "cylinder_reflection_demo.gif"),
    "cylinder"
)

# 3. Anamorphic Illusion
# Image: Anamorphic_1.png
# GIF: anamorphic_1.gif
show_demo_section(
    "3. Anamorphic Illusion",
    os.path.join(base_pic_path, "Anamorphic_1.png"),
    os.path.join(base_demo_path, "anamorphic_1.gif"),
    "anamorphic"
)
