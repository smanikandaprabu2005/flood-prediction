import React, { useEffect, useRef } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Fix for default markers
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
});

const MapView = ({ stations, predictionResult, onStationClick }) => {
  const mapRef = useRef(null);
  const mapInstanceRef = useRef(null);
  const markersRef = useRef([]);
  
  useEffect(() => {
    if (!mapRef.current) return;
    
    // Initialize map
    if (!mapInstanceRef.current) {
      mapInstanceRef.current = L.map(mapRef.current).setView([22.5, 78.0], 5);
      
      // Add tile layer - CartoDB Positron (clean and professional)
      L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
        attribution: '©OpenStreetMap, ©CartoDB',
        maxZoom: 20
      }).addTo(mapInstanceRef.current);
    }
    
    // Clear existing markers
    markersRef.current.forEach(marker => marker.remove());
    markersRef.current = [];
    
    // Add station markers
    if (stations && stations.length > 0) {
      stations.forEach((station) => {
        const marker = L.circleMarker([station.latitude, station.longitude], {
          radius: 6,
          fillColor: '#10B981',
          color: '#fff',
          weight: 2,
          opacity: 1,
          fillOpacity: 0.8
        });
        
        marker.bindPopup(`
          <div style="font-family: 'IBM Plex Sans', sans-serif;">
            <strong style="font-size: 14px;">${station.station_name}</strong><br/>
            <span style="font-size: 12px; color: #64748b;">
              ${station.river} River<br/>
              ${station.district}, ${station.state}
            </span>
          </div>
        `);
        
        marker.on('click', () => {
          if (onStationClick) {
            onStationClick(station);
          }
        });
        
        marker.addTo(mapInstanceRef.current);
        markersRef.current.push(marker);
      });
    }
    
    // Highlight prediction station
    if (predictionResult && predictionResult.station_info) {
      const info = predictionResult.station_info;
      const color = predictionResult.status === 'Danger' ? '#EF4444' : 
                    predictionResult.status === 'Warning' ? '#F59E0B' : '#10B981';
      
      const marker = L.circleMarker([info.latitude, info.longitude], {
        radius: 10,
        fillColor: color,
        color: '#fff',
        weight: 3,
        opacity: 1,
        fillOpacity: 1
      });
      
      marker.bindPopup(`
        <div style="font-family: 'IBM Plex Sans', sans-serif;">
          <strong style="font-size: 14px;">${info.name}</strong><br/>
          <span style="font-size: 12px;">
            <strong style="color: ${color};">${predictionResult.status}</strong><br/>
            Probability: ${(predictionResult.probability * 100).toFixed(1)}%<br/>
            Level: <span style="font-family: 'JetBrains Mono', monospace;">${predictionResult.current_water_level.toFixed(2)}m</span>
          </span>
        </div>
      `).openPopup();
      
      marker.addTo(mapInstanceRef.current);
      markersRef.current.push(marker);
      
      // Center map on this station
      mapInstanceRef.current.setView([info.latitude, info.longitude], 8, {
        animate: true,
        duration: 1
      });
    }
    
    return () => {
      // Cleanup on unmount
      if (mapInstanceRef.current) {
        markersRef.current.forEach(marker => marker.remove());
      }
    };
  }, [stations, predictionResult, onStationClick]);
  
  return <div ref={mapRef} className="h-full w-full" data-testid="map-container" />;
};

export default MapView;
