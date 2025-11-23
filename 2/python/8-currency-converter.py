import streamlit as st

st.set_page_config(page_title="Currency Converter 💱", page_icon="💱", layout="centered")

# Simple POC styles
st.markdown(
    """
    <style>
      .stApp { background: #0d1117; color: #f0f6fc; }
      .block-container { max-width: 720px; }
      .card { background:#11161c; border:1px solid #30363d; border-radius:12px; padding:16px; }
      .result { font-size: 1.8rem; font-weight: 700; color: #58a6ff; }
      .muted { color:#8b949e; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Currency Converter 💱")
st.caption("Simple POC. Static example rates, not live forex.")

# Static example rates (per 1 USD)
# These are illustrative only; change as needed.
RATES_PER_USD = {
    "USD": 1.0,
    "INR": 88.50,
    "EUR": 0.92,
    "GBP": 0.78,
}

CODES = list(RATES_PER_USD.keys())

@st.cache_data(show_spinner=False)
def convert(amount: float, src: str, dst: str) -> float:
    if src == dst:
        return amount
    # Convert src -> USD -> dst
    usd_amount = amount / RATES_PER_USD[src]
    return usd_amount * RATES_PER_USD[dst]

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        src = st.selectbox("From", CODES, index=0)
    with col2:
        dst = st.selectbox("To", CODES, index=1)

    amount = st.number_input("Amount", min_value=0.0, value=1.0, step=1.0, format="%0.2f")

    res = convert(amount, src, dst)

    st.markdown("---")
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.write("Result")
    st.markdown(f"<div class='result'>{res:,.4f} {dst}</div>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='muted'>Rate basis (illustrative): 1 USD = {RATES_PER_USD['INR']} INR, {RATES_PER_USD['EUR']} EUR, {RATES_PER_USD['GBP']} GBP</div>",
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("\n")
