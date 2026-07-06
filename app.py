import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load file .env
load_dotenv()

# Konfigurasi Page & Tema
st.set_page_config(
    page_title="PRAYCHATBOT",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- INJEKSI KUSTOM CSS (PREMIUM GLASS-MORPHISM UI) ---
st.markdown("""
<style>
/* Background keseluruhan web */
.stApp {
    background-color: #0F172A; /* Slate 900 */
    background-image: radial-gradient(circle at 10% 20%, rgba(59, 130, 246, 0.1) 0%, transparent 20%),
                      radial-gradient(circle at 90% 80%, rgba(139, 92, 246, 0.15) 0%, transparent 20%);
    background-attachment: fixed;
    color: #F8FAFC;
}

/* Sidebar Glass-morphism */
[data-testid="stSidebar"] {
    background-color: rgba(15, 23, 42, 0.85) !important;
    backdrop-filter: blur(15px);
    -webkit-backdrop-filter: blur(15px);
    border-right: 1px solid rgba(255, 255, 255, 0.05);
}

/* Menyembunyikan elemen bawaan Streamlit (Header, Footer, Menu) */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Custom Text Gradient untuk Title */
.title-gradient {
    background: linear-gradient(90deg, #3B82F6 0%, #8B5CF6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 3rem;
    font-weight: 800;
    text-align: center;
    margin-bottom: 0.5rem;
}
.subtitle {
    text-align: center;
    color: #94A3B8;
    font-size: 1.1rem;
    margin-bottom: 2rem;
}

/* Chat Container Glass-morphism */
.stChatMessage {
    background: rgba(30, 41, 59, 0.6) !important;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px !important;
    padding: 1.2rem;
    margin-bottom: 1rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

/* Warna pesan user */
.stChatMessage[data-testid="chatAvatarIcon-user"] {
    background: rgba(59, 130, 246, 0.15) !important;
    border: 1px solid rgba(59, 130, 246, 0.2);
}

/* Gaya input chat */
.stChatInputContainer {
    background: rgba(15, 23, 42, 0.8) !important;
    backdrop-filter: blur(16px);
    border-top: 1px solid rgba(255, 255, 255, 0.05);
    padding-bottom: 2rem !important;
}

div[data-testid="stChatInput"] {
    background: rgba(30, 41, 59, 0.8) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 24px !important;
    color: white !important;
}
div[data-testid="stChatInput"]:focus-within {
    border: 1px solid #3B82F6 !important;
    box-shadow: 0 0 0 1px #3B82F6 !important;
}

/* Avatar Kustom */
.stChatMessage div[data-testid="chatAvatarIcon-assistant"] {
    background-color: #8B5CF6;
}
.stChatMessage div[data-testid="chatAvatarIcon-user"] {
    background-color: #3B82F6;
}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR MENU ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #F8FAFC;'>⚙️ Pengaturan LLM</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    selected_model = st.selectbox(
        "Pilih Model AI (Google Gemini):",
        [
            "gemini-1.5-pro-latest", 
            "gemini-1.5-flash-latest", 
            "gemini-1.5-flash-8b-latest",
            "gemini-1.0-pro-latest"
        ],
        index=0,
        help="Model menentukan kecerdasan dan batasan limit akun Anda."
    )
    
    st.markdown("""
    <div style="font-size: 0.82em; color: #94A3B8; margin-bottom: 20px; background: rgba(0,0,0,0.2); padding: 10px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.05);">
    <b>📊 Rate Limits (Free Tier AI Studio):</b><br><br>
    
    <span style="color: #F87171;"><b>1.5 Pro</b> (Paling Pintar)</span><br>
    • Limit Harian: <b>50 request / hari</b><br>
    • Limit Menit: 2 request / menit<br>
    • Token: 32K token / menit<br>
    <i>*Sangat ketat, gunakan hanya untuk tugas kompleks/coding.</i><br><br>
    
    <span style="color: #34D399;"><b>1.5 Flash</b> (Paling Seimbang)</span><br>
    • Limit Harian: <b>1.500 request / hari</b><br>
    • Limit Menit: 15 request / menit<br>
    • Token: 1 Juta token / menit<br>
    <i>*Limit lega, ngebut, performa mantap.</i><br><br>
    
    <span style="color: #60A5FA;"><b>1.5 Flash-8B</b> (Paling Ringan)</span><br>
    • Limit Harian: <b>1.500 request / hari</b><br>
    • Limit Menit: 15 request / menit<br>
    • Token: 1 Juta token / menit<br>
    <i>*Super kencang untuk chat harian biasa.</i>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    if st.button("🗑️ Bersihkan Obrolan", use_container_width=True):
        st.session_state.messages = [
            {"role": "model", "content": "Halo Bos! PRAYCHATBOT siap bantu nih. Ada yang mau diobrolin?"}
        ]
        st.rerun()

# UI Header
st.markdown("<h1 class='title-gradient'>✨ PRAYCHATBOT</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='subtitle'>Powered by <b>{selected_model}</b></p>", unsafe_allow_html=True)

# --- SETUP API GEMINI ---
api_key = os.getenv("GOOGLE_GENERATIVE_AI_API_KEY")

if not api_key:
    st.error("API Key Gemini belum diatur. Silakan tambahkan rahasia 'GOOGLE_GENERATIVE_AI_API_KEY' ke dalam menu Secrets di Streamlit!")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel(
    selected_model,
    system_instruction="Kamu adalah asisten AI PRAYCHATBOT, yang cerdas, ahli di bidang IT & Web3, dan menggunakan bahasa gaul yang santai. Kamu memanggil user dengan sebutan 'Bos'."
)

# Inisialisasi History Chat (session state)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "model", "content": "Halo Bos! PRAYCHATBOT siap bantu nih. Ada yang mau diobrolin?"}
    ]

# Tampilkan history chat (Render)
for msg in st.session_state.messages:
    # Streamlit mapping: model -> assistant, user -> user
    role = "assistant" if msg["role"] == "model" else "user"
    with st.chat_message(role):
        st.markdown(msg["content"])

# Input Chat User
if prompt := st.chat_input("Ketik pesan buat PRAYCHATBOT..."):
    # Render pesan user ke UI
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Tambah ke session state
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Siapkan data format Gemini API (kirim seluruh history agar nyambung konteksnya)
    history_for_gemini = []
    for msg in st.session_state.messages:
        role = "model" if msg["role"] == "model" else "user"
        history_for_gemini.append({
            "role": role,
            "parts": [msg["content"]]
        })
    
    # Ambil respons AI (Streaming effect)
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        
        try:
            chat = model.start_chat(history=history_for_gemini[:-1])
            response = chat.send_message(prompt, stream=True)
            
            full_response = ""
            for chunk in response:
                if chunk.text:
                    full_response += chunk.text
                    response_placeholder.markdown(full_response + "▌")
            
            # Selesai stream, buang cursor block
            response_placeholder.markdown(full_response)
            
            # Tambahkan respons AI ke session state
            st.session_state.messages.append({"role": "model", "content": full_response})
            
        except Exception as e:
            st.error(f"Waduh Bos, ada error dari Gemini: {str(e)}")
