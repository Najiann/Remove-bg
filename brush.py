import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np
import io

st.set_page_config(page_title="🖌️ Brush Background Remover", layout="wide")
st.title("🎨 Manual Brush - Remove Bagian Gambar")

uploaded_file = st.file_uploader("📤 Upload gambar", type=["png", "jpg", "jpeg"])

if uploaded_file:
    input_image = Image.open(uploaded_file).convert("RGBA")
    img_width, img_height = input_image.size
    bg_image_np = np.array(input_image)  # ✅ convert ke numpy

    st.markdown("🖌️ **Gambarlah area yang mau dihapus (pakai kuas)**")

    canvas_result = st_canvas(
        fill_color="rgba(255, 0, 0, 0.5)",
        stroke_width=20,
        stroke_color="#FF0000",
        background_image=input_image,
        update_streamlit=True,
        height=img_height,
        width=img_width,
        drawing_mode="freedraw",
        key="canvas",
    )

    if canvas_result.image_data is not None and st.button("🚀 Hapus Area yang Ditandai"):
        mask_data = canvas_result.image_data[:, :, 3]
        mask = mask_data > 0

        np_img = np.array(input_image)
        np_img[mask] = [0, 0, 0, 0]

        result = Image.fromarray(np_img)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**📥 Sebelum**")
            st.image(input_image)

        with col2:
            st.markdown("**📤 Sesudah (area disapu brush dihapus)**")
            st.image(result)

        output = io.BytesIO()
        result.save(output, format="PNG")
        st.download_button(
            label="💾 Download Gambar",
            data=output.getvalue(),
            file_name="gambar_brush_removed.png",
            mime="image/png"
        )
