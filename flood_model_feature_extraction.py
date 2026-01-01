import pandas as pd
import numpy as np

# -----------------------------
# 1. LOAD DATA
# -----------------------------
df = pd.read_csv("flood,cyclone_data.csv")

# Parse date
df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)

# Sort by time (VERY IMPORTANT)
df = df.sort_values("Date").reset_index(drop=True)

# -----------------------------
# 2. KEEP ONLY REQUIRED COLUMNS
# -----------------------------
river_cols = ["POONDI", "CHOLAVARAM", "REDHILLS", "CHEMBARAMBAKKAM"]

df = df[["Date", "Rainfall"] + river_cols]

# -----------------------------
# 3. RAINFALL FEATURES (CAUSE)
# -----------------------------
df["Rain_3day_sum"] = df["Rainfall"].rolling(window=3).sum()
df["Rain_7day_sum"] = df["Rainfall"].rolling(window=7).sum()
df["Rain_3day_avg"] = df["Rainfall"].rolling(window=3).mean()

# -----------------------------
# 4. NORMALIZE RIVER LEVELS
# (makes model work on other states)
# -----------------------------
for col in river_cols:
    max_level = df[col].max()
    df[f"{col}_norm"] = df[col] / max_level

# -----------------------------
# 5. RATE OF RISE (DANGER SIGNAL)
# -----------------------------
for col in river_cols:
    df[f"{col}_delta"] = df[col].diff()

# -----------------------------
# 6. AGGREGATE RIVER BEHAVIOR
# (REMOVE river identity)
# -----------------------------
norm_cols = [f"{c}_norm" for c in river_cols]
delta_cols = [f"{c}_delta" for c in river_cols]

df["Max_Normalized_River_Level"] = df[norm_cols].max(axis=1)
df["Avg_Normalized_River_Level"] = df[norm_cols].mean(axis=1)
df["Max_River_Rise"] = df[delta_cols].max(axis=1)

# -----------------------------
# 7. LABEL CREATION (TARGET)
# -----------------------------
def create_flood_label(row):
    level = row["Max_Normalized_River_Level"]
    if level >= 0.60:
        return 1   # Low Risk
    else:
        return 0   # No Flood

df["Flood_Label"] = df.apply(create_flood_label, axis=1)

# -----------------------------
# 8. FINAL MODEL DATASET
# -----------------------------
final_features = [
    "Rain_3day_sum",
    "Rain_7day_sum",
    "Rain_3day_avg",
    "Max_Normalized_River_Level",
    "Avg_Normalized_River_Level",
    "Max_River_Rise",
    "Flood_Label"
]

final_df = df[final_features]

# Drop rows with NaNs (due to rolling windows)
final_df = final_df.dropna().reset_index(drop=True)

# -----------------------------
# 9. SAVE CLEAN DATASET
# -----------------------------
final_df.to_csv("flood_model_ready.csv", index=False)

print("✅ Feature engineering & labeling completed")
print(final_df.head())
