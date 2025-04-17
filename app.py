import streamlit as st
import re
import random
import string
from collections import defaultdict

st.markdown("""
<style>
/* Main styling */
.stApp {
    background-color: #f5f5f5;
}

/* Title styling */
h1 {
    color: #2c3e50 !important;
    text-align: center;
    margin-bottom: 1.5rem;
}

/* Input field styling */
.stTextInput>div>div>input {
    border-radius: 8px;
    padding: 10px;
    border: 2px solid #3498db;
}

/* Tab styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
}

.stTabs [data-baseweb="tab"] {
    background-color: #ecf0f1;
    border-radius: 8px 8px 0 0 !important;
    padding: 10px 20px;
    transition: all 0.3s ease;
}

.stTabs [aria-selected="true"] {
    background-color: #3498db !important;
    color: white !important;
}

/* Button styling */
.stButton>button {
    background-color: #3498db;
    color: white;
    border: none;
    padding: 0.5rem 1.5rem;
    border-radius: 8px;
    transition: all 0.3s ease;
}

.stButton>button:hover {
    background-color: #2980b9;
    transform: translateY(-2px);
}

/* Progress bar styling */
.stProgress>div>div>div {
    background-color: #2ecc71;
}

/* Feedback message styling */
.stAlert {
    border-radius: 8px;
    padding: 1rem;
}

/* Code block styling */
.stCodeBlock {
    border-radius: 8px;
    background-color: #f8f9fa;
    padding: 1rem;
    font-size: 1.2rem;
    text-align: center;
    margin: 1rem 0;
}
</style>
        """, unsafe_allow_html=True)

# Common weak passwords blacklist
WEAK_PASSWORDS = [
    "password", "123456", "12345678", "123456789", "qwerty",
    "abc123", "password1", "admin", "welcome", "letmein"
]

# Password generator function
def generate_strong_password(length=12):
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    while True:
        password = ''.join(random.choice(characters) for _ in range(length))
        # Ensure it meets all criteria
        if (len(password) >= 8 and
            re.search(r"[A-Z]", password) and
            re.search(r"[a-z]", password) and
            re.search(r"\d", password) and
            re.search(r"[!@#$%^&*]", password)):
            return password

# Password strength checker
def check_password_strength(password):
    feedback = []
    score = 0
    
    # Check against common weak passwords
    if password.lower() in WEAK_PASSWORDS:
        feedback.append("❌ This is a very common weak password")
        return 0, feedback
    
    # Length Check
    length = len(password)
    if length >= 12:
        score += 2
        feedback.append("✅ Excellent length (12+ characters)")
    elif length >= 8:
        score += 1
        feedback.append("✅ Good length (8+ characters)")
    else:
        feedback.append(f"❌ Too short ({length} characters), needs at least 8")
    
    # Upper & Lowercase Check
    has_upper = re.search(r"[A-Z]", password)
    has_lower = re.search(r"[a-z]", password)
    if has_upper and has_lower:
        score += 1
        feedback.append("✅ Contains both uppercase and lowercase letters")
    else:
        if not has_upper:
            feedback.append("❌ Missing uppercase letters")
        if not has_lower:
            feedback.append("❌ Missing lowercase letters")
    
    # Digit Check
    if re.search(r"\d", password):
        score += 1
        feedback.append("✅ Contains at least one number")
    else:
        feedback.append("❌ Missing numbers")
    
    # Special Character Check
    if re.search(r"[!@#$%^&*]", password):
        score += 1
        feedback.append("✅ Contains at least one special character (!@#$%^&*)")
    else:
        feedback.append("❌ Missing special characters (!@#$%^&*)")
    
    # Entropy check (bonus)
    char_counts = defaultdict(int)
    for char in password:
        char_counts[char] += 1
    entropy = sum(-(count/length)*((count/length)) for count in char_counts.values())
    if entropy > 2.5:
        score += 1
        feedback.append("✅ Good character variety (high entropy)")
    else:
        feedback.append("⚠️ Low character variety - many repeated characters")
    
    # Sequential characters check
    if re.search(r"(.)\1{2,}", password):
        score -= 1
        feedback.append("⚠️ Avoid repeated characters (e.g., 'aaa', '111')")
    
    # Common patterns
    if re.search(r"(123|abc|qwerty)", password.lower()):
        score -= 1
        feedback.append("⚠️ Avoid common sequences (e.g., '123', 'abc')")
    
    # Ensure score is within bounds
    score = max(0, min(5, score))
    
    return score, feedback

# Streamlit UI
st.title("🔐 Password Strength Meter")
st.markdown("Check how strong your password is and get suggestions for improvement")

tab1, tab2 = st.tabs(["Check Password", "Generate Password"])

with tab1:
    password = st.text_input("Enter your password:", type="password")
    
    if password:
        score, feedback = check_password_strength(password)
        
        # Display strength meter
        st.subheader("Password Strength")
        if score <= 1:
            st.error("Very Weak")
            st.progress(0.2)
        elif score <= 2:
            st.warning("Weak")
            st.progress(0.4)
        elif score <= 3:
            st.info("Moderate")
            st.progress(0.6)
        elif score == 4:
            st.success("Strong")
            st.progress(0.8)
        else:
            st.success("Very Strong!")
            st.progress(1.0)
            st.balloons()
        
        # Display feedback
        st.subheader("Feedback")
        for item in feedback:
            if item.startswith("✅"):
                st.success(item)
            elif item.startswith("⚠️"):
                st.warning(item)
            else:
                st.error(item)

with tab2:
    st.subheader("Generate a Strong Password")
    length = st.slider("Select password length", 8, 20, 12)
    if st.button("Generate Password"):
        password = generate_strong_password(length)
        st.code(password, language="text")
        st.success("Generated a strong password that meets all security criteria!")
        
        # Show strength check for generated password
        score, feedback = check_password_strength(password)
        st.subheader("This password meets:")
        for item in feedback:
            if item.startswith("✅"):
                st.success(item)

# About section
st.markdown("---")
st.markdown("""
### 🔒 Password Security Tips
- Use **at least 12 characters** for important accounts
- **Never reuse passwords** across different sites
- Consider using a **password manager** to store your passwords securely
- Enable **two-factor authentication** where available
""")