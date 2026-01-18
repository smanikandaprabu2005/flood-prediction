import numpy as np
import pandas as pd
import tensorflow as tf

from sklearn.metrics import confusion_matrix, classification_report, accuracy_score

# =====================================
# 1. LOAD TRAINED MODEL
# =====================================
model = tf.keras.models.load_model("flood_lstm_binary_model.keras")
print("✅ Model loaded successfully")
# =====================================
# 2. LOAD DATA
# =====================================
df = pd.read_csv("flood_preprocessed.csv")

FEATURE_COLS = [
    "Rain_3day_sum",
    "Rain_7day_sum",
    "Rain_3day_avg",
    "Max_Normalized_River_Level",
    "Avg_Normalized_River_Level",
    "Max_River_Rise"
]

LABEL_COL = "Flood_Label"   # 0 = No Flood, 1 = Flood

X = df[FEATURE_COLS].values
y = df[LABEL_COL].values.astype(int)


# =====================================
# 3. CREATE LSTM SEQUENCES
# =====================================
TIME_STEPS = 7

def create_sequences(X, y, window):
    X_seq, y_seq = [], []
    for i in range(len(X) - window):
        X_seq.append(X[i:i + window])
        y_seq.append(y[i + window])
    return np.array(X_seq), np.array(y_seq)

X_seq, y_seq = create_sequences(X, y, TIME_STEPS)


# =====================================
# 4. DEFINE TEST SPLIT (LAST 40%)
# =====================================
TEST_RATIO = 0.40
test_start = int((1 - TEST_RATIO) * len(X_seq))

X_test = X_seq[test_start:]
y_test = y_seq[test_start:]

print("Test samples :", len(X_test))
print("Floods in test:", np.sum(y_test == 1))


# =====================================
# 5. MODEL PREDICTION
# =====================================
y_prob = model.predict(X_test).ravel()

# ⚠️ IMPORTANT:
# Threshold MUST be fixed (no tuning here)
THRESHOLD = 0.5

y_pred = (y_prob >= THRESHOLD).astype(int)


# =====================================
# 6. EVALUATION
# =====================================
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred, zero_division=0))

acc = accuracy_score(y_test, y_pred)
print("Accuracy:", acc)


# =====================================
# 7. OPTIONAL: SAVE PREDICTIONS
# =====================================
results = pd.DataFrame({
    "y_true": y_test,
    "y_prob": y_prob,
    "y_pred": y_pred
})

results.to_csv("flood_test_predictions.csv", index=False)
print("📁 Test predictions saved to flood_test_predictions.csv")
