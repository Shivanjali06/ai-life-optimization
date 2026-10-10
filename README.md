AI Life Optimization Engine

An all-in-one daily tracking, prediction, and diagnostic platform designed to bridge physical fitness, academic productivity, digital wellness, and personal finance into a single unified interface.

What Makes This App Unique

Unlike traditional habit trackers, fitness logs, or budgeting tools that operate in isolated silos, the AI Life Optimization Engine consolidates multiple core life dimensions into a single intelligent platform:

- Unified Life Metrics: Tracks physical activity, sleep, study focus, screen time, and daily spending in one central dashboard.
- Machine Learning Diagnostics: Uses a trained Scikit-Learn Random Forest model to calculate a daily Productivity Index (0 to 100) and identify primary behavioral bottlenecks.
- Multi-Category Strategy Feedback: Provides tailored, real-time diagnostic warnings and targeted suggestions across all failing metric thresholds simultaneously.
- Live Fitness Integration: Syncs step counts directly with Google Fit REST API while offering full manual override controls for precise daily data logging.

Tech Stack and Architecture

- Frontend and Dashboard: Streamlit, Plotly (Radar Charts and Data Visualization)
- Machine Learning: Scikit-Learn (Random Forest Regressor), NumPy, Pandas
- Backend and Database: Python, SQLite3
- Integrations: Google Fit REST API via OAuth 2.0

Future Scope and Roadmap

- Smartwatch Direct Syncing: Direct wrist-wearable integration (via Zepp, Amazfit, or Wear OS APIs) for automatic, high-precision sleep tracking and active recovery metrics, eliminating manual sleep entry entirely.
- Long-Term Trend Predictive Modeling: Time-series performance forecasting to predict weekly burnout risks based on cumulative sleep debt and focus patterns.
- Automated Expense Categorization: Receipt OCR scanning and automated budget tracking.
- Customized Daily Schedules: Dynamic AI calendar generation based on daily energy scores and predicted peak focus hours.

How to Run Locally

1. Clone or download the repository.
2. Install dependencies:
   pip install -r requirements.txt
3. Launch the application:
   streamlit run app.py

"Note: To test the Google Fit API integration locally, generate your own credentials from the Google Cloud Console, save them as client_secret.json in the project root, and ensure the Google Fit API is enabled."
