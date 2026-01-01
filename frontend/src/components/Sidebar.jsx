import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { AlertCircle, Loader2 } from 'lucide-react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Sidebar = ({ onPredict, loading }) => {
  const [states, setStates] = useState([]);
  const [allStations, setAllStations] = useState([]);
  
  const [selectedState, setSelectedState] = useState('');
  const [selectedDistrict, setSelectedDistrict] = useState('');
  const [selectedBasin, setSelectedBasin] = useState('');
  const [selectedRiver, setSelectedRiver] = useState('');
  
  const [districts, setDistricts] = useState([]);
  const [basins, setBasins] = useState([]);
  const [rivers, setRivers] = useState([]);
  
  const [loadingData, setLoadingData] = useState(true);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    fetchStations();
  }, []);
  
  const fetchStations = async () => {
    try {
      setLoadingData(true);
      const response = await axios.get(`${API}/stations`);
      setStates(response.data.states);
      setAllStations(response.data.stations);
      setLoadingData(false);
    } catch (err) {
      setError('Failed to load stations data');
      setLoadingData(false);
    }
  };
  
  // Filter cascading dropdowns
  useEffect(() => {
    if (selectedState) {
      const filtered = allStations.filter(s => s.state === selectedState);
      const uniqueDistricts = [...new Set(filtered.map(s => s.district))];
      setDistricts(uniqueDistricts.sort());
      setSelectedDistrict('');
      setSelectedBasin('');
      setSelectedRiver('');
    }
  }, [selectedState, allStations]);
  
  useEffect(() => {
    if (selectedState && selectedDistrict) {
      const filtered = allStations.filter(s => 
        s.state === selectedState && s.district === selectedDistrict
      );
      const uniqueBasins = [...new Set(filtered.map(s => s.basin))];
      setBasins(uniqueBasins.sort());
      setSelectedBasin('');
      setSelectedRiver('');
    }
  }, [selectedDistrict, selectedState, allStations]);
  
  useEffect(() => {
    if (selectedState && selectedDistrict && selectedBasin) {
      const filtered = allStations.filter(s => 
        s.state === selectedState && 
        s.district === selectedDistrict && 
        s.basin === selectedBasin
      );
      const uniqueRivers = [...new Set(filtered.map(s => s.river))];
      setRivers(uniqueRivers.sort());
      setSelectedRiver('');
    }
  }, [selectedBasin, selectedDistrict, selectedState, allStations]);
  
  const handlePredict = () => {
    if (selectedState && selectedDistrict && selectedBasin && selectedRiver) {
      onPredict({
        state: selectedState,
        district: selectedDistrict,
        basin: selectedBasin,
        river: selectedRiver
      });
    }
  };
  
  if (loadingData) {
    return (
      <div className="flex items-center justify-center py-8">
        <Loader2 className="h-8 w-8 animate-spin text-sky-500" />
      </div>
    );
  }
  
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-lg font-semibold text-white mb-2" style={{ fontFamily: 'Manrope, sans-serif' }}>
          Select Location
        </h2>
        <p className="text-sm text-slate-400" style={{ fontFamily: 'IBM Plex Sans, sans-serif' }}>
          Choose a river station to predict flood risk
        </p>
      </div>
      
      {error && (
        <div className="flex items-center gap-2 rounded-md bg-red-500/10 border border-red-500/20 p-3 text-sm text-red-400">
          <AlertCircle className="h-4 w-4" />
          {error}
        </div>
      )}
      
      <div className="space-y-4">
        {/* State */}
        <div className="space-y-2">
          <Label htmlFor="state" className="text-slate-300" style={{ fontFamily: 'IBM Plex Sans, sans-serif' }}>
            State
          </Label>
          <Select value={selectedState} onValueChange={setSelectedState}>
            <SelectTrigger data-testid="state-select" id="state" className="bg-slate-800 border-slate-700 text-white">
              <SelectValue placeholder="Select state" />
            </SelectTrigger>
            <SelectContent>
              {states.map((state) => (
                <SelectItem key={state} value={state}>{state}</SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
        
        {/* District */}
        <div className="space-y-2">
          <Label htmlFor="district" className="text-slate-300" style={{ fontFamily: 'IBM Plex Sans, sans-serif' }}>
            District
          </Label>
          <Select value={selectedDistrict} onValueChange={setSelectedDistrict} disabled={!selectedState}>
            <SelectTrigger data-testid="district-select" id="district" className="bg-slate-800 border-slate-700 text-white disabled:opacity-50">
              <SelectValue placeholder="Select district" />
            </SelectTrigger>
            <SelectContent>
              {districts.map((district) => (
                <SelectItem key={district} value={district}>{district}</SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
        
        {/* Basin */}
        <div className="space-y-2">
          <Label htmlFor="basin" className="text-slate-300" style={{ fontFamily: 'IBM Plex Sans, sans-serif' }}>
            Basin
          </Label>
          <Select value={selectedBasin} onValueChange={setSelectedBasin} disabled={!selectedDistrict}>
            <SelectTrigger data-testid="basin-select" id="basin" className="bg-slate-800 border-slate-700 text-white disabled:opacity-50">
              <SelectValue placeholder="Select basin" />
            </SelectTrigger>
            <SelectContent>
              {basins.map((basin) => (
                <SelectItem key={basin} value={basin}>{basin}</SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
        
        {/* River */}
        <div className="space-y-2">
          <Label htmlFor="river" className="text-slate-300" style={{ fontFamily: 'IBM Plex Sans, sans-serif' }}>
            River
          </Label>
          <Select value={selectedRiver} onValueChange={setSelectedRiver} disabled={!selectedBasin}>
            <SelectTrigger data-testid="river-select" id="river" className="bg-slate-800 border-slate-700 text-white disabled:opacity-50">
              <SelectValue placeholder="Select river" />
            </SelectTrigger>
            <SelectContent>
              {rivers.map((river) => (
                <SelectItem key={river} value={river}>{river}</SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
      </div>
      
      <Button
        data-testid="predict-button"
        onClick={handlePredict}
        disabled={!selectedRiver || loading}
        className="w-full bg-sky-500 hover:bg-sky-600 text-white font-medium tracking-wide transition-colors duration-200"
        style={{ fontFamily: 'Manrope, sans-serif' }}
      >
        {loading ? (
          <>
            <Loader2 className="mr-2 h-4 w-4 animate-spin" />
            Analyzing...
          </>
        ) : (
          'Predict Flood Risk'
        )}
      </Button>
    </div>
  );
};

export default Sidebar;
