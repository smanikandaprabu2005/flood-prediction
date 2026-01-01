from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
import os
import logging
from pathlib import Path
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd

from scraper import RiverDataScraper
from model_inference import FloodPredictor
from utils import WeatherAPI

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Create the main app
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize components
scraper = RiverDataScraper()
predictor = FloodPredictor()
weather_api = WeatherAPI()

# Load stations data
STATIONS_FILE = ROOT_DIR / "stations.xlsx"
stations_df = None

try:
    stations_df = pd.read_excel(STATIONS_FILE)
    logger.info(f"Loaded {len(stations_df)} stations")
except Exception as e:
    logger.error(f"Failed to load stations data: {e}")

# Load model at startup
predictor.load_model()

# Define Models
class StationInfo(BaseModel):
    station_name: str
    state: str
    district: str
    basin: str
    river: str
    latitude: float
    longitude: float
    type: str

class PredictionRequest(BaseModel):
    state: str
    district: str
    basin: str
    river: str
    station_name: Optional[str] = None

class PredictionResponse(BaseModel):
    prediction: str
    probability: float
    confidence: float
    status: str
    current_water_level: float
    warning_level: float
    danger_level: float
    rainfall_data: List[float]
    water_levels: List[float]
    station_info: dict

@api_router.get("/")
async def root():
    return {"message": "FloodWatch India API", "version": "1.0"}

@api_router.get("/stations")
async def get_stations():
    """
    Get all stations data with filter options
    """
    if stations_df is None:
        raise HTTPException(status_code=500, detail="Stations data not loaded")
    
    # Get unique values for dropdowns
    states = sorted(stations_df['State name'].unique().tolist())
    
    # Get all stations as list
    stations = []
    for _, row in stations_df.iterrows():
        stations.append({
            "station_name": row['Station Name'],
            "state": row['State name'],
            "district": row['District / Town'],
            "basin": row['Basin Name'],
            "river": row['River Name'],
            "latitude": float(row['Latitude']),
            "longitude": float(row['longitude']),
            "type": row['Type Of Site']
        })
    
    return {
        "states": states,
        "stations": stations,
        "total": len(stations)
    }

@api_router.get("/stations/filters")
async def get_filter_options(state: Optional[str] = None, 
                             district: Optional[str] = None,
                             basin: Optional[str] = None):
    """
    Get cascading filter options based on selections
    """
    if stations_df is None:
        raise HTTPException(status_code=500, detail="Stations data not loaded")
    
    filtered_df = stations_df.copy()
    
    if state:
        filtered_df = filtered_df[filtered_df['State name'] == state]
    if district:
        filtered_df = filtered_df[filtered_df['District / Town'] == district]
    if basin:
        filtered_df = filtered_df[filtered_df['Basin Name'] == basin]
    
    return {
        "districts": sorted(filtered_df['District / Town'].unique().tolist()) if state else [],
        "basins": sorted(filtered_df['Basin Name'].unique().tolist()) if district else [],
        "rivers": sorted(filtered_df['River Name'].unique().tolist()) if basin else [],
        "stations": filtered_df['Station Name'].unique().tolist()
    }

@api_router.post("/scrape-water-level")
async def scrape_water_level(request: PredictionRequest):
    """
    Scrape water level data for a specific location
    """
    try:
        logger.info(f"Scraping water level for {request.state}, {request.river}")
        
        data = await scraper.scrape_water_level(
            request.state,
            request.district,
            request.basin,
            request.river
        )
        
        return data
        
    except Exception as e:
        logger.error(f"Scraping failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Scraping failed: {str(e)}")

@api_router.post("/predict")
async def predict_flood(request: PredictionRequest):
    """
    Main prediction endpoint - combines rainfall, water level, and makes prediction
    """
    try:
        # Get station info
        if stations_df is None:
            raise HTTPException(status_code=500, detail="Stations data not loaded")
        
        station_row = stations_df[
            (stations_df['State name'] == request.state) &
            (stations_df['River Name'] == request.river)
        ]
        
        if station_row.empty:
            raise HTTPException(status_code=404, detail="Station not found")
        
        station = station_row.iloc[0]
        latitude = float(station['Latitude'])
        longitude = float(station['longitude'])
        
        logger.info(f"Predicting flood for {station['Station Name']}")
        
        # Fetch rainfall data (last 7 days)
        logger.info("Fetching rainfall data...")
        rainfall_data = await weather_api.get_rainfall_data(latitude, longitude, days=7)
        
        # Scrape water level data
        logger.info("Scraping water level data...")
        water_data = await scraper.scrape_water_level(
            request.state,
            request.district,
            request.basin,
            request.river
        )
        
        water_levels = water_data.get('water_levels', [])
        warning_level = water_data.get('warning_level', 50.0)
        danger_level = water_data.get('danger_level', 52.0)
        
        # Make prediction
        logger.info("Making prediction...")
        prediction_result = predictor.predict(
            rainfall_data,
            water_levels,
            warning_level,
            danger_level
        )
        
        # Combine results
        response = {
            **prediction_result,
            "rainfall_data": rainfall_data,
            "water_levels": water_levels,
            "station_info": {
                "name": station['Station Name'],
                "state": station['State name'],
                "district": station['District / Town'],
                "basin": station['Basin Name'],
                "river": station['River Name'],
                "latitude": latitude,
                "longitude": longitude
            },
            "is_mock": water_data.get('is_mock', False)
        }
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)
