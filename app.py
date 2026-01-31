import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import io
import random
import string
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

st.set_page_config(page_title="GEG Cert Gen", page_icon="🏆", layout="centered")

st.markdown("""
<style>
.main { background-color: #f8fafc; }
.stButton>button {
    width: 100%; background-color: #4F46E5; color: white;
    font-weight: bold; padding: 0.75rem; border-radius: 1rem;
}
.header-box {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem; border-radius: 1rem; text-align: center;
    margin-bottom: 2rem; color: white;
}
.success-box {
    background-color: #d1fae5; border: 2px solid #6ee7b7;
    padding: 1rem; border-radius: 0.5rem; margin: 1rem 0;
}
.warning-box {
    background-color: #fef3c7; border: 2px solid #fbbf24;
    padding: 1rem; border-radius: 0.5rem; margin: 1rem 0;
}

/* ===== HIDE ALL STREAMLIT & GITHUB BRANDING ===== */
header[data-testid="stHeader"] {
    display: none !important;
    visibility: hidden !important;
}
.stDeployButton {
    display: none !important;
    visibility: hidden !important;
}
#MainMenu {
    display: none !important;
    visibility: hidden !important;
}
footer {
    display: none !important;
    visibility: hidden !important;
}
footer:after {
    content: none !important;
    display: none !important;
}
.viewerBadge_container__1QSob {
    display: none !important;
    visibility: hidden !important;
}
.viewerBadge_container__r5tak {
    display: none !important;
    visibility: hidden !important;
}
[data-testid="stStatusWidget"] {
    display: none !important;
    visibility: hidden !important;
}
iframe[title="GitHub"] {
    display: none !important;
    visibility: hidden !important;
}
.stToolbar {
    display: none !important;
    visibility: hidden !important;
}
.styles_viewerBadge__1yB5_ {
    display: none !important;
    visibility: hidden !important;
}
.github-corner {
    display: none !important;
    visibility: hidden !important;
}
[data-testid="stToolbar"] {
    display: none !important;
    visibility: hidden !important;
}
button[kind="header"] {
    display: none !important;
    visibility: hidden !important;
}
header {
    display: none !important;
    visibility: hidden !important;
}
.stApp header {
    display: none !important;
    visibility: hidden !important;
}
.stApp {
    padding-top: 0 !important;
}
.main .block-container {
    padding-top: 2rem !important;
}

/* ===== HIDE FLOATING BUTTONS ===== */
.stChatFloatingInputContainer {
    display: none !important;
    visibility: hidden !important;
}
[data-testid="stChatFloatingActionButton"] {
    display: none !important;
    visibility: hidden !important;
}
.floating-button {
    display: none !important;
    visibility: hidden !important;
}
.support-widget {
    display: none !important;
    visibility: hidden !important;
}
[data-testid="stChatMessageFeedback"] {
    display: none !important;
    visibility: hidden !important;
}
button[style*="position: fixed"][style*="bottom"][style*="right"] {
    display: none !important;
    visibility: hidden !important;
}
.stBottomBlockContainer {
    display: none !important;
    visibility: hidden !important;
}
div[style*="position: fixed"][style*="bottom: 0"][style*="right: 0"],
div[style*="position: fixed"][style*="bottom: 1rem"][style*="right: 1rem"],
div[style*="position: fixed"][style*="bottom: 20px"][style*="right: 20px"] {
    display: none !important;
    visibility: hidden !important;
}
iframe {
    display: none !important;
    visibility: hidden !important;
}
</style>
""", unsafe_allow_html=True)

# ===== JAVASCRIPT TO AGGRESSIVELY HIDE FLOATING ELEMENTS =====
st.markdown("""
<script>
// Wait for page load
window.addEventListener('load', function() {
    // Remove all fixed position elements in bottom-right
    setTimeout(function() {
        const elements = document.querySelectorAll('*');
        elements.forEach(el => {
            const style = window.getComputedStyle(el);
            if (style.position === 'fixed') {
                const bottom = parseInt(style.bottom);
                const right = parseInt(style.right);
                // If element is in bottom-right corner (within 100px)
                if (bottom >= 0 && bottom < 100 && right >= 0 && right < 100) {
                    el.style.display = 'none !important';
                    el.style.visibility = 'hidden !important';
                    el.remove();
                }
            }
        });
    }, 1000);
    
    // Keep monitoring and removing (continuous check)
    setInterval(function() {
        const elements = document.querySelectorAll('*');
        elements.forEach(el => {
            const style = window.getComputedStyle(el);
            if (style.position === 'fixed') {
                const bottom = parseInt(style.bottom);
                const right = parseInt(style.right);
                if (bottom >= 0 && bottom < 100 && right >= 0 && right < 100) {
                    el.remove();
                }
            }
        });
    }, 2000); // Check every 2 seconds
});
</script>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-box">
    <h1>🏆 GEG Sabah Cert Generator</h1>
    <p style="font-size: 0.8rem;">GEG Sabah x GEG Kelantan Collaboration</p>
</div>
""", unsafe_allow_html=True)

# ===== EMAIL CONFIGURATION - SECURE =====
try:
    EMAIL_SENDER = st.secrets["EMAIL_SENDER"]
    EMAIL_PASSWORD = st.secrets["EMAIL_PASSWORD"]
except:
    EMAIL_SENDER = "jebatlegacy@gegkotakinabalu.edu.my"
    EMAIL_PASSWORD = "xeit neeg ounj jnwv"
# ========================================

def generate_cert_id():
    prefix = "GEG"
    year = datetime.now().year
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"{prefix}-{year}-{random_str}"

def create_certificate_image(name, location, cert_id):
    """Create certificate image with overlay text"""
    template_paths = ["certificate_template.png", "template.jpg", "Sijil_Jebat__GEG.jpg"]
    template = None
    
    for template_path in template_paths:
        if os.path.exists(template_path):
            try:
                template = Image.open(template_path)
                if template.mode != 'RGB':
                    template = template.convert('RGB')
                break
            except Exception as e:
                continue
    
    if template is None:
        st.error("❌ Template tidak dijumpai!")
        return None
    
    width, height = template.size
    draw = ImageDraw.Draw(template)
    
    # ===== FONT LOADING =====
    try:
        name_font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 100)
        location_font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 120)
        id_font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 85)
    except:
        try:
            name_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 100)
            location_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 120)
            id_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 85)
        except Exception as e:
            name_font = ImageFont.load_default()
            location_font = ImageFont.load_default()
            id_font = ImageFont.load_default()
    
    text_color = "#000000"
    
    # Overlay NAME
    name_y = int(height * 0.37)
    bbox = draw.textbbox((0, 0), name, font=name_font)
    name_width = bbox[2] - bbox[0]
    name_x = (width - name_width) // 2
    draw.text((name_x, name_y), name, fill=text_color, font=name_font)
    
    # Overlay LOCATION
    location_y = int(height * 0.50)
    bbox = draw.textbbox((0, 0), location, font=location_font)
    location_width = bbox[2] - bbox[0]
    location_x = (width - location_width) // 2
    draw.text((location_x, location_y), location, fill=text_color, font=location_font)
    
    # Certificate ID
    id_text = f"ID: {cert_id}"
    draw.text((width - 280, height - 50), id_text, fill='#9CA3AF', font=id_font)
    
    return template

def image_to_pdf(image):
    """Convert image to PDF"""
    pdf_buffer = io.BytesIO()
    if image.mode != 'RGB':
        image = image.convert('RGB')
    image.save(pdf_buffer, format='PDF', quality=95)
    pdf_buffer.seek(0)
    return pdf_buffer

def send_certificate_email(recipient_email, recipient_name, cert_id, pdf_data):
    """Send certificate via email"""
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SENDER
        msg['To'] = recipient_email
        msg['Subject'] = f"Sijil GEG Sabah x Kelantan - {recipient_name}"
        
        body = f"""
Assalamualaikum & Salam Sejahtera,

Tahniah {recipient_name}! 🎉

Sijil penyertaan anda untuk program GEG Sabah x GEG Kelantan telah berjaya dijana.

📄 Certificate ID: {cert_id}
📅 Tarikh: {datetime.now().strftime("%d %B %Y")}

Sijil digital anda dilampirkan dalam format PDF. Sila muat turun dan simpan untuk rekod anda.

Terima kasih atas penyertaan anda!

Salam hormat,
Google Educator Group Sabah & Kelantan

---
🌐 www.jebatlegacy.vip
📧 Email ini dijana secara automatik. Sila jangan balas.
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(pdf_data.read())
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename=Sijil_{recipient_name.replace(" ", "_")}_GEG.pdf'
        )
        msg.attach(part)
        
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
        
        return True
    except Exception as e:
        st.error(f"❌ Gagal menghantar email. Sila cuba lagi.")
        return False

# Session state
if 'cert_generated' not in st.session_state:
    st.session_state.cert_generated = False

# Check template silently
template_found = False
for tpath in ["certificate_template.png", "template.jpg", "Sijil_Jebat__GEG.jpg"]:
    if os.path.exists(tpath):
        template_found = True
        break

if not template_found:
    st.error("❌ Template tidak dijumpai! Sila hubungi admin.")
    st.stop()

# Form
st.markdown("### 📝 Pendaftaran Sijil")
st.write("Sijil akan dihantar ke email anda secara automatik")

name = st.text_input("👤 Nama Penuh Peserta *", placeholder="Contoh: Muhammad Ali bin Ahmad")
location = st.text_input("📍 Institusi / Lokasi *", placeholder="Contoh: SK Keningau, Sabah")
email = st.text_input("📧 Alamat E-mel *", placeholder="contoh@email.com")

col1, col2 = st.columns([3, 1])

with col1:
    if st.button("🚀 Jana & Hantar Sijil"):
        if name and location and email:
            with st.spinner("⏳ Sedang menjana & menghantar sijil..."):
                cert_id = generate_cert_id()
                cert_image = create_certificate_image(name, location, cert_id)
                
                if cert_image:
                    pdf_buffer = image_to_pdf(cert_image)
                    pdf_buffer.seek(0)
                    email_sent = send_certificate_email(email, name, cert_id, pdf_buffer)
                    
                    if email_sent:
                        st.session_state.cert_generated = True
                        st.session_state.cert_image = cert_image
                        st.session_state.name = name
                        st.session_state.cert_id = cert_id
                        st.session_state.email = email
                        st.session_state.email_sent = True
                        st.rerun()
        else:
            st.error("❌ Sila isi semua medan!")

with col2:
    if st.button("🔄 Reset"):
        st.session_state.cert_generated = False
        st.rerun()

# Display certificate
if st.session_state.cert_generated:
    st.markdown("""
    <div class="success-box">
        <h4 style="color: #065f46; margin: 0;">✅ Sijil Berjaya Dijana & Dihantar!</h4>
        <p style="color: #047857; margin: 0.5rem 0 0 0; font-size: 0.9rem;">
            Sijil telah dihantar ke email. Sila check inbox/spam folder.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.image(st.session_state.cert_image, use_container_width=True)
    
    pdf_buffer = image_to_pdf(st.session_state.cert_image)
    png_buffer = io.BytesIO()
    st.session_state.cert_image.save(png_buffer, format='PNG', quality=95)
    png_buffer.seek(0)
    
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="📄 Muat Turun PDF",
            data=pdf_buffer,
            file_name=f"Sijil_{st.session_state.name.replace(' ', '_')}_GEG.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    with col2:
        st.download_button(
            label="🖼️ Muat Turun PNG",
            data=png_buffer,
            file_name=f"Sijil_{st.session_state.name.replace(' ', '_')}_GEG.png",
            mime="image/png",
            use_container_width=True
        )
    
    st.info(f"📧 **Email:** {st.session_state.email}\n\n🆔 **Certificate ID:** `{st.session_state.cert_id}`")

st.markdown("---")
st.markdown("""
<p style="text-align: center; color: #9CA3AF; font-size: 0.8rem;">
    Official Google Educator Groups Digital Achievement • 2026<br>
    <span style="color: #10B981;">●</span> Verified Document
</p>
""", unsafe_allow_html=True)
