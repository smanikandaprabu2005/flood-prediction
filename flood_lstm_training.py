
import numpy as np
import pandas as pd
import tensorflow as tf

from sklearn.utils.class_weight import compute_class_weight
from sklearn.metrics import confusion_matrix, classification_report, recall_score

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, LayerNormalization, Input
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping

# =====================================
# 0. MODEL BUILDER (BINARY)
# =====================================
def build_lstm_model(time_steps, n_features):
    model = Sequential([
        Input(shape=(time_steps, n_features)),

        LSTM(64, return_sequences=True),
        LayerNormalization(),
        Dropout(0.3),

        LSTM(32),
        LayerNormalization(),
        Dropout(0.3),

        Dense(32, activation="relu"),
        Dense(1, activation="sigmoid")   # ✅ Binary output
    ])

    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss="binary_crossentropy",       # ✅ Correct loss
        metrics=[
            tf.keras.metrics.AUC(name="auc"),        # main quality signal
            tf.keras.metrics.Precision(name="precision"),
            tf.keras.metrics.Recall(name="recall")
        ]
    )
    return model


# =====================================
# 1. LOAD DATA
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
# 2. CREATE LSTM SEQUENCES
# =====================================
TIME_STEPS = 7

def create_sequences(X, y, window):
    X_seq, y_seq = [], []
    for i in range(len(X) - window):
        X_seq.append(X[i:i + window])
        y_seq.append(y[i + window])
    return np.array(X_seq), np.array(y_seq)

X_seq, y_seq = create_sequences(X, y, TIME_STEPS)

print("Sequence shape:", X_seq.shape)
print("Label shape   :", y_seq.shape)


# =====================================
# 3. WALK-FORWARD TIME SERIES CV
# =====================================
N_FEATURES = X_seq.shape[2]

# (train %, val %)
"""folds = [
    (0.55, 0.65),
    (0.65, 0.85)
]"""
folds = [
    (0.5, 0.71),
    (0.71, 0.95)
]

cv_results = []


# =====================================
# 4. CV TRAINING LOOP
# =====================================
for fold_id, (train_end, val_end) in enumerate(folds, start=1):
    print(f"\n================ FOLD {fold_id} ================")

    train_idx = int(train_end * len(X_seq))
    val_idx   = int(val_end * len(X_seq))

    X_train, X_val = X_seq[:train_idx], X_seq[train_idx:val_idx]
    y_train, y_val = y_seq[:train_idx], y_seq[train_idx:val_idx]

    print("Train samples:", len(X_train))
    print("Val samples  :", len(X_val))
    print("Floods in Val:", np.sum(y_val == 1))

    # ---------------------------------
    # CLASS WEIGHTS (TRAIN ONLY)
    # ---------------------------------
    classes = np.unique(y_train)
    weights = compute_class_weight(
        class_weight="balanced",
        classes=classes,
        y=y_train
    )
    class_weight = dict(zip(classes, weights))
    print("Class weights:", class_weight)

    # ---------------------------------
    # BUILD & TRAIN MODEL
    # ---------------------------------
    model = build_lstm_model(TIME_STEPS, N_FEATURES)

    early_stop = EarlyStopping(
        monitor="val_loss",
        patience=5,
        restore_best_weights=True,
       # mode=max
    )

    model.fit(
        X_train,
        y_train,
        validation_data=(X_val, y_val),
        epochs=50,
        batch_size=32,
        class_weight=class_weight,
        shuffle=False,              # 🚨 REQUIRED for time series
        callbacks=[early_stop],
        verbose=1
    )

    # ---------------------------------
    # EVALUATION
    # ---------------------------------
    y_prob = model.predict(X_val).ravel()
    #y_pred = (y_prob >= 0.4).astype(int)   # ✅ Threshold tuned for recall
    threshold = np.percentile(y_prob, 80)
    y_pred = (y_prob >= threshold).astype(int)

    print("\nConfusion Matrix:")
    print(confusion_matrix(y_val, y_pred))

    print("\nClassification Report:")
    print(classification_report(y_val, y_pred, zero_division=0))

    recall_flood = recall_score(
        y_val, y_pred,
        pos_label=1,
        zero_division=0
    )

    acc = np.mean(y_pred == y_val)

    cv_results.append({
        "fold": fold_id,
        "accuracy": acc,
        "recall_flood": recall_flood
    })


# =====================================
# 5. CV SUMMARY
# =====================================
print("\n================ CV SUMMARY ================")

for r in cv_results:
    print(
        f"Fold {r['fold']} → "
        f"Acc: {r['accuracy']:.3f}, "
        f"Recall(Flood): {r['recall_flood']:.3f}"
    )

print("\nMEAN CV METRICS")
print(f"Accuracy      : {np.mean([r['accuracy'] for r in cv_results]):.3f}")
print(f"Recall(Flood) : {np.mean([r['recall_flood'] for r in cv_results]):.3f}")


# =====================================
# 6. TRAIN FINAL MODEL (2015–2019)
# =====================================
final_model = build_lstm_model(TIME_STEPS, N_FEATURES)

final_model.fit(
    X_seq,
    y_seq,
    epochs=50,
    batch_size=32,
    class_weight=class_weight,
    shuffle=False,
    callbacks=[early_stop],
    verbose=1
)

final_model.save("flood_lstm_binary_model.keras")
print("\n✅ Final Binary Flood LSTM model saved successfully")
