import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- Configuration and Setup ---

# Set page configuration for high contrast (using the built-in dark theme preference)
st.set_page_config(
    page_title="Simple Gym Logger",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for high readability (optional, for explicit contrast/styling)
st.markdown("""
<style>
    /* Ensure good contrast, mainly relies on Streamlit's theme settings */
    .stApp {
        background-color: #0d1117; /* Dark background */
        color: #f0f6fc; /* Light text color */
    }
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        background-color: #161b22; /* Slightly lighter dark input field */
        color: #f0f6fc;
        border: 1px solid #30363d;
    }
    .stButton>button {
        background-color: #238636; /* GitHub green for primary button */
        color: white;
        font-weight: bold;
        border-radius: 6px;
    }
    /* Main title and header styling */
    h1 {
        color: #238636;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)


# --- Session State Initialization ---

if 'workout_log' not in st.session_state:
    # Initialize the log as an empty list to store dictionaries
    st.session_state.workout_log = []

# --- Helper Functions ---

def log_workout(exercise, sets, reps, weight):
    """Adds a new workout entry to the session state log."""
    if exercise and sets > 0 and reps > 0 and weight >= 0:
        new_entry = {
            'Date': datetime.now().strftime('%Y-%m-%d'),
            'Time': datetime.now().strftime('%H:%M:%S'),
            'Exercise': exercise.strip(),
            'Sets': sets,
            'Reps': reps,
            'Weight': weight,
            'Volume': sets * reps * weight # Calculated metric
        }
        st.session_state.workout_log.append(new_entry)
        # Force re-run to clear the input fields immediately
        st.rerun()
    else:
        st.error("Please ensure all fields are filled correctly (Sets/Reps > 0, Weight >= 0).")

# --- UI Layout ---

st.title("🏋️‍♂️ Simple Gym Workout Logger")

# 1. Workout Input Form
with st.container():
    st.header("Log a New Set", divider='green')
    
    # Use columns for a clean, horizontal layout on desktop
    col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 2])
    
    with col1:
        exercise_name = st.text_input("Exercise", key="ex_name_input", placeholder="e.g., Bench Press, Squat")
    
    with col2:
        sets = st.number_input("Sets", min_value=1, value=3, step=1, key="sets_input")
        
    with col3:
        reps = st.number_input("Reps", min_value=1, value=10, step=1, key="reps_input")

    with col4:
        weight = st.number_input("Weight (kg/lb)", min_value=0.0, value=100.0, step=2.5, format="%.1f", key="weight_input")
        
    # The button is placed slightly lower for better visual separation from inputs
    st.markdown("---")
    if st.button("💪 Log Set"):
        log_workout(exercise_name, sets, reps, weight)
        
    st.markdown("---")


# Check if the log is empty before proceeding
if not st.session_state.workout_log:
    st.info("Start logging your workouts! Your history and progress graph will appear here.")
else:
    # Convert log to DataFrame for easy processing/display
    df_log = pd.DataFrame(st.session_state.workout_log)

    # 2. Progress Graph (Weekly Volume)
    st.header("Weekly Progress: Total Volume", divider='green')

    # Convert 'Date' to datetime objects
    df_log['Date'] = pd.to_datetime(df_log['Date'])
    
    # Calculate daily total volume
    daily_volume_df = df_log.groupby('Date')['Volume'].sum().reset_index()
    
    # Filter for the last 7 days
    last_7_days = datetime.now() - timedelta(days=6)
    weekly_volume_df = daily_volume_df[daily_volume_df['Date'] >= last_7_days.strftime('%Y-%m-%d')]

    # Ensure all 7 days are present for a clean graph (even if volume is 0)
    date_range = [datetime.now() - timedelta(days=x) for x in range(7)]
    dates_df = pd.DataFrame({'Date': date_range})
    dates_df['Date'] = dates_df['Date'].dt.strftime('%Y-%m-%d')
    weekly_volume_df['Date'] = weekly_volume_df['Date'].dt.strftime('%Y-%m-%d')
    
    # Merge to include days with zero volume
    weekly_volume_df = dates_df.merge(weekly_volume_df, on='Date', how='left').fillna(0)
    weekly_volume_df.rename(columns={'Volume': 'Total Volume'}, inplace=True)
    
    # Sort for correct graph display
    weekly_volume_df.sort_values(by='Date', inplace=True)

    # Display the chart
    st.line_chart(weekly_volume_df, x='Date', y='Total Volume', use_container_width=True)
    
    # 3. Full Workout History Table
    st.header("Current Session History", divider='green')

    # Display the DataFrame, dropping the intermediate 'Volume' column from the view
    st.dataframe(
        df_log.drop(columns=['Volume']).sort_values(by=['Date', 'Time'], ascending=[False, False]), 
        use_container_width=True,
        # Customize columns for better display
        column_order=['Date', 'Time', 'Exercise', 'Sets', 'Reps', 'Weight'],
        hide_index=True
    )

    # Simple button to clear the log (uses session state)
    st.markdown("---")
    if st.button("❌ Clear All Logs (Current Session)"):
        st.session_state.workout_log = []
        st.success("All workout logs have been cleared.")
        st.rerun()