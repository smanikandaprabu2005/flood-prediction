import React from 'react';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { AlertTriangle, CheckCircle, AlertCircle, Droplets, CloudRain, Activity } from 'lucide-react';
import { AreaChart, Area, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';

const PredictionPanel = ({ result }) => {
  if (!result) {
    return (
      <div className="flex h-full items-center justify-center">
        <div className="text-center" style={{ fontFamily: 'IBM Plex Sans, sans-serif' }}>
          <Droplets className="mx-auto h-16 w-16 text-slate-400 mb-4" />
          <p className="text-slate-600 text-lg">Select a location and click "Predict Flood Risk"</p>
        </div>
      </div>
    );
  }
  
  const statusConfig = {
    'Danger': { color: 'bg-red-500', icon: AlertTriangle, textColor: 'text-red-500' },
    'Warning': { color: 'bg-amber-500', icon: AlertCircle, textColor: 'text-amber-500' },
    'Safe': { color: 'bg-emerald-500', icon: CheckCircle, textColor: 'text-emerald-500' }
  };
  
  const config = statusConfig[result.status] || statusConfig['Safe'];
  const StatusIcon = config.icon;
  
  // Prepare chart data
  const waterLevelData = result.water_levels.map((level, idx) => ({
    day: `Day ${idx + 1}`,
    level: level,
    warning: result.warning_level,
    danger: result.danger_level
  }));
  
  const rainfallData = result.rainfall_data.map((rain, idx) => ({
    day: `Day ${idx + 1}`,
    rainfall: rain
  }));
  
  return (
    <div className="h-full overflow-y-auto p-4 space-y-4">
      {/* Header Card */}
      <Card className="bg-white/90 backdrop-blur-md border-slate-200 shadow-lg p-6">
        <div className="flex items-start justify-between mb-4">
          <div>
            <h2 className="text-2xl font-bold text-slate-900 mb-1" style={{ fontFamily: 'Manrope, sans-serif' }}>
              {result.station_info.name}
            </h2>
            <p className="text-sm text-slate-600" style={{ fontFamily: 'IBM Plex Sans, sans-serif' }}>
              {result.station_info.river} River • {result.station_info.district}, {result.station_info.state}
            </p>
          </div>
          <Badge className={`${config.color} text-white px-4 py-2 text-base`} data-testid="status-badge">
            <StatusIcon className="mr-2 h-4 w-4" />
            {result.status}
          </Badge>
        </div>
        
        {/* Prediction Result */}
        <div className="grid grid-cols-2 gap-4 mt-6">
          <div className="bg-slate-50 rounded-md p-4">
            <p className="text-sm text-slate-600 mb-1" style={{ fontFamily: 'IBM Plex Sans, sans-serif' }}>Flood Prediction</p>
            <p className={`text-2xl font-bold ${config.textColor}`} style={{ fontFamily: 'Manrope, sans-serif' }} data-testid="prediction-label">
              {result.prediction}
            </p>
          </div>
          <div className="bg-slate-50 rounded-md p-4">
            <p className="text-sm text-slate-600 mb-1" style={{ fontFamily: 'IBM Plex Sans, sans-serif' }}>Probability</p>
            <p className="text-2xl font-bold text-slate-900" style={{ fontFamily: 'JetBrains Mono, monospace' }} data-testid="probability-value">
              {(result.probability * 100).toFixed(1)}%
            </p>
          </div>
        </div>
      </Card>
      
      {/* Water Level Metrics */}
      <Card className="bg-white/90 backdrop-blur-md border-slate-200 shadow-lg p-6">
        <div className="flex items-center gap-2 mb-4">
          <Activity className="h-5 w-5 text-sky-500" />
          <h3 className="text-lg font-semibold text-slate-900" style={{ fontFamily: 'Manrope, sans-serif' }}>
            Water Levels
          </h3>
        </div>
        
        <div className="grid grid-cols-3 gap-3 mb-4">
          <div className="bg-sky-50 rounded-md p-3">
            <p className="text-xs text-slate-600 mb-1" style={{ fontFamily: 'IBM Plex Sans, sans-serif' }}>Current</p>
            <p className="text-xl font-bold text-sky-600" style={{ fontFamily: 'JetBrains Mono, monospace' }} data-testid="current-level">
              {result.current_water_level.toFixed(2)}m
            </p>
          </div>
          <div className="bg-amber-50 rounded-md p-3">
            <p className="text-xs text-slate-600 mb-1" style={{ fontFamily: 'IBM Plex Sans, sans-serif' }}>Warning</p>
            <p className="text-xl font-bold text-amber-600" style={{ fontFamily: 'JetBrains Mono, monospace' }}>
              {result.warning_level.toFixed(2)}m
            </p>
          </div>
          <div className="bg-red-50 rounded-md p-3">
            <p className="text-xs text-slate-600 mb-1" style={{ fontFamily: 'IBM Plex Sans, sans-serif' }}>Danger</p>
            <p className="text-xl font-bold text-red-600" style={{ fontFamily: 'JetBrains Mono, monospace' }}>
              {result.danger_level.toFixed(2)}m
            </p>
          </div>
        </div>
        
        {/* Water Level Chart */}
        <ResponsiveContainer width="100%" height={200}>
          <AreaChart data={waterLevelData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
            <XAxis dataKey="day" style={{ fontFamily: 'IBM Plex Sans, sans-serif', fontSize: '12px' }} />
            <YAxis style={{ fontFamily: 'JetBrains Mono, monospace', fontSize: '12px' }} />
            <Tooltip 
              contentStyle={{ fontFamily: 'IBM Plex Sans, sans-serif', fontSize: '12px' }}
              formatter={(value) => `${value.toFixed(2)}m`}
            />
            <ReferenceLine y={result.warning_level} stroke="#F59E0B" strokeDasharray="5 5" label="Warning" />
            <ReferenceLine y={result.danger_level} stroke="#EF4444" strokeDasharray="5 5" label="Danger" />
            <Area type="monotone" dataKey="level" stroke="#0EA5E9" fill="#0EA5E9" fillOpacity={0.3} />
          </AreaChart>
        </ResponsiveContainer>
      </Card>
      
      {/* Rainfall Chart */}
      <Card className="bg-white/90 backdrop-blur-md border-slate-200 shadow-lg p-6">
        <div className="flex items-center gap-2 mb-4">
          <CloudRain className="h-5 w-5 text-sky-500" />
          <h3 className="text-lg font-semibold text-slate-900" style={{ fontFamily: 'Manrope, sans-serif' }}>
            Rainfall (Last 7 Days)
          </h3>
        </div>
        
        <ResponsiveContainer width="100%" height={200}>
          <BarChart data={rainfallData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
            <XAxis dataKey="day" style={{ fontFamily: 'IBM Plex Sans, sans-serif', fontSize: '12px' }} />
            <YAxis style={{ fontFamily: 'JetBrains Mono, monospace', fontSize: '12px' }} />
            <Tooltip 
              contentStyle={{ fontFamily: 'IBM Plex Sans, sans-serif', fontSize: '12px' }}
              formatter={(value) => `${value.toFixed(1)}mm`}
            />
            <Bar dataKey="rainfall" fill="#0EA5E9" />
          </BarChart>
        </ResponsiveContainer>
      </Card>
      
      {result.is_mock && (
        <Card className="bg-amber-50 border-amber-200 p-4">
          <div className="flex items-center gap-2 text-amber-800" style={{ fontFamily: 'IBM Plex Sans, sans-serif' }}>
            <AlertCircle className="h-4 w-4" />
            <p className="text-sm">Note: Using simulated water level data. Live scraping from government site may be unavailable.</p>
          </div>
        </Card>
      )}
    </div>
  );
};

export default PredictionPanel;
