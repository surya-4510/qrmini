import streamlit as st
import qrcode
from PIL import Image
import cv2
import numpy as np

# ---------- Streamlit Page Setup ----------
st.set_page_config(page_title="QR Code Generator & Scanner", page_icon="🔳")

st.title("🔳 QR Code Generator & Scanner Mini Project")
st.write("Generate QR Codes and Scan QR Codes easily using Python + Streamlit")

# ---------- Tabs ----------
tab1, tab2 = st.tabs(["📌 QR Code Generator", "📷 QR Code Scanner"])

# ======================================================
#                 QR CODE GENERATOR
# ======================================================
with tab1:
    st.header("📌 Generate QR Code")

    text = st.text_input("Enter Text / URL to Generate QR Code")

    if st.button("Generate QR Code"):
        if text.strip() != "":
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4,
            )
            qr.add_data(text)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")

            st.success("✅ QR Code Generated Successfully!")
            st.image(img)

            # Save QR Code
            img.save("generated_qr.png")
            st.download_button(
                label="⬇ Download QR Code",
                data=open("generated_qr.png", "rb"),
                file_name="qr_code.png",
                mime="image/png"
            )
        else:
            st.warning("⚠ Please enter some text or URL!")

# ======================================================
#                 QR CODE SCANNER
# ======================================================
with tab2:
    st.header("📷 Scan QR Code from Image")

    uploaded_file = st.file_uploader("Upload QR Code Image", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded QR Image")

        # Convert PIL Image to OpenCV format
        img_array = np.array(image)
        img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

        detector = cv2.QRCodeDetector()
        data, bbox, _ = detector.detectAndDecode(img_cv)

        if data:
            st.success("✅ QR Code Scanned Successfully!")
            st.write("📌 Decoded Text / URL:")
            st.code(data)
        else:
            st.error("❌ No QR Code Found in the Image!")
