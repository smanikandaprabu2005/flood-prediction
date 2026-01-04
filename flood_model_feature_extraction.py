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
# 4. BANDED NORMALIZATION FOR RIVER LEVELS
# (prevents sigmoid saturation and reduces bias)
# -----------------------------
def normalize_water_level_banded(level, warning_level, danger_level):
    """
    Banded normalization to prevent sigmoid saturation.
    Maps water levels to 0-1 range with safe/warning/danger zones.
    """
    if level <= warning_level:
        # Safe to warning zone: 0.0 to 0.7
        if warning_level <= 0:
            return 0.0
        normalized = (level / warning_level) * 0.7
    else:
        # Warning to danger zone: 0.7 to 1.0
        danger_range = danger_level - warning_level
        if danger_range <= 0:
            return 0.7
        warning_to_danger_ratio = (level - warning_level) / danger_range
        normalized = 0.7 + (warning_to_danger_ratio * 0.3)

    # Cap at 0.95 to prevent sigmoid saturation
    return min(normalized, 0.95)

# Use Chennai reservoir thresholds (approximate for training data)
WARNING_LEVEL = 0.7  # 70% of max capacity
DANGER_LEVEL = 0.85  # 85% of max capacity

for col in river_cols:
    max_level = df[col].max()
    # Convert max-normalized back to absolute, then apply banded normalization
    df[f"{col}_norm"] = df[col].apply(lambda x: normalize_water_level_banded(x, WARNING_LEVEL * max_level, DANGER_LEVEL * max_level))

# -----------------------------
# 5. RATE OF RISE (DANGER SIGNAL)
# -----------------------------
for col in river_cols:
    df[f"{col}_delta"] = df[col].diff()

# -----------------------------
# 6. AGGREGATE RIVER BEHAVIOR WITH REDUCED DOMINANCE
# (REMOVE river identity and reduce bias)
# -----------------------------
norm_cols = [f"{c}_norm" for c in river_cols]
delta_cols = [f"{c}_delta" for c in river_cols]

df["Max_Normalized_River_Level"] = df[norm_cols].max(axis=1) * 0.8  # Reduce dominance
df["Avg_Normalized_River_Level"] = df[norm_cols].mean(axis=1) * 0.8  # Reduce dominance
df["Max_River_Rise"] = df[delta_cols].max(axis=1)


# -----------------------------
# 8. FINAL MODEL DATASET
# -----------------------------
final_features = [
    "Rain_3day_sum",
    "Rain_7day_sum",
    "Rain_3day_avg",
    "Max_Normalized_River_Level",
    "Avg_Normalized_River_Level",
    "Max_River_Rise"  # Use normalized rise
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
