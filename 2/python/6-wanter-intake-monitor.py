# app.py
"""
Water Intake Tracker 💧
Run: streamlit run app.py

What it does:
- Log water intake (ml) with timestamp (defaults to now)
- Quick-add buttons for common amounts
- Persist entries to data/water_log.csv (created automatically)
- Show today's summary, progress to 3L (3000 ml), and friendly messages
- Weekly hydration chart (last 7 days) using Altair
- Download last-7-days CSV and download a PNG of the weekly chart
- Delete entries (choose an entry to delete or delete the last entry)
- Minimal dependencies: streamlit, pandas, altair, matplotlib

Short README (usage)
1. Install dependencies: pip install -r requirements.txt
2. Run: streamlit run app.py
3. Use sidebar to add quick amounts or custom ml and press "Add"
4. Download CSV / chart from sidebar
5. Delete entries from history section if needed
"""

import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
from io import BytesIO
from datetime import datetime, timedelta
from pathlib import Path
import os

# ---------------------------
# Configuration / Constants
# ---------------------------
DATA_DIR = Path("data")
DATA_FILE = DATA_DIR / "water_log.csv"
GOAL_ML = 3000
QUICK_AMOUNTS = [250, 500, 750]  # ml quick-add buttons
CAP_SOFT_WARNING_ML = 2000  # suggest confirmation over this
DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"  # ISO-like without timezone to keep simple (local time)
# ---------------------------

st.set_page_config(page_title="Water Intake Tracker 💧", layout="centered")

# ---------------------------
# Helper functions
# ---------------------------


def ensure_data_file():
    """Ensure data directory and CSV exist (with header)."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        df = pd.DataFrame(columns=["timestamp", "ml"])
        df.to_csv(DATA_FILE, index=False)


def load_data() -> pd.DataFrame:
    """Load CSV into DataFrame. Ensure timestamp column is parsed."""
    ensure_data_file()
    try:
        df = pd.read_csv(DATA_FILE)
        if df.empty:
            return df
        # parse timestamps; keep as strings for display but create parsed dt column when needed
        return df
    except Exception:
        # Corrupt or missing -> return empty df with columns
        return pd.DataFrame(columns=["timestamp", "ml"])


def save_data(df: pd.DataFrame):
    """Save DataFrame to CSV (overwrite)."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(DATA_FILE, index=False)


def add_entry(ml: int, ts: datetime = None):
    """Append a new entry to CSV."""
    if ts is None:
        ts = datetime.now()
    df = load_data()
    new = {"timestamp": ts.strftime(DATE_FORMAT), "ml": int(ml)}
    df = pd.concat([df, pd.DataFrame([new])], ignore_index=True)
    save_data(df)


def delete_entry_by_index(idx: int):
    """Delete entry by integer index (0-based)."""
    df = load_data()
    if idx < 0 or idx >= len(df):
        return False
    df = df.drop(df.index[idx]).reset_index(drop=True)
    save_data(df)
    return True


def get_today_total(df: pd.DataFrame, today: datetime = None) -> int:
    """Sum ml for today's date (local system date)."""
    if df.empty:
        return 0
    if today is None:
        today = datetime.now()
    df2 = df.copy()
    df2["dt"] = pd.to_datetime(df2["timestamp"], format=DATE_FORMAT, errors="coerce")
    df2["date"] = df2["dt"].dt.date
    total = int(df2[df2["date"] == today.date()]["ml"].sum())
    return total


def last_7_days_aggregation(df: pd.DataFrame, today: datetime = None) -> pd.DataFrame:
    """
    Returns a DataFrame with last 7 days (including today) and total ml per day.
    Columns: date (datetime.date), ml
    """
    if today is None:
        today = datetime.now()
    dates = [ (today - timedelta(days=i)).date() for i in reversed(range(7)) ]  # oldest -> newest
    agg = pd.DataFrame({"date": dates, "ml": [0]*7})
    if df.empty:
        return agg
    df2 = df.copy()
    df2["dt"] = pd.to_datetime(df2["timestamp"], format=DATE_FORMAT, errors="coerce")
    df2["date"] = df2["dt"].dt.date
    grouped = df2.groupby("date")["ml"].sum().reset_index()
    # merge
    agg = agg.merge(grouped, on="date", how="left", suffixes=("_x", ""))
    agg["ml"] = agg["ml"].fillna(agg["ml_x"]).fillna(0).astype(int)
    agg = agg[["date", "ml"]]
    return agg


def ml_to_l(ml: int) -> float:
    return round(ml / 1000.0, 2)


def create_altair_chart(agg_df: pd.DataFrame, highlight_date=None):
    """
    Create an Altair bar chart for the last 7 days.
    highlight_date: datetime.date to highlight (today)
    """
    chart_df = agg_df.copy()
    chart_df["day"] = chart_df["date"].apply(lambda d: d.strftime("%a\n%Y-%m-%d"))
    chart_df["is_today"] = chart_df["date"] == (highlight_date if highlight_date else datetime.now().date())

    base = alt.Chart(chart_df).mark_bar(size=30).encode(
        x=alt.X("day:N", title=None, sort=None),
        y=alt.Y("ml:Q", title="Total (ml)"),
        tooltip=[alt.Tooltip("date:T", title="Date"), alt.Tooltip("ml:Q", title="Total (ml)")],
        color=alt.condition(alt.datum.is_today, alt.value("#1f77b4"), alt.value("#d3d3d3")),
    ).properties(
        height=300,
        width="container",
        title="Last 7 days — Daily total"
    )

    # goal rule
    rule = alt.Chart(pd.DataFrame({"goal": [GOAL_ML]})).mark_rule(strokeDash=[4,4]).encode(
        y="goal:Q"
    )

    return (base + rule).configure_title(fontSize=16).interactive()


def create_matplotlib_chart_bytes(agg_df: pd.DataFrame, highlight_date=None) -> BytesIO:
    """Create a matplotlib bar chart and return PNG bytes in BytesIO for download."""
    fig, ax = plt.subplots(figsize=(8, 4.5))
    dates = agg_df["date"].dt if isinstance(agg_df["date"].dtype, pd.DatetimeTZDtype) else pd.to_datetime(agg_df["date"])
    labels = agg_df["date"].apply(lambda d: d.strftime("%a\n%d %b"))
    bars = ax.bar(labels, agg_df["ml"])
    # highlight today's bar
    today = highlight_date if highlight_date else datetime.now().date()
    for rect, d in zip(bars, agg_df["date"]):
        if d == today:
            rect.set_edgecolor("black")
            rect.set_linewidth(1.5)
    ax.axhline(GOAL_ML, linestyle="--")
    ax.set_ylabel("ml")
    ax.set_title("Last 7 days — Daily total")
    plt.tight_layout()

    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    plt.close(fig)
    return buf


# ---------------------------
# App UI
# ---------------------------

st.title("Water Intake Tracker 💧")
st.write("Log water quickly. Aim: **3 L / day** (3000 ml). Keep hydrated — Happy healthy life 🤍")
st.write("---")

# Sidebar: controls
with st.sidebar:
    st.header("Add water")
    st.write("Quick amounts")
    col_quick = st.columns(len(QUICK_AMOUNTS))
    for i, amt in enumerate(QUICK_AMOUNTS):
        if col_quick[i].button(f"+{amt} ml"):
            # quick add immediately
            add_entry(amt)
            st.rerun()

    st.markdown("---")
    st.markdown("**Custom amount**")
    custom_ml = st.number_input("Amount (ml)", min_value=1, value=250, step=50, help="Enter amount in milliliters (ml)")
    date_val = st.date_input("Date (optional)", value=datetime.now().date(), help="Defaults to today")
    time_val = st.time_input("Time (optional)", value=datetime.now().time().replace(microsecond=0), help="Defaults to current time")
    custom_ts = datetime.combine(date_val, time_val)
    # confirmation for very large entries
    confirm_large = False
    if custom_ml > CAP_SOFT_WARNING_ML:
        confirm_large = st.checkbox(f"I confirm {custom_ml} ml is correct (entries > {CAP_SOFT_WARNING_ML} ml require confirmation)")

    if st.button("Add"):
        if custom_ml <= 0:
            st.error("Please enter a positive amount of water (ml).")
        elif custom_ml > CAP_SOFT_WARNING_ML and not confirm_large:
            st.warning("Please confirm the large amount by checking the box before adding.")
        else:
            add_entry(int(custom_ml), ts=custom_ts)
            st.success(f"Added {custom_ml} ml at {custom_ts.strftime('%Y-%m-%d %H:%M:%S')}")
            st.rerun()

    st.markdown("---")
    st.header("Export & Share")
    # Export last 7 days CSV
    df_all = load_data()
    last7_agg = last_7_days_aggregation(df_all)
    # Build last 7 days raw entries for export
    if not df_all.empty:
        df_all["dt"] = pd.to_datetime(df_all["timestamp"], format=DATE_FORMAT, errors="coerce")
        seven_days_ago = datetime.now().date() - timedelta(days=6)
        last7_raw = df_all[df_all["dt"].dt.date >= seven_days_ago].sort_values("dt")
    else:
        last7_raw = pd.DataFrame(columns=["timestamp", "ml"])

    csv_bytes = last7_raw.to_csv(index=False).encode("utf-8")
    st.download_button("Download last 7 days CSV", data=csv_bytes, file_name="water_last7.csv", mime="text/csv")

    # Chart PNG download: create matplotlib version for reliable PNG generation
    chart_png = create_matplotlib_chart_bytes(last7_agg, highlight_date=datetime.now().date())
    st.download_button("Download weekly chart (PNG)", data=chart_png, file_name="weekly_chart.png", mime="image/png")

    st.markdown("---")
    st.caption("Tip: You can also take a screenshot from your device. To share the chart quickly, download the PNG above.")
    st.markdown("---")
    st.write("Made with ❤️ — Share the screenshots, Happy Healthy living 🤍")

# Main area
df = load_data()

# Today's summary and progress
today_total_ml = get_today_total(df)
today_total_l = ml_to_l(today_total_ml)
percent = min(100, int((today_total_ml / GOAL_ML) * 100)) if GOAL_ML > 0 else 0
remaining_ml = max(0, GOAL_ML - today_total_ml)

col1, col2 = st.columns([2, 1])
with col1:
    st.subheader("Today's progress")
    st.metric(label="Total today", value=f"{today_total_ml} ml", delta=f"{today_total_l} L")
    st.write(f"Goal: {GOAL_ML} ml ({ml_to_l(GOAL_ML)} L)")
    st.progress(percent / 100.0)
    if today_total_ml >= GOAL_ML:
        st.success(f"🎉 Congrats — you hit your goal! You drank {today_total_ml} ml today.")
    else:
        st.info(f"Almost there — {remaining_ml} ml to reach {ml_to_l(GOAL_ML)} L!")

with col2:
    st.subheader("Quick summary")
    st.write(f"Progress: **{percent}%**")
    st.write(f"Remaining: **{remaining_ml} ml**")
    st.write(f"Today's total: **{today_total_l} L**")

st.markdown("---")

# Weekly chart
st.subheader("Weekly hydration")
agg = last_7_days_aggregation(df)
# ensure date column is datetime.date -> convert to pandas.Timestamp for Altair compatibility
agg["date"] = pd.to_datetime(agg["date"])
chart = create_altair_chart(agg, highlight_date=datetime.now().date())
st.altair_chart(chart, use_container_width=True)

st.markdown("---")

# Recent entries & history / delete
st.subheader("Recent entries")
if df.empty:
    st.info("No entries yet — add a quick amount from the sidebar.")
else:
    # show most recent 50 entries with newest on top
    df_display = df.copy()
    df_display["dt"] = pd.to_datetime(df_display["timestamp"], format=DATE_FORMAT, errors="coerce")
    df_display = df_display.sort_values("dt", ascending=False).reset_index(drop=True)
    df_display["when"] = df_display["dt"].dt.strftime("%Y-%m-%d %H:%M:%S")
    compact = df_display[["when", "ml"]].rename(columns={"when": "timestamp", "ml": "ml (ml)"})
    st.dataframe(compact.head(50), use_container_width=True)

    st.markdown("**Delete an entry**")
    st.write("Pick an entry below to delete (this is irreversible). As a quick option, you can delete the last entry added.")
    # Make a selection mapping to original index in the stored CSV
    df_orig = load_data()
    if not df_orig.empty:
        df_orig["dt"] = pd.to_datetime(df_orig["timestamp"], format=DATE_FORMAT, errors="coerce")
        df_orig = df_orig.reset_index().rename(columns={"index":"orig_index"})
        # prepare choices
        choices = df_orig.sort_values("dt", ascending=False).apply(
            lambda row: f"{row['orig_index']}: {row['dt'].strftime('%Y-%m-%d %H:%M:%S')} — {row['ml']} ml", axis=1
        ).tolist()
        to_delete = st.selectbox("Select entry to delete", options=["(none)"] + choices, index=0)
        if to_delete != "(none)":
            if st.button("Delete selected entry"):
                # parse orig_index from selected label
                orig_index = int(to_delete.split(":")[0])
                ok = delete_entry_by_index(orig_index)
                if ok:
                    st.success("Deleted entry.")
                    st.rerun()
                else:
                    st.error("Failed to delete (index not found).")
        # Quick delete last entry (most recent by time)
        if st.button("Delete last entry"):
            # find last entry index (latest dt)
            latest_row = df_orig.sort_values("dt", ascending=False).head(1)
            if latest_row.empty:
                st.warning("No entry to delete.")
            else:
                idx = int(latest_row.iloc[0]["orig_index"])
                delete_entry_by_index(idx)
                st.success("Deleted last entry.")
                st.rerun()

st.write("---")
st.caption("Small accessible UI, clear labels (ml / L), and CSV persistence in `data/water_log.csv`.")
st.markdown("### Footer")
st.write("Share the screenshots — Happy Learning guys 🤍")
