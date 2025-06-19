import streamlit as st
from rembg import remove
from PIL import Image
import requests
import io
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
REMOVE_BG_API_KEY = os.getenv("REMOVE_BG_API_KEY")

# fungsi replace background
def replace_background_with_color(fg_img, color=(255, 255, 255, 255)):
    bg = Image.new("RGBA", fg_img.size, color)
    return Image.alpha_composite(bg, fg_img)

def replace_background_with_image(fg_img, bg_img):
    bg_resized = bg_img.resize(fg_img.size)
    return Image.alpha_composite(bg_resized, fg_img)

# hybrid nya ini
def remove_bg_auto(file, api_key=None):
    if api_key:
        try:
            file_bytes = file.read()
            response = requests.post(
                "https://api.remove.bg/v1.0/removebg",
                files={"image_file": ("image.png", file_bytes, "image/png")},
                data={"size": "auto"},
                headers={"X-Api-Key": api_key},
                timeout=10
            )

            if response.status_code == 200:
                st.success("✅ Gambar ini diproses via API Remove.bg")
                return Image.open(io.BytesIO(response.content))
            else:
                st.warning(f"Gagal pakai API ({response.status_code}) → pakai lokal.")
        except Exception as e:
            st.warning(f"Tidak bisa konek ke API → pakai lokal. ({str(e)})")

    # fallback to local
    return remove(Image.open(file).convert("RGBA"))

# UI STREAMLIT
st.set_page_config(page_title="Remove BG Batch App", layout="wide")
st.title("🖼️ Background Remover - Batch Mode")

uploaded_files = st.file_uploader("📤 Upload Gambar! ", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

if uploaded_files: 
    st.markdown("### ➡️ Pilih Aksi Setelah Remove BG:")
    option = st.radio("Pilih:", ["Remove-only", "Ganti Warna Background", "Ganti Gambar Background"])

    selected_color = None
    bg_img = None

    if option == "Ganti Warna Background":
        hex_color = st.color_picker("🎨 Pilih warna background", "#ffffff")
        r, g, b = tuple(int(hex_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        selected_color = (r, g, b, 255)

    elif option == "Ganti Gambar Background":
        bg_file = st.file_uploader("Upload gambar background", type=["png", "jpg", "jpeg"])
        if bg_file:
            bg_img = Image.open(bg_file).convert("RGBA")

    if st.button("🚀 Proses Semua Gambar"):
        for i, uploaded_file in enumerate(uploaded_files):
            st.markdown(f"---\n### 🖼️ Gambar {i+1}: `{uploaded_file.name}`")
            input_image = Image.open(uploaded_file).convert("RGBA")

            # Reset pointer karena akan dibaca dua kali (API dan preview)
            uploaded_file.seek(0)
            input_image = Image.open(uploaded_file).convert("RGBA")

            # Reset lagi sebelum dikirim ke API
            uploaded_file.seek(0)
            fg = remove_bg_auto(uploaded_file, REMOVE_BG_API_KEY)

            if option == "Remove-only":
                result = fg
            elif option == "Ganti Warna Background":
                result = replace_background_with_color(fg, selected_color)
            elif option == "Ganti Gambar Background" and bg_img:
                result = replace_background_with_image(fg, bg_img)
            else:
                st.warning("❗ Upload background gambar dulu.")
                continue

            # TAMPILKAN SIDE-BY-SIDE
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**📥 Sebelum**")
                st.image(input_image, width=300)

            with col2:
                st.markdown("**📤 Sesudah**")
                st.image(result, width=300)

            # TOMBOL DOWNLOAD
            output = io.BytesIO()
            result.save(output, format="PNG")
            st.download_button(
                label="💾 Download Gambar",
                data=output.getvalue(),
                file_name=f"{uploaded_file.name.rsplit('.', 1)[0]}_hasil.png",
                mime="image/png"
            )
