import streamlit as st
import requests
import uuid

# ================== CONFIG ==================

BASE_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Streaming Chatbot",
    layout="wide"
)

st.title("💬 Streaming Chatbot")

# ================== HELPERS ==================

def new_thread_id():
    return f"thread-{uuid.uuid4().hex[:8]}"

def get_threads():
    r = requests.get(f"{BASE_URL}/chat/threads")
    r.raise_for_status()
    return r.json()

def get_history(thread_id):
    r = requests.get(f"{BASE_URL}/chat/history/{thread_id}")
    r.raise_for_status()
    return r.json()["messages"]

# ================== SESSION STATE ==================

if "current_thread" not in st.session_state:
    st.session_state.current_thread = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# ================== SIDEBAR ==================

st.sidebar.title("🧵 Threads")

threads = get_threads()

if not threads:
    st.sidebar.info("No threads yet")

else:
    for tid in threads:
        label = f"👉 {tid}" if tid == st.session_state.current_thread else tid
        if st.sidebar.button(label, key=tid):
            st.session_state.current_thread = tid
            st.session_state.messages = get_history(tid)
            st.rerun()

st.sidebar.divider()

if st.sidebar.button("➕ New Thread"):
    tid = new_thread_id()
    st.session_state.current_thread = tid
    st.session_state.messages = []
    st.rerun()

# ================== MAIN CHAT ==================

if not st.session_state.current_thread:
    st.info("Select or create a thread")
    st.stop()

st.subheader(f"🧠 {st.session_state.current_thread}")

# Render chat history
for msg in st.session_state.messages:
    role = msg.get("type")

    if role == "human":
        with st.chat_message("user"):
            st.markdown(msg["content"])

    elif role == "ai":
        with st.chat_message("assistant"):
            st.markdown(msg["content"])

# ================== CHAT INPUT ==================

user_input = st.chat_input("Type your message")

if user_input:
    # ---- User message (optimistic render)
    st.session_state.messages.append({
        "type": "human",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # ---- Assistant streaming
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        with requests.get(
            f"{BASE_URL}/chat/stream/{st.session_state.current_thread}",
            params={"message": user_input},
            stream=True,
            timeout=None
        ) as r:
            for chunk in r.iter_content(chunk_size=None):
                if not chunk:
                    continue
                token = chunk.decode("utf-8")
                full_response += token
                placeholder.markdown(full_response)

    # ---- Persist assistant message
    st.session_state.messages.append({
        "type": "ai",
        "content": full_response
    })

    st.rerun()
