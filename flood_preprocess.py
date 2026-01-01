import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import joblib

# =====================================
# 1. LOAD DATA
# =====================================
df = pd.read_csv("flood_model_ready.csv")

# =====================================
# 2. DROP NaNs (safety)
# =====================================
df = df.dropna().reset_index(drop=True)

# =====================================
# 3. DEFINE COLUMNS
# =====================================
# Scale ONLY rainfall + river rise
scale_cols = [
    "Rain_3day_sum",
    "Rain_7day_sum",
    "Rain_3day_avg",
    "Max_River_Rise"
]

already_normalized = [
    "Max_Normalized_River_Level",
    "Avg_Normalized_River_Level"
]
label_col = "Flood_Label"

# =====================================
# 4. CLEAN Max_River_Rise (CRITICAL)
# =====================================
# Remove negative values (falling water is not flood risk)
df["Max_River_Rise"] = df["Max_River_Rise"].clip(lower=0)

# Cap extreme spikes (sensor / release artefacts)
upper = df["Max_River_Rise"].quantile(0.99)
df["Max_River_Rise"] = df["Max_River_Rise"].clip(0, upper)

# =====================================
# 5. SCALE FEATURES (LSTM REQUIRED)
# =====================================
scaler = MinMaxScaler()
df[scale_cols] = scaler.fit_transform(df[scale_cols])
feature_cols = scale_cols + already_normalized
X = df[feature_cols].values
y = df[label_col].values
# =====================================
# 6. CREATE FINAL DATAFRAME
# =====================================
df_scaled = pd.DataFrame(X, columns=feature_cols)
df_scaled[label_col] = y

# =====================================
# 7. SAVE OUTPUTS
# =====================================
df_scaled.to_csv("flood_preprocessed.csv", index=False)
joblib.dump(scaler, "flood_scaler.pkl")

print("✅ Flood preprocessing completed successfully")
print(df_scaled.head())
