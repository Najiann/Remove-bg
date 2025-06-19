# 🖼️ Background Remover - Batch Mode

A simple and interactive web app to remove backgrounds from images in **batch mode** using [rembg](https://github.com/danielgatis/rembg) and [Streamlit](https://streamlit.io/). Users can optionally **replace the background** with a **color** or **custom image**.

---

## ✨ Features

- ✅ Upload multiple images (`.png`, `.jpg`, `.jpeg`)
- 🧼 Remove image background using `rembg`
- 🎨 Replace background with:
  - Solid color (`color_picker`)
  - Custom image
- 🖼️ Side-by-side preview (before & after)
- 💾 Download results individually

---

## 🚀 How to Run

### 1. Clone the Repository
```bash
git clone https://github.com/Najiann/remove_bg.git
cd remove_bg
```

### 2. Create Virtual Environment (optional but recommended)
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the App
```bash
streamlit run app.py
```

---

## 📦 Dependencies

- `streamlit`
- `rembg`
- `Pillow`

---

## 📸 Screenshot

| Before | After |
|--------|-------|
| ![before](https://via.placeholder.com/300x200?text=Sebelum) | ![after](https://via.placeholder.com/300x200?text=Sesudah) |

---

## 🛠️ To-Do (Optional Enhancements)

- [ ] Magic brush (manual masking)
- [ ] Batch download (ZIP)
- [ ] Preview background overlay
- [ ] Save session history

---

## 📄 License

MIT License — feel free to use and modify.

---

## 🙌 Credits

Built with ❤️ using:
- [Streamlit](https://streamlit.io/)
- [rembg](https://github.com/danielgatis/rembg)
- [Pillow](https://python-pillow.org/)