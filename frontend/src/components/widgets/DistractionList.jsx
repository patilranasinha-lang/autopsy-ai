import React from 'react';
import { AlertTriangle, ZapOff, Moon } from 'lucide-react';

const DistractionList = ({ patterns }) => {
  const getIcon = (type) => {
    switch (type) {
      case 'Distraction Loop': return <AlertTriangle size={18} className="text-orange-400" />;
      case 'Focus Disruption': return <ZapOff size={18} className="text-yellow-400" />;
      case 'Circadian Disruption': return <Moon size={18} className="text-blue-400" />;
      default: return <AlertTriangle size={18} className="text-gray-400" />;
    }
  };

  return (
    <div className="bg-gray-800 p-6 rounded-xl border border-gray-700">
      <h2 className="text-xl font-bold mb-4 text-white">Top Productivity Killers</h2>
      
      <div className="space-y-4">
        {patterns.slice(0, 5).map(pattern => (
          <div key={pattern.id} className="bg-gray-900/50 p-4 rounded-lg border border-gray-700 flex items-start gap-4">
            <div className="mt-1 bg-gray-800 p-2 rounded-lg">
                {getIcon(pattern.pattern_type)}
            </div>
            <div className="flex-1">
              <div className="flex justify-between items-start mb-1">
                <h3 className="font-semibold text-lg text-gray-200">{pattern.pattern_name}</h3>
                <span className="text-xs font-bold px-2 py-1 rounded bg-rose-900/30 text-rose-400 border border-rose-500/20">
                  Severity: {pattern.severity_score.toFixed(0)}
                </span>
              </div>
              <p className="text-sm text-gray-400 mb-2">{pattern.description}</p>
              
              <div className="flex gap-4 text-xs text-gray-500 font-medium">
                <span>Frequency: <span className="text-gray-300">{pattern.frequency}</span></span>
                <span>Time Lost: <span className="text-gray-300">{pattern.estimated_time_lost} mins</span></span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default DistractionList;
