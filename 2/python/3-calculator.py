import streamlit as st

# --- Page setup ---
st.set_page_config(page_title="Simple Calculator", page_icon="🧮", layout="centered")

# --- Custom CSS for blending corners and smooth UI ---
st.markdown("""
    <style>
        .main {
            background: linear-gradient(145deg, #f3f3f3, #e2e2e2);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 2px 2px 12px rgba(0,0,0,0.1);
        }
        .stTextInput > div > div > input {
            border-radius: 10px;
            height: 3em;
            font-size: 18px;
            text-align: center;
        }
        .stSelectbox > div > div {
            border-radius: 10px;
        }
        .stButton>button {
            width: 100%;
            height: 3em;
            border-radius: 12px;
            background: #0078D4;
            color: white;
            font-size: 18px;
            font-weight: 600;
            border: none;
        }
        .stButton>button:hover {
            background: #005fa3;
        }
        .result-box {
            margin-top: 20px;
            background: #ffffff;
            padding: 15px;
            border-radius: 12px;
            box-shadow: inset 0 0 8px rgba(0,0,0,0.05);
            text-align: center;
            font-size: 22px;
            font-weight: 600;
            color: black;
        }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.title("🧮 Simple Calculator")
st.write("A friendly calculator designed for everyone — especially our elders — to make digital tools easy to use 💙")

# --- Input fields ---
num1 = st.number_input("Enter first number", format="%.2f")
operation = st.selectbox("Choose operation", ["+", "-", "×", "÷", "%"])
num2 = st.number_input("Enter second number", format="%.2f")

# --- Perform calculation ---
result = None
if st.button("Calculate"):
    try:
        if operation == "+":
            result = num1 + num2
        elif operation == "-":
            result = num1 - num2
        elif operation == "×":
            result = num1 * num2
        elif operation == "÷":
            if num2 == 0:
                st.error("🚫 Division by zero is not allowed!")
            else:
                result = num1 / num2
        elif operation == "%":
            if num2 == 0:
                st.error("🚫 Division by zero is not allowed!")
            else:
                result = num1 % num2
    except Exception as e:
        st.error(f"⚠️ Something went wrong: {e}")

# --- Display result ---
if result is not None:
    st.markdown(f"<div class='result-box'>Result: {result}</div>", unsafe_allow_html=True)
