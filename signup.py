import streamlit as st
import sqlite3
import hashlib
import time

# Database Connection
conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()

# Create Users Table (if not exists)
c.execute('''CREATE TABLE IF NOT EXISTS users (email TEXT, password TEXT)''')
conn.commit()

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Streamlit UI
st.title("🔐 Track Your Care Cost - Login & Signup")

# Sidebar for Navigation
choice = st.sidebar.selectbox("Login/Signup", ["Login", "Sign Up"])

if choice == "Sign Up":
    st.subheader("Create an Account")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Sign Up"):
        hashed_password = hash_password(password)
        c.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, hashed_password))
        conn.commit()
        st.success("✅ Account created successfully!")

elif choice == "Login":
    st.subheader("Login to Your Account")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        hashed_password = hash_password(password)
        c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, hashed_password))
        result = c.fetchone()

        if result:
            st.session_state['user'] = email  # Store user session
            st.session_state['logged_in'] = True
            st.success("🎉 Logged in successfully! Redirecting...")
            time.sleep(2)  # Small delay for UX
            st.switch_page("pages/app.py")
           
        else:
            st.error("⚠️ Invalid email or password.")
