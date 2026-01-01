import React, { useState, useEffect } from 'react';
import './App.css';
import axios from 'axios';
import DashboardLayout from './components/DashboardLayout';
import Sidebar from './components/Sidebar';
import MapView from './components/MapView';
import PredictionPanel from './components/PredictionPanel';
import { Toaster } from '@/components/ui/sonner';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function App() {
  const [stations, setStations] = useState([]);
  const [predictionResult, setPredictionResult] = useState(null);
  const [loading, setLoading] = useState(false);
  
  useEffect(() => {
    fetchStations();
  }, []);
  
  const fetchStations = async () => {
    try {
      const response = await axios.get(`${API}/stations`);
      setStations(response.data.stations);
    } catch (error) {
      console.error('Failed to fetch stations:', error);
      toast.error('Failed to load station data');
    }
  };
  
  const handlePredict = async (location) => {
    setLoading(true);
    setPredictionResult(null);
    
    toast.loading('Fetching rainfall data and water levels...');
    
    try {
      const response = await axios.post(`${API}/predict`, location);
      setPredictionResult(response.data);
      
      toast.dismiss();
      
      if (response.data.status === 'Danger') {
        toast.error(`DANGER: Flood risk detected at ${response.data.station_info.name}!`);
      } else if (response.data.status === 'Warning') {
        toast.warning(`WARNING: Elevated flood risk at ${response.data.station_info.name}`);
      } else {
        toast.success(`Safe: No flood risk detected at ${response.data.station_info.name}`);
      }
      
    } catch (error) {
      console.error('Prediction failed:', error);
      toast.dismiss();
      toast.error(error.response?.data?.detail || 'Prediction failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };
  
  const handleStationClick = (station) => {
    console.log('Station clicked:', station);
  };
  
  return (
    <div className="App">
      <DashboardLayout
        sidebar={<Sidebar onPredict={handlePredict} loading={loading} />}
      >
        {/* Map Background */}
        <div className="absolute inset-0 z-0">
          <MapView 
            stations={stations} 
            predictionResult={predictionResult}
            onStationClick={handleStationClick}
          />
        </div>
        
        {/* Floating Prediction Panel */}
        {predictionResult && (
          <div className="absolute right-4 top-4 bottom-4 w-96 z-10 pointer-events-auto">
            <div className="h-full bg-white/95 backdrop-blur-md rounded-lg shadow-2xl border border-slate-200">
              <PredictionPanel result={predictionResult} />
            </div>
          </div>
        )}
      </DashboardLayout>
      
      <Toaster position="top-right" richColors />
    </div>
  );
}

export default App;
