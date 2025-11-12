import streamlit as st

# Set page config
st.set_page_config(
    page_title="Greeting App",
    page_icon="👋",
    layout="centered"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        max-width: 500px;
        padding: 2rem;
        border-radius: 15px;
        background: linear-gradient(145deg, #f0f2f6, #ffffff);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        margin: 2rem auto;
    }
    .stTextInput>div>div>input {
        border-radius: 10px;
        padding: 10px;
    }
    .stSlider>div>div>div>div {
        background: #4CAF50 !important;
    }
    .greeting-box {
        background: linear-gradient(135deg, #4CAF50, #45a049);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-top: 2rem;
        animation: fadeIn 1s;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .emoji {
        font-size: 2rem;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Main container
with st.container():
    st.title("👋 Welcome to the Greeting App")
    st.markdown("---")
    
    # Form
    with st.form("greeting_form"):
        name = st.text_input("Your Name", placeholder="Enter your name here...")
        age = st.slider("Your Age", min_value=1, max_value=120, value=25)
        submit_button = st.form_submit_button("Get Greeting", type="primary")
    
    # Handle form submission
    if submit_button:
        if name.strip() == "":
            st.warning("Please enter your name!")
        else:
            # Generate emoji based on age
            if age < 18:
                emoji = "👶"
                age_group = "young one"
            elif age < 30:
                emoji = "😊"
                age_group = "young adult"
            elif age < 50:
                emoji = "👍"
                age_group = "mature individual"
            else:
                emoji = "👴"
                age_group = "wise person"
            
            # Display greeting
            greeting = f"""
            <div class="greeting-box">
                <div class="emoji">{emoji}</div>
                <h2>Hello, {name.title()}!</h2>
                <p>You are {age} years young! What a wonderful age to be a {age_group}!</p>
                <p>Thank you for using our app! Have a fantastic day! ✨</p>
            </div>
            """
            st.markdown(greeting, unsafe_allow_html=True)
            
            # Confetti effect
            st.balloons()
            
# Add some space at the bottom
st.markdown("<br><br>", unsafe_allow_html=True)

# Add a footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit")