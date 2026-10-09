import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from database import init_db, log_daily_data, fetch_history_data, clear_all_entries
from fit_handler import fetch_google_fit_data
from model import predict_productivity, get_performance_insights

# Page Configuration
st.set_page_config(page_title="AI Life Optimization Engine", layout="wide")
init_db()

st.title("⚡ AI Life Optimization Engine")
st.caption("Track, predict, and optimize your daily health, study habits, and productivity.")

# Fetch Live Google Fit Metrics
fit_data = fetch_google_fit_data()

# OAuth Authentication Guard
if not fit_data.get('authenticated', False):
    st.warning("🔒 Please authenticate with your Google account to access your live fitness dashboard.")
    if st.button("🔑 Sign in with Google"):
        fit_data = fetch_google_fit_data()
        st.rerun()
    st.stop()

# Initialize Session State
if "diagnostics_run" not in st.session_state:
    st.session_state.diagnostics_run = False

# Sidebar: Live Metrics & Reset Action
st.sidebar.header("👤 Account & Live Metrics")
st.sidebar.success(f"Status: {fit_data['status']}")
st.sidebar.metric("Live Step Count (Google Fit)", f"{fit_data['steps']} steps")

st.sidebar.markdown("---")
if st.sidebar.button("🗑️ Clear Database Logs"):
    clear_all_entries()
    st.sidebar.success("All historical logs cleared!")
    st.rerun()

# Unpack Live Fitness Metrics
step_count = fit_data['steps']
default_sleep = float(fit_data.get('sleep', 7.0)) if fit_data.get('sleep', 0) > 0 else 7.0

# Main Input Grid
st.subheader("📊 Enter Today's Metrics")

col_in1, col_in2, col_in3, col_in4 = st.columns(4)

with col_in1:
    sleep_hours = st.number_input("Sleep Duration (Hours)", min_value=0.0, max_value=24.0, value=default_sleep, step=0.5)

with col_in2:
    study_hours = st.number_input("Deep Focus / Study Time (Hours)", min_value=0.0, max_value=16.0, value=0.0, step=0.5)

with col_in3:
    screen_time = st.number_input("Recreational Screen Time (Hours)", min_value=0.0, max_value=16.0, value=0.0, step=0.5)

with col_in4:
    expenses = st.number_input("Daily Expenses (₹)", min_value=0.0, value=0.0, step=50.0)

# Main Action Button
st.markdown("")
if st.button("🚀 Run Performance Diagnostics", type="primary", use_container_width=True):
    st.session_state.diagnostics_run = True

st.markdown("---")

# Execution State
if not st.session_state.diagnostics_run:
    st.info("💡 Enter your daily metrics above and click **'Run Performance Diagnostics'** to calculate your score, radar chart, and bottleneck analysis.")
    
    # Historical Data View
    history = fetch_history_data()
    if history:
        st.subheader("📜 Historical Entries")
        history_df = pd.DataFrame(
            history, 
            columns=["Date", "Sleep (hrs)", "Steps", "Study (hrs)", "Screen Time (hrs)", "Expenses (₹)", "Score", "Bottleneck"]
        )
        st.dataframe(history_df, use_container_width=True)

else:
    # Run Predictions & Diagnostic Analysis
    features = [sleep_hours, step_count, study_hours, screen_time, expenses]
    predicted_score = predict_productivity(features)
    primary_bottleneck = get_performance_insights(features)

    # Metric Normalization (0 - 100 Scale)
    sleep_score = min((sleep_hours / 8.0) * 100, 100)
    activity_score = min((step_count / 10000.0) * 100, 100)
    study_score = min((study_hours / 6.0) * 100, 100)
    screen_control_score = max(0, 100 - (screen_time * 10))
    budget_score = max(0, 100 - (expenses / 500.0 * 100))

    metrics_dict = {
        "Sleep Duration": round(sleep_score, 1),
        "Physical Activity": round(activity_score, 1),
        "Study Focus": round(study_score, 1),
        "Screen Time Control": round(screen_control_score, 1),
        "Budget Management": round(budget_score, 1)
    }

    # Visual Layout: Performance Score & Radar Chart
    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.subheader("🎯 Daily Performance Score")
        st.metric("Predicted Productivity Index", f"{predicted_score} / 100")
        st.warning(f"🚨 **Primary Bottleneck Identified:** {primary_bottleneck}")

    with col_right:
        # Radar Chart
        radar_df = pd.DataFrame({
            'Category': list(metrics_dict.keys()),
            'Score': list(metrics_dict.values())
        })
        fig = px.line_polar(radar_df, r='Score', theta='Category', line_close=True, range_r=[0, 100])
        fig.update_traces(fill='toself')
        st.plotly_chart(fig, use_container_width=True)

    # Bottom Actions: Manual Save Option
    st.markdown("---")
    col_save, col_hist = st.columns([1, 2])
    
    with col_save:
        if st.button("💾 Save Entry to Database", use_container_width=True):
            log_daily_data(sleep_hours, step_count, study_hours, screen_time, expenses, predicted_score, primary_bottleneck)
            st.success("Entry saved!")
            st.rerun()

    with col_hist:
        history = fetch_history_data()
        if history:
            st.write("**Recent Activity Logs:**")
            history_df = pd.DataFrame(
                history, 
                columns=["Date", "Sleep (hrs)", "Steps", "Study (hrs)", "Screen Time (hrs)", "Expenses (₹)", "Score", "Bottleneck"]
            )
            st.dataframe(history_df, use_container_width=True)

    st.markdown("---")

    # Section 2: Comprehensive AI Diagnostic Summary & Detailed Recommendations
    st.header("🧠 AI Performance Diagnostics & Insights")

    diag_col1, diag_col2 = st.columns([1, 1])

    with diag_col1:
        st.subheader("📊 Category Diagnostics & Targets")
        st.write(f"• **Sleep Restorative Level:** `{sleep_hours} hrs` — **Target:** `Min 7.5 - 8.0 hrs` ({'✅ Optimal' if sleep_hours >= 7.5 else '⚠️ Needs Attention'})")
        st.write(f"• **Physical Activity Level:** `{step_count} steps` — **Target:** `Min 8,000 - 10,000 steps` ({'✅ Target Reached' if step_count >= 8000 else '⚠️ Below Target'})")
        st.write(f"• **Deep Work Focus Time:** `{study_hours} hrs` — **Target:** `Min 4.5 - 6.0 hrs` ({'✅ High Output' if study_hours >= 4.5 else '⚠️ Sub-optimal Focus'})")
        st.write(f"• **Screen Time Overhead:** `{screen_time} hrs` — **Target:** `Max 3.0 - 3.5 hrs` ({'✅ Balanced' if screen_time <= 3.5 else '⚠️ Excessive Usage'})")
        st.write(f"• **Financial Outlay:** `₹{expenses}` — **Target:** `Max ₹300 / day` ({'✅ Within Budget' if expenses <= 300 else '⚠️ High Expenditure'})")

    with diag_col2:
        st.subheader("💡 Tailored Optimization Strategies")
        
        has_issue = False

        if sleep_hours < 7.5:
            has_issue = True
            st.error(
                f"🌙 **Sleep Duration (Current: {sleep_hours} hrs | Target: Min 7.5 hrs):**\n"
                "Inadequate sleep reduces memory consolidation and cognitive speed. "
                "Establish a consistent circadian routine: avoid screen light 45 minutes before bedtime "
                "and aim for a fixed wake-up time to optimize REM sleep recovery."
            )

        if step_count < 8000:
            has_issue = True
            st.warning(
                f"🚶 **Physical Activity (Current: {step_count} steps | Target: Min 8,000 steps):**\n"
                "Low physical movement leads to mid-day lethargy and decreased focus. "
                "Incorporate two 15-minute brisk walks during breaks or schedule active study sessions "
                "to boost cardiovascular health and maintain energy stability."
            )

        if study_hours < 4.5:
            has_issue = True
            st.warning(
                f"📚 **Deep Work Focus (Current: {study_hours} hrs | Target: Min 4.5 hrs):**\n"
                "Your deep work output is below the optimal cognitive productivity threshold. "
                "Implement structured 50-minute Pomodoro sessions with zero digital interruptions "
                "to systematically build uninterrupted study momentum."
            )

        if screen_time > 3.5:
            has_issue = True
            st.error(
                f"📱 **Recreational Screen Time (Current: {screen_time} hrs | Target: Max 3.5 hrs):**\n"
                "Excessive non-essential screen usage triggers dopamine depletion and mental fatigue. "
                "Use application timers, switch device displays to grayscale during focus blocks, "
                "and set a strict daily screen limit."
            )

        if expenses > 300:
            has_issue = True
            st.error(
                f"💸 **Budget Management (Current: ₹{expenses} | Target: Max ₹300/day):**\n"
                "Daily expenditures exceed your target baseline, impacting long-term financial discipline. "
                "Track impulse spending, plan campus meals ahead of time, and review discretionary costs daily."
            )

        if not has_issue:
            st.success("🎉 **Routine Status:** Excellent work! All core life metrics are currently within optimal target thresholds.")

    st.markdown("---")

    # Section 3: Key Metric Breakdown Cards with Target Indicators
    st.subheader("📌 Key Metric Breakdown & Targets")
    m1, m2, m3, m4, m5 = st.columns(5)

    m1.metric("Sleep (Target: 8.0h)", f"{sleep_hours} hrs", f"{metrics_dict['Sleep Duration']}% Target")
    m2.metric("Steps (Target: 10k)", f"{step_count}", f"{metrics_dict['Physical Activity']}% Target")
    m3.metric("Study (Target: 6.0h)", f"{study_hours} hrs", f"{metrics_dict['Study Focus']}% Target")
    m4.metric("Screen Time (Max: 3.5h)", f"{screen_time} hrs", f"{metrics_dict['Screen Time Control']}% Control")
    m5.metric("Expenses (Max: ₹300)", f"₹{expenses}", f"{metrics_dict['Budget Management']}% Budget")