import numpy as np
import pickle
from tensorflow import keras
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class FloodPredictor:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.model_path = Path(__file__).parent / "flood_lstm_binary_model.keras"
        self.scaler_path = Path(__file__).parent / "flood_scaler.pkl"
        
    def load_model(self):
        """Load the trained LSTM model and scaler"""
        try:
            logger.info(f"Loading model from {self.model_path}")
            self.model = keras.models.load_model(str(self.model_path))
            
            logger.info(f"Loading scaler from {self.scaler_path}")
            with open(self.scaler_path, 'rb') as f:
                self.scaler = pickle.load(f)
            
            logger.info("Model and scaler loaded successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            return False
    
    def prepare_features(self, rainfall_data: list, water_levels: list, 
                        warning_level: float, danger_level: float):
        """
        Prepare features for LSTM model
        
        Expected features (last 7 days):
        - Rain_3day_sum
        - Rain_7day_sum
        - Rain_3day_avg
        - Max_Normalized_River_Level
        - Avg_Normalized_River_Level
        - Max_River_Rise
        """
        try:
            # Ensure we have 7 days of rainfall data
            if len(rainfall_data) < 7:
                # Pad with zeros if needed
                rainfall_data = [0] * (7 - len(rainfall_data)) + rainfall_data
            
            rainfall_data = rainfall_data[-7:]  # Take last 7 days
            
            # Ensure we have water level data
            if len(water_levels) < 4:
                water_levels = water_levels + [water_levels[-1]] * (4 - len(water_levels))
            
            # Pad water levels to 7 days
            water_levels = water_levels + [water_levels[-1]] * (7 - len(water_levels))
            water_levels = water_levels[-7:]
            
            # Calculate features for each of the 7 days
            features = []
            
            for i in range(7):
                # Rain_3day_sum: sum of last 3 days rainfall up to day i
                rain_3day_sum = sum(rainfall_data[max(0, i-2):i+1])
                
                # Rain_7day_sum: sum of all rainfall up to day i
                rain_7day_sum = sum(rainfall_data[:i+1])
                
                # Rain_3day_avg: average of last 3 days
                rain_3day_avg = rain_3day_sum / min(3, i+1)
                
                # Normalize water levels
                normalized_level = water_levels[i] / danger_level if danger_level > 0 else 0.5
                
                # Max normalized river level (up to day i)
                max_normalized = max(water_levels[:i+1]) / danger_level if danger_level > 0 else 0.5
                
                # Avg normalized river level (up to day i)
                avg_normalized = np.mean(water_levels[:i+1]) / danger_level if danger_level > 0 else 0.5
                
                # Max river rise (maximum change in consecutive days up to day i)
                if i > 0:
                    rises = [water_levels[j] - water_levels[j-1] for j in range(1, i+1)]
                    max_rise = max(rises) if rises else 0
                else:
                    max_rise = 0
                
                features.append([
                    rain_3day_sum,
                    rain_7day_sum,
                    rain_3day_avg,
                    max_normalized,
                    avg_normalized,
                    max_rise
                ])
            
            return np.array(features)
            
        except Exception as e:
            logger.error(f"Feature preparation failed: {str(e)}")
            raise
    
    def predict(self, rainfall_data: list, water_levels: list, 
               warning_level: float, danger_level: float):
        """
        Make flood prediction
        
        Returns:
            dict with prediction, probability, and status
        """
        try:
            if self.model is None or self.scaler is None:
                if not self.load_model():
                    raise Exception("Model not loaded")
            
            # Prepare features
            features = self.prepare_features(rainfall_data, water_levels, 
                                           warning_level, danger_level)
            
            # Scale features
            features_scaled = self.scaler.transform(features)
            
            # Reshape for LSTM: (1, 7, 6) - 1 sample, 7 timesteps, 6 features
            features_reshaped = features_scaled.reshape(1, 7, 6)
            
            # Make prediction
            prediction = self.model.predict(features_reshaped, verbose=0)
            flood_probability = float(prediction[0][0])
            
            # Determine status
            if flood_probability >= 0.5:
                prediction_label = "Flood"
                if flood_probability >= 0.8:
                    status = "Danger"
                else:
                    status = "Warning"
            else:
                prediction_label = "No Flood"
                status = "Safe"
            
            # Additional checks based on water levels
            current_level = water_levels[-1] if water_levels else 0
            if current_level >= danger_level:
                status = "Danger"
                prediction_label = "Flood"
                flood_probability = max(flood_probability, 0.85)
            elif current_level >= warning_level:
                if status == "Safe":
                    status = "Warning"
            
            return {
                "prediction": prediction_label,
                "probability": round(flood_probability, 3),
                "confidence": round(abs(flood_probability - 0.5) * 2, 3),
                "status": status,
                "current_water_level": current_level,
                "warning_level": warning_level,
                "danger_level": danger_level
            }
            
        except Exception as e:
            logger.error(f"Prediction failed: {str(e)}")
            raise
