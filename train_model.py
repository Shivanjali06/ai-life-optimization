import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

np.random.seed(42)
n_samples = 1500

sleep = np.random.uniform(4.0, 10.0, n_samples)
study = np.random.uniform(1.0, 10.0, n_samples)
phone = np.random.uniform(1.0, 9.0, n_samples)
exercise = np.random.choice([0, 1], size=n_samples, p=[0.4, 0.6])
expenses = np.random.uniform(50, 1000, n_samples)

score = (
    (study * 6.5) +
    (sleep * 4.0) -
    (phone * 5.0) +
    (exercise * 12.0) -
    (expenses * 0.015) +
    25
)
score = np.clip(score, 10, 100)

df = pd.DataFrame({
    'sleep': sleep,
    'study': study,
    'phone': phone,
    'exercise': exercise,
    'expenses': expenses,
    'score': score
})

X = df[['sleep', 'study', 'phone', 'exercise', 'expenses']]
y = df['score']

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

joblib.dump(model, 'productivity_model.pkl')
print("Model trained and saved as productivity_model.pkl")