import streamlit as st
import requests
import pages.home as home  
import pages.form as form  
import pages.about as about  

# Set Page Title and Layout
st.set_page_config(page_title="Track Your Care Cost", layout="wide")

# Ensure the user is logged in before accessing the home page
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.warning("⚠️ Please log in to access this page.")
    st.stop()  # Stop execution if not logged in

# Welcome message for logged-in users
st.write(f"👋 Welcome back, **{st.session_state['user']}**!")



# Initialize session state for page navigation
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'home'

# Sidebar Navigation
st.sidebar.title("🔍 Navigation")
st.sidebar.write(f"**Current Page:** `{st.session_state['current_page']}`")

# Sidebar buttons for navigation
if st.sidebar.button("🏠 Home"):
    st.session_state['current_page'] = 'home'
    st.rerun()

if st.sidebar.button("📝 Fill Form"):
    st.session_state['current_page'] = 'form'
    st.rerun()

if st.sidebar.button("ℹ️ About"):
    st.session_state['current_page'] = 'about'
    st.rerun()

# Logout button in the sidebar
if st.sidebar.button("🚪 Logout"):
    st.session_state.clear()  # Clear session state
    st.success("✅ Logged out successfully!")
    st.rerun()

# Display the selected page based on session state
if st.session_state['current_page'] == 'home':
    st.markdown('<h1 class="title">Welcome to Track  Care Cost</h1>', unsafe_allow_html=True)
    st.write("📊 Easily track and predict your healthcare expenses with our AI-powered system.")
    st.image("trackcarecost.logo1.png", width=250)
    home.show()

    # View Activity Section
    st.subheader("📜 User Activity Log")
    if st.button("🔍 View My Activity"):
        response = requests.get(f"http://localhost:8503/activity?user_id={st.session_state['user']}")
        
        print("response status code:", response.status_code)
        print("response text:", response.text)

        if response.status_code == 200 and response.text.strip():
            activity_data = response.json()
        else:
            activity_data = {"error": "no valid json response form server"}
            

elif st.session_state['current_page'] == 'form':
    form.show()
elif st.session_state['current_page'] == 'about':
    about.show()
elif st.session_state['current_page'] == 'form':
    form.show()
elif st.session_state['current_page'] == 'about':
    about.show()
