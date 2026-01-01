import React from 'react';
import { Droplets } from 'lucide-react';

const DashboardLayout = ({ children, sidebar }) => {
  return (
    <div className="relative h-screen w-screen overflow-hidden bg-slate-50">
      {/* Sidebar */}
      <aside className="fixed left-0 top-0 z-20 h-screen w-80 bg-slate-900/90 backdrop-blur-xl border-r border-slate-700/50 shadow-2xl">
        <div className="flex h-full flex-col">
          {/* Logo */}
          <div className="flex items-center gap-3 border-b border-slate-700/50 p-6">
            <div className="flex h-10 w-10 items-center justify-center rounded-md bg-sky-500">
              <Droplets className="h-6 w-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold tracking-tight text-white" style={{ fontFamily: 'Manrope, sans-serif' }}>
                FloodWatch
              </h1>
              <p className="text-xs text-slate-400" style={{ fontFamily: 'IBM Plex Sans, sans-serif' }}>
                India Flood Prediction
              </p>
            </div>
          </div>
          
          {/* Sidebar Content */}
          <div className="flex-1 overflow-y-auto p-6">
            {sidebar}
          </div>
        </div>
      </aside>
      
      {/* Main Content Area */}
      <main className="absolute inset-0 left-80 z-0">
        {children}
      </main>
    </div>
  );
};

export default DashboardLayout;
