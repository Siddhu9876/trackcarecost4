import streamlit as st
from user_activity import log_user_activity

st.title("📂 Upload Your Profile File")

if "user" not in st.session_state:
    st.warning("⚠️ Please log in to upload files.")
    st.stop()

uploaded_file = st.file_uploader("Choose a file", type=["csv", "png", "jpg", "pdf"])

if uploaded_file is not None:
    # Save file locally
    with open(f"uploads/{uploaded_file.name}", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.success(f"✅ Uploaded `{uploaded_file.name}` successfully!")
    
    # Log activity
    log_user_activity(st.session_state['user'], uploaded_file.name, "File Uploaded")
