import joblib
import numpy as np

def load_model():
    """Loads the pre-trained Random Forest model."""
    try:
        return joblib.load('productivity_model.pkl')
    except Exception:
        return None

model = load_model()

def predict_productivity(features):
    """
    Predicts productivity score using the ML model or a fallback formula.
    features: [sleep_hours, step_count, study_hours, screen_time, expenses]
    """
    if model is None:
        sleep, steps, study, phone, exp = features
        # Fallback heuristic calculation normalized across features
        val = (study * 6.5) + (sleep * 4.0) + (min(steps / 10000, 1.0) * 15) - (phone * 4.0) - (exp * 0.015) + 25
        return round(float(np.clip(val, 10, 100)), 1)
    
    features_arr = np.array(features).reshape(1, -1)
    score = model.predict(features_arr)[0]
    return round(float(np.clip(score, 0, 100)), 1)

def get_performance_insights(features):
    """
    Calculates key penalty metrics to identify the primary bottleneck.
    features: [sleep_hours, step_count, study_hours, screen_time, expenses]
    """
    sleep, steps, study, phone, exp = features
    
    penalties = {
        "Sleep Deprivation": max(0, 7.5 - sleep) * 12,
        "Excessive Screen Time": max(0, phone - 3.0) * 10,
        "Low Focus Volume": max(0, 4.0 - study) * 8,
        "Low Physical Activity": max(0, 8000 - steps) * 0.005,
        "Unplanned Financial Outlay": max(0, exp - 400) * 0.05
    }
    
    bottleneck = max(penalties, key=penalties.get)
    if penalties[bottleneck] == 0:
        bottleneck = "None Identified (Optimal Routine)"
        
    return bottleneck