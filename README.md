# Flood Prediction Web Application

A complete flood prediction system using LSTM machine learning model with real-time data scraping and interactive visualization.

## Features

- **LSTM Model**: Trained binary classification model for flood prediction
- **Real-time Data**: Scrapes water level data from India Water Resources website
- **Weather Integration**: Fetches rainfall data from Open-Meteo API
- **Interactive Map**: Leaflet-based India map with river station markers
- **Modern UI**: React frontend with Tailwind CSS
- **FastAPI Backend**: RESTful API with CORS support

## Architecture

### Backend (FastAPI)
- `/api/stations` - Get all river monitoring stations
- `/api/predict` - Make flood prediction using LSTM model

### Frontend (React)
- Interactive map with station markers
- Cascading dropdowns for location selection
- Real-time prediction results with charts
- Responsive design

## Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js 16+

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Install Playwright browsers:
```bash
python -m playwright install chromium
```

4. Start the backend server:
```bash
python server.py
```
Server will run on http://localhost:8001

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install Node dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```
Frontend will run on http://localhost:5173

## Model Details

### Input Features (Last 7 days)
- Rain_3day_sum: Sum of rainfall over last 3 days
- Rain_7day_sum: Sum of rainfall over last 7 days
- Rain_3day_avg: Average rainfall over last 3 days
- Max_Normalized_River_Level: Maximum normalized river level
- Avg_Normalized_River_Level: Average normalized river level
- Max_River_Rise: Maximum daily river level rise

### Output
- Binary classification: Flood (1) / No Flood (0)
- Probability score (0-1)
- Status: Safe/Warning/Danger

## Data Sources

1. **Rainfall Data**: Open-Meteo API (free, no API key required)
2. **Water Level Data**: Got from https://ffs.india-water.gov.in/
3. **Station Information**: Pre-loaded Excel file with 1645+ stations

## Technologies Used

- **Backend**: FastAPI, TensorFlow/Keras,Pandas
- **Frontend**: React, Leaflet, Recharts, Tailwind CSS
- **ML Model**: LSTM Neural Network
- **Data Processing**: Scikit-learn, NumPy

## API Endpoints

### GET /api/stations
Returns list of all monitoring stations with location data.

### POST /api/predict
Makes flood prediction for a location.
```json
{
  "state": "Maharashtra",
  "district": "Pune",
  "basin": "Krishna",
  "river": "Bhima"
}
```


## Report

This project is for educational and research purposes. Please respect the terms of service of data sources used.
     
Sequence shape: (1616, 7, 6)
Label shape   : (1616,)

================ FOLD 1 ================
Train samples: 808
Val samples  : 355
Floods in Val: 80
Class weights: {0: 0.6644736842105263, 1: 2.02}

Confusion Matrix:
[[257  18]
 [ 27  53]]

Classification Report:
              precision    recall  f1-score   support

           0       0.90      0.93      0.92       275
           1       0.75      0.66      0.70        80

    accuracy                           0.87       355
   macro avg       0.83      0.80      0.81       355
weighted avg       0.87      0.87      0.87       355


================ FOLD 2 ================
Train samples: 1163
Val samples  : 323
Floods in Val: 55
Class weights: {0: 0.6585503963759909, 1: 2.0767857142857142}

Confusion Matrix:
[[251  17]
 [  7  48]]

Classification Report:
              precision    recall  f1-score   support

           0       0.97      0.94      0.95       268
           1       0.74      0.87      0.80        55

    accuracy                           0.93       323
   macro avg       0.86      0.90      0.88       323
weighted avg       0.93      0.93      0.93       323


================ CV SUMMARY ================
Fold 1 → Acc: 0.873, Recall(Flood): 0.662
Fold 2 → Acc: 0.926, Recall(Flood): 0.873

MEAN CV METRICS
Accuracy      : 0.899
Recall(Flood) : 0.768

✅ Final Binary Flood LSTM model saved successfully