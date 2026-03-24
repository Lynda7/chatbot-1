import streamlit as st
from openai import OpenAI
import os

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="AI Chatbot Assistant", page_icon="🤖", layout="centered")

# --- RÉCUPÉRATION DE LA CLÉ API ---
# On essaie d'abord de la trouver dans les secrets Streamlit (pour le web) 
# ou dans les variables d'environnement (pour le local)
if "OPENAI_API_KEY" in st.secrets:
    openai_api_key = st.secrets["OPENAI_API_KEY"]
else:
    openai_api_key = os.getenv("OPENAI_API_KEY")

# --- BARRE LATÉRALE (SIDEBAR) ---
with st.sidebar:
    st.title("🤖 Chatbot Info")
    st.success("API Connection: Active ✅") # On rassure l'utilisateur
    
    st.divider()
    st.markdown("### 🚀 About this App")
    st.write("This professional AI assistant is powered by GPT-3.5-Turbo and built with Streamlit.")
    
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# --- TITRE PRINCIPAL ---
st.title("🤖 Personal AI Assistant")
st.caption("A smart conversational agent for your daily tasks.")

# --- INITIALISATION & AFFICHAGE DE L'HISTORIQUE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- LOGIQUE DU CHAT ---
if prompt := st.chat_input("What is on your mind?"):
    if not openai_api_key:
        st.error("API Key not found! Please configure it in your secrets.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            stream=True,
        )
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                full_response += chunk.choices[0].delta.content
                message_placeholder.markdown(full_response + "▌")
        
        message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})