import streamlit as st
import re
import random
import string
import matplotlib.pyplot as plt
from io import BytesIO

def check_password_strength(password):
    score = 0
    feedback = []
    
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Increase password length to at least 8 characters.")
    
    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Add lowercase letters for better security.")
    
    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Include uppercase letters to enhance strength.")
    
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("Use at least one digit (0-9).")
    
    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        feedback.append("Include a special character (!@#$%^&*).")
    
    return score, feedback

def generate_strong_password():
    words = ["Blue", "Eagle", "Sky", "River", "Lion", "Moon", "Star", "Thunder", "Ocean"]
    special_chars = "!@#$%^&*"
    random_password = f"{random.choice(words)}-{random.choice(words)}{random.randint(10,99)}{random.choice(special_chars)}"
    
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    alternative_password = ''.join(random.choice(characters) for _ in range(12))
    
    return random_password, alternative_password

def plot_gauge_meter(score):
    fig, ax = plt.subplots()
    colors = ["red", "orange", "yellow", "lightgreen", "green"]
    ax.barh(0, score, color=colors[score-1], height=0.5)
    ax.set_xlim(0, 5)
    ax.set_yticks([])
    ax.set_xticks(range(6))
    ax.set_title("Password Strength Meter")
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    return buf

# Streamlit UI
st.set_page_config(page_title="🔒 Password Strength Meter", layout="centered")

dark_mode = st.checkbox("🌙 Dark Mode")
if dark_mode:
    st.markdown("<style>body { background-color: #222; color: white; }</style>", unsafe_allow_html=True)

st.title("🔒 Password Strength Meter")
password = st.text_input("Enter your password:", type="password")

if password:
    score, feedback = check_password_strength(password)
    img_buf = plot_gauge_meter(score)
    st.image(img_buf, caption="Password Strength", use_column_width=True)
    
    if score <= 2:
        st.error("Weak Password 🚨")
    elif score <= 4:
        st.warning("Moderate Password ⚠️")
    else:
        st.success("Strong Password ✅")
    
    if feedback:
        st.write("**Suggestions to improve:**")
        for tip in feedback:
            st.write(f"- {tip}")

if st.button("Generate Strong Password"):
    strong_password, alternative_password = generate_strong_password()
    st.write(f"**Memorable Password:** `{strong_password}`")
    st.write(f"**Random Secure Password:** `{alternative_password}`")
