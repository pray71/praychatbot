import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load file .env
load_dotenv()

# Konfigurasi Page & Tema
st.set_page_config(
    page_title="PRAYCHATBOT",
    page_icon="👑",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- INJEKSI KUSTOM CSS & FONTAWESOME (PREMIUM UI) ---
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
/* Background keseluruhan web */
.stApp {
    background-color: #0B1121; /* Slate 950 */
    background-image: radial-gradient(circle at 10% 20%, rgba(59, 130, 246, 0.1) 0%, transparent 20%),
                      radial-gradient(circle at 90% 80%, rgba(139, 92, 246, 0.15) 0%, transparent 20%);
    background-attachment: fixed;
    color: #F8FAFC;
}

/* Sidebar Glass-morphism */
[data-testid="stSidebar"] {
    background-color: rgba(15, 23, 42, 0.75) !important;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-right: 1px solid rgba(255, 255, 255, 0.05);
}

/* Menyembunyikan elemen bawaan Streamlit */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Custom Text Gradient untuk Title */
.title-gradient {
    background: linear-gradient(90deg, #3B82F6 0%, #8B5CF6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2.8rem;
    font-weight: 900;
    text-align: center;
    margin-bottom: 0.2rem;
    letter-spacing: -1px;
}
.subtitle {
    text-align: center;
    color: #94A3B8;
    font-size: 1rem;
    margin-bottom: 2.5rem;
    font-weight: 500;
}

/* Chat Container Glass-morphism */
.stChatMessage {
    background: rgba(30, 41, 59, 0.4) !important;
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 20px !important;
    padding: 1.5rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
}
.stChatMessage:hover {
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 10px 25px -3px rgba(59, 130, 246, 0.1);
}

/* Warna pesan user */
.stChatMessage:nth-child(even) {
    background: rgba(59, 130, 246, 0.1) !important;
    border: 1px solid rgba(59, 130, 246, 0.2);
}

/* Gaya input chat */
.stChatInputContainer {
    background: rgba(11, 17, 33, 0.9) !important;
    backdrop-filter: blur(20px);
    border-top: 1px solid rgba(255, 255, 255, 0.05);
    padding-bottom: 2rem !important;
}

div[data-testid="stChatInput"] {
    background: rgba(30, 41, 59, 0.6) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 30px !important;
    color: white !important;
    box-shadow: inset 0 2px 4px 0 rgba(0, 0, 0, 0.1);
}
div[data-testid="stChatInput"]:focus-within {
    border: 1px solid #8B5CF6 !important;
    box-shadow: 0 0 15px rgba(139, 92, 246, 0.3), inset 0 2px 4px 0 rgba(0, 0, 0, 0.1) !important;
}

/* Rate Limit Card Style */
.rate-limit-card {
    background: rgba(0,0,0,0.25);
    padding: 15px;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.05);
    font-size: 0.85em;
    color: #CBD5E1;
    margin-bottom: 20px;
    transition: all 0.3s ease;
}
.rate-limit-card:hover {
    border-color: rgba(59, 130, 246, 0.4);
    box-shadow: 0 0 15px rgba(59, 130, 246, 0.1);
}
.badge {
    padding: 3px 8px;
    border-radius: 6px;
    font-size: 0.75em;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR MENU ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #F8FAFC;'><i class='fa-solid fa-microchip' style='color:#3B82F6;'></i> Engine Settings</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    selected_model = st.selectbox(
        "🧠 Pilih Model AI:",
        [
            "gemini-1.5-pro-latest", 
            "gemini-1.5-flash-latest", 
            "gemini-1.5-flash-8b-latest",
            "gemini-1.0-pro-latest"
        ],
        index=0,
    )
    
    st.markdown("""
    <div class="rate-limit-card">
    <div style="text-align: center; margin-bottom: 10px; color:#8B5CF6;"><i class="fa-solid fa-chart-pie"></i> <b>Rate Limits (Free Tier)</b></div>
    
    <div style="margin-bottom: 12px;">
    <span class="badge" style="background: rgba(248, 113, 113, 0.2); color: #F87171;"><i class="fa-solid fa-brain"></i> 1.5 Pro</span><br>
    <i class="fa-solid fa-battery-quarter" style="color:#64748B; width:15px;"></i> <b>50</b> req/hari<br>
    <i class="fa-solid fa-stopwatch" style="color:#64748B; width:15px;"></i> 2 req/menit<br>
    </div>
    
    <div style="margin-bottom: 12px;">
    <span class="badge" style="background: rgba(52, 211, 153, 0.2); color: #34D399;"><i class="fa-solid fa-bolt"></i> 1.5 Flash</span><br>
    <i class="fa-solid fa-battery-full" style="color:#64748B; width:15px;"></i> <b>1.500</b> req/hari<br>
    <i class="fa-solid fa-stopwatch" style="color:#64748B; width:15px;"></i> 15 req/menit<br>
    </div>
    
    <div>
    <span class="badge" style="background: rgba(96, 165, 250, 0.2); color: #60A5FA;"><i class="fa-solid fa-feather"></i> 1.5 Flash-8B</span><br>
    <i class="fa-solid fa-battery-full" style="color:#64748B; width:15px;"></i> <b>1.500</b> req/hari<br>
    </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    if st.button("🗑️ Bersihkan Obrolan", use_container_width=True):
        st.session_state.messages = [] # Kosongkan state untuk diisi ulang di bawah
        st.rerun()

# UI Header
st.markdown("<h1 class='title-gradient'><i class='fa-solid fa-crown' style='color:#FBBF24; font-size:2.4rem;'></i> PRAYCHATBOT</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='subtitle'><i class='fa-solid fa-link' style='color:#8B5CF6;'></i> Connected to <b>{selected_model}</b></p>", unsafe_allow_html=True)

# --- SETUP API GEMINI ---
api_key = os.getenv("GOOGLE_GENERATIVE_AI_API_KEY")

if not api_key:
    st.warning("⚠️ **API Key Gemini belum diatur.**\n\nSilakan tambahkan `GOOGLE_GENERATIVE_AI_API_KEY` di menu **Secrets** Streamlit Cloud untuk mulai chatting.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel(
    selected_model,
    system_instruction="Kamu adalah asisten AI PRAYCHATBOT, yang cerdas, ahli di bidang IT & Web3, dan menggunakan bahasa gaul yang santai. Kamu memanggil user dengan sebutan 'Bos'."
)

# Pesan Welcome Screen (Jika history kosong)
welcome_msg = """
### <i class="fa-solid fa-hand-sparkles" style="color:#FBBF24;"></i> Halo Bos!

Saya **PRAYCHATBOT**, AI Assistant premium yang siap bantu Bos hari ini.

<div style="display:flex; gap: 20px; margin-top: 15px;">
    <div style="background: rgba(59,130,246,0.1); padding: 15px; border-radius: 10px; border: 1px solid rgba(59,130,246,0.2); flex: 1;">
        <h4 style="margin-top:0; color:#60A5FA;"><i class="fa-solid fa-code"></i> Coding</h4>
        <span style="font-size:0.9em; color:#CBD5E1;">Fix bug, bikin web, review code Python/Next.js.</span>
    </div>
    <div style="background: rgba(139,92,246,0.1); padding: 15px; border-radius: 10px; border: 1px solid rgba(139,92,246,0.2); flex: 1;">
        <h4 style="margin-top:0; color:#A78BFA;"><i class="fa-brands fa-ethereum"></i> Web3</h4>
        <span style="font-size:0.9em; color:#CBD5E1;">Riset airdrop, bedah smart contract, crypto alpha.</span>
    </div>
</div>

<br>Ketik pertanyaan atau perintah Bos di bawah ya! 👇
"""

# Inisialisasi History Chat (session state)
if "messages" not in st.session_state or len(st.session_state.messages) == 0:
    st.session_state.messages = [
        {"role": "model", "content": welcome_msg}
    ]

# Tampilkan history chat
for msg in st.session_state.messages:
    # Set Custom Avatar (Mahkota buat AI, Kacamata Hitam buat User)
    role = "assistant" if msg["role"] == "model" else "user"
    avatar = "👑" if role == "assistant" else "😎"
    
    with st.chat_message(role, avatar=avatar):
        st.markdown(msg["content"], unsafe_allow_html=True)

# Input Chat User
if prompt := st.chat_input("Ketik pesan buat PRAYCHATBOT..."):
    # Render pesan user
    with st.chat_message("user", avatar="😎"):
        st.markdown(prompt, unsafe_allow_html=True)
    
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Siapkan history untuk API
    history_for_gemini = []
    for msg in st.session_state.messages:
        # Filter HTML tag di history supaya Gemini tidak kebingungan sama FontAwesome
        clean_content = msg["content"]
        if "Halo Bos!" in clean_content and "<i class" in clean_content:
            clean_content = "Halo Bos! Saya PRAYCHATBOT, siap membantu."
            
        r = "model" if msg["role"] == "model" else "user"
        history_for_gemini.append({
            "role": r,
            "parts": [clean_content]
        })
    
    # Render pesan AI
    with st.chat_message("assistant", avatar="👑"):
        response_placeholder = st.empty()
        try:
            chat = model.start_chat(history=history_for_gemini[:-1])
            response = chat.send_message(prompt, stream=True)
            
            full_response = ""
            for chunk in response:
                if chunk.text:
                    full_response += chunk.text
                    response_placeholder.markdown(full_response + " ▌", unsafe_allow_html=True)
            
            response_placeholder.markdown(full_response, unsafe_allow_html=True)
            st.session_state.messages.append({"role": "model", "content": full_response})
            
        except Exception as e:
            st.error(f"<i class='fa-solid fa-triangle-exclamation'></i> Waduh Bos, ada error dari Gemini: {str(e)}", unsafe_allow_html=True)
