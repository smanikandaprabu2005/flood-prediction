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
- `/api/scrape-water-level` - Scrape water level data from government site
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
- Playwright browsers

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
2. **Water Level Data**: Scraped from https://ffs.india-water.gov.in/
3. **Station Information**: Pre-loaded Excel file with 1645+ stations

## Technologies Used

- **Backend**: FastAPI, TensorFlow/Keras, Playwright, Pandas
- **Frontend**: React, Leaflet, Recharts, Tailwind CSS
- **ML Model**: LSTM Neural Network
- **Data Processing**: Scikit-learn, NumPy

## API Endpoints

### GET /api/stations
Returns list of all monitoring stations with location data.

### POST /api/scrape-water-level
Scrapes water level data for a specific station.
```json
{
  "state": "Maharashtra",
  "district": "Pune",
  "basin": "Krishna",
  "river": "Bhima"
}
```

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

## Development Notes

- The scraper uses Playwright for robust web scraping
- Data is cached for 1 hour to reduce server load
- Model predictions include confidence scores
- Frontend uses Vite for fast development

## License

This project is for educational and research purposes. Please respect the terms of service of data sources used.
Epoch 1/50
28/28 ━━━━━━━━━━━━━━━━━━━━ 4s 28ms/step - accuracy: 0.5755 - loss: 1.4325 - val_accuracy: 0.8889 - val_loss: 0.5234
Epoch 2/50
28/28 ━━━━━━━━━━━━━━━━━━━━ 0s 11ms/step - accuracy: 0.5011 - loss: 0.7816 - val_accuracy: 0.9691 - val_loss: 0.3237
Epoch 3/50
28/28 ━━━━━━━━━━━━━━━━━━━━ 0s 11ms/step - accuracy: 0.6610 - loss: 0.6117 - val_accuracy: 1.0000 - val_loss: 0.1941
Epoch 4/50
28/28 ━━━━━━━━━━━━━━━━━━━━ 0s 11ms/step - accuracy: 0.8333 - loss: 0.4449 - val_accuracy: 0.9877 - val_loss: 0.1055
Epoch 5/50
28/28 ━━━━━━━━━━━━━━━━━━━━ 0s 11ms/step - accuracy: 0.8851 - loss: 0.3054 - val_accuracy: 0.9753 - val_loss: 0.0672
Epoch 6/50
28/28 ━━━━━━━━━━━━━━━━━━━━ 0s 11ms/step - accuracy: 0.8694 - loss: 0.2752 - val_accuracy: 0.9877 - val_loss: 0.0448
Epoch 7/50
28/28 ━━━━━━━━━━━━━━━━━━━━ 0s 12ms/step - accuracy: 0.9718 - loss: 0.1170 - val_accuracy: 0.9877 - val_loss: 0.0320
Epoch 8/50
28/28 ━━━━━━━━━━━━━━━━━━━━ 1s 11ms/step - accuracy: 0.9741 - loss: 0.0892 - val_accuracy: 0.8889 - val_loss: 0.2438
Epoch 9/50
28/28 ━━━━━━━━━━━━━━━━━━━━ 0s 10ms/step - accuracy: 0.9223 - loss: 0.3175 - val_accuracy: 0.9259 - val_loss: 0.2244
Epoch 10/50
28/28 ━━━━━━━━━━━━━━━━━━━━ 0s 10ms/step - accuracy: 0.7297 - loss: 0.6274 - val_accuracy: 0.9938 - val_loss: 0.0399
Epoch 11/50
28/28 ━━━━━━━━━━━━━━━━━━━━ 0s 10ms/step - accuracy: 0.9268 - loss: 0.2155 - val_accuracy: 0.9877 - val_loss: 0.0319
Epoch 12/50
28/28 ━━━━━━━━━━━━━━━━━━━━ 0s 11ms/step - accuracy: 0.9155 - loss: 0.1532 - val_accuracy: 0.9938 - val_loss: 0.0354
Epoch 13/50
28/28 ━━━━━━━━━━━━━━━━━━━━ 0s 11ms/step - accuracy: 0.9876 - loss: 0.0988 - val_accuracy: 0.9877 - val_loss: 0.0240
Epoch 14/50
28/28 ━━━━━━━━━━━━━━━━━━━━ 0s 11ms/step - accuracy: 0.9437 - loss: 0.1239 - val_accuracy: 0.9938 - val_loss: 0.0212
Epoch 15/50
28/28 ━━━━━━━━━━━━━━━━━━━━ 0s 11ms/step - accuracy: 0.9910 - loss: 0.0636 - val_accuracy: 0.9938 - val_loss: 0.0144
Epoch 16/50
28/28 ━━━━━━━━━━━━━━━━━━━━ 0s 10ms/step - accuracy: 0.9347 - loss: 0.1603 - val_accuracy: 0.9938 - val_loss: 0.0131
Epoch 17/50
28/28 ━━━━━━━━━━━━━━━━━━━━ 0s 10ms/step - accuracy: 0.9651 - loss: 0.0888 - val_accuracy: 0.9938 - val_loss: 0.0231
Epoch 18/50
28/28 ━━━━━━━━━━━━━━━━━━━━ 0s 11ms/step - accuracy: 0.9899 - loss: 0.0515 - val_accuracy: 0.9877 - val_loss: 0.0265
Epoch 19/50
28/28 ━━━━━━━━━━━━━━━━━━━━ 0s 10ms/step - accuracy: 0.9944 - loss: 0.0428 - val_accuracy: 0.9877 - val_loss: 0.0349
Epoch 20/50
28/28 ━━━━━━━━━━━━━━━━━━━━ 0s 11ms/step - accuracy: 0.9966 - loss: 0.0389 - val_accuracy: 0.9877 - val_loss: 0.0265
Epoch 21/50
28/28 ━━━━━━━━━━━━━━━━━━━━ 0s 11ms/step - accuracy: 0.9752 - loss: 0.0646 - val_accuracy: 0.9568 - val_loss: 0.1110
6/6 ━━━━━━━━━━━━━━━━━━━━ 1s 69ms/step 

Confusion Matrix:
[[129  13]
 [  0  20]]

Classification Report:
              precision    recall  f1-score   support

           0       1.00      0.91      0.95       142
           1       0.61      1.00      0.75        20

    accuracy                           0.92       162
   macro avg       0.80      0.95      0.85       162
weighted avg       0.95      0.92      0.93       162


================ FOLD 2 ================
Train samples: 1050
Val samples  : 323
Floods in Val: 45
Class weights: {0: 0.6489493201483313, 1: 2.1784232365145226}
Epoch 1/50
33/33 ━━━━━━━━━━━━━━━━━━━━ 4s 25ms/step - accuracy: 0.7629 - loss: 1.6763 - val_accuracy: 0.8607 - val_loss: 0.5001
Epoch 2/50
33/33 ━━━━━━━━━━━━━━━━━━━━ 0s 12ms/step - accuracy: 0.7124 - loss: 0.6485 - val_accuracy: 0.8607 - val_loss: 0.4763
Epoch 3/50
33/33 ━━━━━━━━━━━━━━━━━━━━ 0s 12ms/step - accuracy: 0.8114 - loss: 0.4328 - val_accuracy: 0.6316 - val_loss: 0.6204
Epoch 4/50
33/33 ━━━━━━━━━━━━━━━━━━━━ 0s 11ms/step - accuracy: 0.9048 - loss: 0.2408 - val_accuracy: 0.5418 - val_loss: 1.1968
Epoch 5/50
33/33 ━━━━━━━━━━━━━━━━━━━━ 0s 10ms/step - accuracy: 0.8971 - loss: 0.2492 - val_accuracy: 0.4644 - val_loss: 1.7962
Epoch 6/50
33/33 ━━━━━━━━━━━━━━━━━━━━ 1s 13ms/step - accuracy: 0.8571 - loss: 0.3058 - val_accuracy: 0.7492 - val_loss: 0.4081
Epoch 7/50
33/33 ━━━━━━━━━━━━━━━━━━━━ 0s 10ms/step - accuracy: 0.9714 - loss: 0.0888 - val_accuracy: 0.6997 - val_loss: 0.8891
Epoch 8/50
33/33 ━━━━━━━━━━━━━━━━━━━━ 0s 12ms/step - accuracy: 0.9867 - loss: 0.0609 - val_accuracy: 0.6935 - val_loss: 1.0619
Epoch 9/50
33/33 ━━━━━━━━━━━━━━━━━━━━ 0s 13ms/step - accuracy: 0.9810 - loss: 0.0584 - val_accuracy: 0.7399 - val_loss: 1.0141
Epoch 10/50
33/33 ━━━━━━━━━━━━━━━━━━━━ 0s 13ms/step - accuracy: 0.9829 - loss: 0.0657 - val_accuracy: 0.6192 - val_loss: 1.7216
Epoch 11/50
33/33 ━━━━━━━━━━━━━━━━━━━━ 0s 11ms/step - accuracy: 0.9571 - loss: 0.1404 - val_accuracy: 0.3715 - val_loss: 2.9391
11/11 ━━━━━━━━━━━━━━━━━━━━ 1s 43ms/step 

Confusion Matrix:
[[257  21]
 [  1  44]]

Classification Report:
              precision    recall  f1-score   support

           0       1.00      0.92      0.96       278
           1       0.68      0.98      0.80        45

    accuracy                           0.93       323
   macro avg       0.84      0.95      0.88       323
weighted avg       0.95      0.93      0.94       323


================ CV SUMMARY ================
Fold 1 → Acc: 0.920, Recall(Flood): 1.000
Fold 2 → Acc: 0.932, Recall(Flood): 0.978

MEAN CV METRICS
Accuracy      : 0.926
Recall(Flood) : 0.989
Epoch 1/50
51/51 ━━━━━━━━━━━━━━━━━━━━ 0s 8ms/step - accuracy: 0.7421 - loss: 1.3898C:\Users\smani\AppData\Local\Programs\Python\Python310\lib\site-packages\keras\src\callbacks\early_stopping.py:99: UserWarning: Early stopping conditioned on metric `val_loss` which is not available. Available metrics are: accuracy,loss 
  current = self.get_monitor_value(logs)
51/51 ━━━━━━━━━━━━━━━━━━━━ 5s 9ms/step - accuracy: 0.7506 - loss: 1.1535
Epoch 2/50
51/51 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - accuracy: 0.7153 - loss: 0.6862 
Epoch 3/50
51/51 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - accuracy: 0.7624 - loss: 0.5038 
Epoch 4/50
51/51 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - accuracy: 0.8385 - loss: 0.3708 
Epoch 5/50
51/51 ━━━━━━━━━━━━━━━━━━━━ 1s 9ms/step - accuracy: 0.8608 - loss: 0.2968 
Epoch 6/50
51/51 ━━━━━━━━━━━━━━━━━━━━ 0s 8ms/step - accuracy: 0.9220 - loss: 0.2087 
Epoch 7/50
51/51 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - accuracy: 0.8113 - loss: 0.3915 
Epoch 8/50
51/51 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - accuracy: 0.8626 - loss: 0.2678 
Epoch 9/50
51/51 ━━━━━━━━━━━━━━━━━━━━ 0s 8ms/step - accuracy: 0.8967 - loss: 0.2468 
Epoch 10/50
51/51 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - accuracy: 0.9270 - loss: 0.1805 
Epoch 11/50
51/51 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - accuracy: 0.8960 - loss: 0.2603 
Epoch 12/50
51/51 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - accuracy: 0.8465 - loss: 0.2511 
Epoch 13/50
51/51 ━━━━━━━━━━━━━━━━━━━━ 1s 7ms/step - accuracy: 0.9288 - loss: 0.1818   
Epoch 14/50
51/51 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - accuracy: 0.9226 - loss: 0.1970 
Epoch 15/50
51/51 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - accuracy: 0.9356 - loss: 0.1496 
Epoch 16/50
51/51 ━━━━━━━━━━━━━━━━━━━━ 0s 8ms/step - accuracy: 0.9134 - loss: 0.2179 
Epoch 17/50
51/51 ━━━━━━━━━━━━━━━━━━━━ 1s 9ms/step - accuracy: 0.9350 - loss: 0.1337 
Epoch 18/50
51/51 ━━━━━━━━━━━━━━━━━━━━ 0s 8ms/step - accuracy: 0.8874 - loss: 0.2781 
Epoch 19/50
51/51 ━━━━━━━━━━━━━━━━━━━━ 0s 8ms/step - accuracy: 0.8552 - loss: 0.2305 
Epoch 20/50
51/51 ━━━━━━━━━━━━━━━━━━━━ 0s 8ms/step - accuracy: 0.9394 - loss: 0.1587 
Epoch 21/50
51/51 ━━━━━━━━━━━━━━━━━━━━ 0s 8ms/step - accuracy: 0.9127 - loss: 0.2162 
Epoch 22/50
51/51 ━━━━━━━━━━━━━━━━━━━━ 1s 10ms/step - accuracy: 0.9325 - loss: 0.1369
Epoch 23/50
51/51 ━━━━━━━━━━━━━━━━━━━━ 1s 9ms/step - accuracy: 0.9276 - loss: 0.1652   
Epoch 24/50
51/51 ━━━━━━━━━━━━━━━━━━━━ 0s 8ms/step - accuracy: 0.9270 - loss: 0.1642 
Epoch 25/50
51/51 ━━━━━━━━━━━━━━━━━━━━ 0s 8ms/step - accuracy: 0.9208 - loss: 0.1665 
Epoch 26/50
51/51 ━━━━━━━━━━━━━━━━━━━━ 0s 8ms/step - accuracy: 0.9468 - loss: 0.1184 
Epoch 27/50
51/51 ━━━━━━━━━━━━━━━━━━━━ 0s 8ms/step - accuracy: 0.9703 - loss: 0.0870 
Epoch 28/50
51/51 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - accuracy: 0.9152 - loss: 0.2292 
Epoch 29/50
51/51 ━━━━━━━━━━━━━━━━━━━━ 0s 8ms/step - accuracy: 0.9561 - loss: 0.1264 
Epoch 30/50
51/51 ━━━━━━━━━━━━━━━━━━━━ 0s 8ms/step - accuracy: 0.8880 - loss: 0.2528 
Epoch 31/50
51/51 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - accuracy: 0.8979 - loss: 0.1472 
Epoch 32/50
51/51 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - accuracy: 0.9053 - loss: 0.2196 
Epoch 33/50
51/51 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - accuracy: 0.9332 - loss: 0.1278 
Epoch 34/50
51/51 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - accuracy: 0.9251 - loss: 0.1610 
Epoch 35/50
51/51 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - accuracy: 0.9660 - loss: 0.1028 
Epoch 36/50
51/51 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - accuracy: 0.9573 - loss: 0.0970 
Epoch 37/50
51/51 ━━━━━━━━━━━━━━━━━━━━ 0s 8ms/step - accuracy: 0.9158 - loss: 0.1900 
Epoch 38/50
51/51 ━━━━━━━━━━━━━━━━━━━━ 0s 7ms/step - accuracy: 0.9684 - loss: 0.0958 
Epoch 39/50
51/51 ━━━━━━━━━━━━━━━━━━━━ 0s 8ms/step - accuracy: 0.9783 - loss: 0.0829 
Epoch 40/50
51/51 ━━━━━━━━━━━━━━━━━━━━ 1s 9ms/step - accuracy: 0.9623 - loss: 0.0795   
Epoch 41/50
51/51 ━━━━━━━━━━━━━━━━━━━━ 0s 9ms/step - accuracy: 0.8632 - loss: 0.3825 
Epoch 42/50
51/51 ━━━━━━━━━━━━━━━━━━━━ 0s 9ms/step - accuracy: 0.8521 - loss: 0.2247 
Epoch 43/50
51/51 ━━━━━━━━━━━━━━━━━━━━ 0s 8ms/step - accuracy: 0.8886 - loss: 0.2530 
Epoch 44/50
51/51 ━━━━━━━━━━━━━━━━━━━━ 0s 8ms/step - accuracy: 0.9517 - loss: 0.1272 
Epoch 45/50
51/51 ━━━━━━━━━━━━━━━━━━━━ 0s 8ms/step - accuracy: 0.9412 - loss: 0.1322 
Epoch 46/50
51/51 ━━━━━━━━━━━━━━━━━━━━ 0s 8ms/step - accuracy: 0.8861 - loss: 0.2512 
Epoch 47/50
51/51 ━━━━━━━━━━━━━━━━━━━━ 0s 8ms/step - accuracy: 0.9090 - loss: 0.1353 
Epoch 48/50
51/51 ━━━━━━━━━━━━━━━━━━━━ 0s 8ms/step - accuracy: 0.9462 - loss: 0.1148 
Epoch 49/50
51/51 ━━━━━━━━━━━━━━━━━━━━ 1s 9ms/step - accuracy: 0.9567 - loss: 0.0955 
Epoch 50/50
51/51 ━━━━━━━━━━━━━━━━━━━━ 1s 9ms/step - accuracy: 0.9530 - loss: 0.1055 

✅ Final Binary Flood LSTM model saved successfully
PS D:\pers\disaster> 