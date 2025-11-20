import streamlit as st

st.set_page_config(page_title="Kids Unit Converter", page_icon="🔄", layout="centered")

st.markdown(
    """
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@500;700&display=swap');
      html, body, [class*="css"], .stMarkdown, .stButton>button, .stTextInput>div>div>input, .stNumberInput input {
        font-family: 'Poppins', sans-serif !important;
      }
      .stApp {
        background: linear-gradient(135deg, #FFDEE9 0%, #B5FFFC 100%);
      }
      .block-container {
        max-width: 800px;
        min-height: 100vh; /* take full viewport height */
        display: flex;
        flex-direction: column;
        justify-content: center; /* center vertically */
        padding: 2rem 1rem; /* balanced padding */
        position: absolute;
        top: 5rem;
      }
      .title-card {
        background: linear-gradient(135deg, #fff, #f5f5ff);
        padding: 18px 22px;
        border-radius: 18px;
        border: 4px solid #7C4DFF33;
        box-shadow: 0 12px 24px rgba(0,0,0,0.08);
        margin-bottom: 16px; /* space below title */
      }
      .big-label {
        font-size: 1.2rem;
        font-weight: 700;
        color: #512DA8;
      }
      .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
      }
      .stTabs [data-baseweb="tab"] {
        height: 60px;
        padding: 14px 18px;
        border-radius: 16px;
        background: #ffffffd9;
        border: 3px solid #90CAF925;
        box-shadow: 0 8px 16px rgba(0,0,0,0.05);
        font-size: 1.05rem;
        color: #FF7043; /* default orange/red text */
      }
      .stTabs [data-baseweb="tab"]:hover {
        color: #FF7043; /* keep same color on hover */
      }
      .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #A5D6A7, #81D4FA);
        color: #000000; /* black when focused/selected */
        border-color: #1E88E5;
      }
      .stNumberInput input, .stTextInput input {
        font-size: 1.4rem;
        padding: 18px 16px !important;
        border-radius: 16px !important;
        border: 3px solid #E1BEE7 !important;
        color: #1A237E; /* readable dark text */
      }
      .stNumberInput > div > div {
        border-radius: 16px !important;
      }
      .stSelectbox div[data-baseweb="select"] > div {
        padding: 14px 16px;
        border-radius: 16px;
        border: 3px solid #FFCC80;
        color: #FF7043; /* readable orange/red text */
      }
      .stRadio > div {
        gap: 16px;
      }
      .stRadio { color: #BF360C; }
      .stRadio label {
        padding: 10px 14px;
        background: #ffffff;
        border: 3px solid #FFAB91;
        border-radius: 14px;
        box-shadow: 0 6px 12px rgba(0,0,0,0.05);
        font-weight: 600;
        color: #BF360C; /* readable orange/red text */
      }
      .stRadio label span,
      .stRadio label div,
      .stRadio label p {
        color: #BF360C !important; /* force inner label elements to same color */
      }
      .stRadio label:hover { color: #BF360C; }
      .stNumberInput label {
        color: #BF360C;
        font-weight: 700;
      }
      .stButton>button {
        font-size: 1.2rem;
        padding: 14px 22px;
        border-radius: 16px;
        border: 0;
        background: linear-gradient(135deg, #FFD54F, #FF8A65);
        color: #1A237E;
        box-shadow: 0 10px 18px rgba(0,0,0,0.15);
      }
      .stButton>button:hover, .stButton>button:focus { color: #1A237E; }
      .stNumberInput input::placeholder { color: #FF7043; opacity: 0.85; }
      .stNumberInput input:focus { border-color: #FF7043 !important; outline: none; }
      /* Base Web input (used by text-like inputs) */
      div[data-baseweb="base-input"] input {
        color: #FFFFFF !important;
      }
      div[data-baseweb="base-input"] input::placeholder {
        color: #FFFFFF !important;
        opacity: 0.95;
      }
      .result-card {
        margin-top: 10px;
        background: linear-gradient(135deg, #E1F5FE, #E8F5E9);
        border-radius: 18px;
        border: 4px solid #81D4FA;
        padding: 18px;
        box-shadow: 0 12px 24px rgba(0,0,0,0.08);
      }
      .result-value {
        font-size: 2rem;
        font-weight: 800;
        color: #0D47A1;
      }
      .unit-badge {
        display: inline-block;
        padding: 6px 12px;
        margin-left: 8px;
        border-radius: 999px;
        background: #F8BBD0;
        border: 3px solid #F06292;
        font-weight: 700;
        color: #880E4F;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

def round_display(x: float, places: int = 6) -> str:
    try:
        return f"{x:.{places}f}".rstrip('0').rstrip('.') if places else str(x)
    except Exception:
        return str(x)

USD_PER_INR = 1.0 / 88.51
INR_PER_USD = 88.51

def inr_to_usd(x: float) -> float:
    return x * USD_PER_INR

def usd_to_inr(x: float) -> float:
    return x * INR_PER_USD

def c_to_f(x: float) -> float:
    return (x * 9.0 / 5.0) + 32.0

def f_to_c(x: float) -> float:
    return (x - 32.0) * 5.0 / 9.0

def cm_to_inch(x: float) -> float:
    return x * 0.393701

def inch_to_cm(x: float) -> float:
    return x * 2.54

def kg_to_lb(x: float) -> float:
    return x * 2.20462

def lb_to_kg(x: float) -> float:
    return x * 0.453592

st.markdown(
    """
    <div class="title-card">
      <h1 style="margin:0; font-size: 2.2rem; color:#283593;">🔄 Kids Unit Converter</h1>
      <div style="font-size:1.05rem;color:#6A1B9A; font-weight:700;">Big, colorful and easy! Tap, type, convert ✨</div>
    </div>
    """,
    unsafe_allow_html=True,
)

tabs = st.tabs([
    "💰 Currency",
    "🌡️ Temperature",
    "📏 Length",
    "🏋️ Weight",
])

with tabs[0]:
    st.write("")
    direction = st.radio("Choose conversion", ["INR → USD", "USD → INR"], horizontal=True)
    amount = st.number_input("Enter amount", value=1.0, step=1.0, format="%0.6f")
    if direction == "INR → USD":
        res = inr_to_usd(amount)
        unit = "USD"
        badge = "💵"
    else:
        res = usd_to_inr(amount)
        unit = "INR"
        badge = "₹"
    st.markdown(
        f"""
        <div class="result-card">
          <div class="big-label">Result</div>
          <div class="result-value">{round_display(res)} <span class="unit-badge">{badge} {unit}</span></div>
          <div style="margin-top:6px;color:#6D4C41;font-weight:700;">Rate used: 1 USD = {INR_PER_USD} INR (example)</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with tabs[1]:
    st.write("")
    direction = st.radio("Choose conversion", ["°C → °F", "°F → °C"], horizontal=True)
    val = st.number_input("Enter temperature", value=1.0, step=1.0, format="%0.6f")
    if direction == "°C → °F":
        res = c_to_f(val)
        unit = "°F"
    else:
        res = f_to_c(val)
        unit = "°C"
    st.markdown(
        f"""
        <div class="result-card">
          <div class="big-label">Result</div>
          <div class="result-value">{round_display(res)} <span class="unit-badge">{unit}</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with tabs[2]:
    st.write("")
    direction = st.radio("Choose conversion", ["cm → inch", "inch → cm"], horizontal=True)
    val = st.number_input("Enter length", value=1.0, step=1.0, format="%0.6f")
    if direction == "cm → inch":
        res = cm_to_inch(val)
        unit = "inch"
    else:
        res = inch_to_cm(val)
        unit = "cm"
    st.markdown(
        f"""
        <div class="result-card">
          <div class="big-label">Result</div>
          <div class="result-value">{round_display(res)} <span class="unit-badge">{unit}</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with tabs[3]:
    st.write("")
    direction = st.radio("Choose conversion", ["kg → lb", "lb → kg"], horizontal=True)
    val = st.number_input("Enter weight", value=1.0, step=1.0, format="%0.6f")
    if direction == "kg → lb":
        res = kg_to_lb(val)
        unit = "lb"
    else:
        res = lb_to_kg(val)
        unit = "kg"
    st.markdown(
        f"""
        <div class="result-card">
          <div class="big-label">Result</div>
          <div class="result-value">{round_display(res)} <span class="unit-badge">{unit}</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

