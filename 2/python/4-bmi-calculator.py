import streamlit as st

st.set_page_config(page_title="BMI Calculator", page_icon="⚕️", layout="centered")

# ---------- Utility Functions ----------
def get_bmi(weight, height_cm):
    if height_cm == 0:
        return 0
    height_m = height_cm / 100
    return weight / (height_m * height_m)

def get_category(bmi):
    if bmi == 0:
        return ("Invalid", "#6c757d", "#ffffff")
    if bmi < 18.5:
        return ("Underweight", "#0d6efd", "#ffffff")  # Blue
    elif 18.5 <= bmi < 25:
        return ("Normal", "#198754", "#ffffff")       # Green
    elif 25 <= bmi < 30:
        return ("Overweight", "#fd7e14", "#000000")   # Orange (high contrast)
    else:
        return ("Obese", "#b02a37", "#ffffff")        # Dark Red
        

# ---------- UI Styling ----------
st.markdown("""
    <style>
        .big-input input {
            font-size: 22px !important;
            height: 55px !important;
        }
        .big-label {
            font-size: 24px !important;
            font-weight: 600 !important;
        }
        .big-button button {
            font-size: 24px !important;
            padding: 15px 30px !important;
        }
        .result-box {
            padding: 25px;
            border-radius: 12px;
            font-size: 26px;
            text-align: center;
            margin-top: 20px;
        }
    </style>
""", unsafe_allow_html=True)


st.title("⚕️ BMI Calculator")
st.write("### Simple, clear calculator for everyone in the family.")

# ---------- Form ----------
with st.form("bmi_form"):
    st.markdown("<div class='big-label'>Weight (kg)</div>", unsafe_allow_html=True)
    weight = st.number_input(
        label="",
        min_value=1.0,
        max_value=300.0,
        value=60.0,
        step=1.0,
        key="weight",
        format="%.1f",
        help="Enter your weight in kilograms",
    )

    st.markdown("<div class='big-label'>Height (cm)</div>", unsafe_allow_html=True)
    height = st.number_input(
        label="",
        min_value=30.0,
        max_value=250.0,
        value=170.0,
        step=1.0,
        key="height",
        format="%.1f",
        help="Enter your height in centimeters",
    )

    submitted = st.form_submit_button("Calculate BMI", use_container_width=True)

# ---------- Result ----------
if submitted:
    bmi = get_bmi(weight, height)
    category, bg_color, text_color = get_category(bmi)

    st.markdown(
        f"""
        <div class="result-box" style="background-color:{bg_color}; color:{text_color};">
            <b>BMI: {bmi:.2f}</b><br>
            <span>{category}</span>
        </div>
        """,
        unsafe_allow_html=True
    )
