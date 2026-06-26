import React from 'react';
import { Calendar } from 'lucide-react';

const RoutineMap = () => {
  // Placeholder for a future interactive heatmap.
  // For the current milestone, it renders a visual representation of detected routine clusters.
  
  const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
  
  return (
    <div className="bg-gray-800 p-6 rounded-xl border border-gray-700">
      <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
        <Calendar className="text-indigo-400" /> Weekly Routine Map
      </h2>
      <p className="text-sm text-gray-400 mb-6">Visualizes your most clustered behavior blocks across the week.</p>
      
      <div className="grid grid-cols-7 gap-2 text-center">
        {days.map(day => (
          <div key={day} className="text-xs font-semibold text-gray-500 mb-2">{day}</div>
        ))}
        
        {/* Mock representation of heat blocks */}
        {Array.from({ length: 28 }).map((_, i) => {
            const isHighHeat = i === 9 || i === 10 || i === 16;
            const isMediumHeat = i === 2 || i === 11 || i === 24;
            
            let bgClass = "bg-gray-900";
            if (isHighHeat) bgClass = "bg-indigo-500";
            else if (isMediumHeat) bgClass = "bg-indigo-500/50";
            
            return (
                <div key={i} className={`h-12 rounded ${bgClass} border border-gray-700 transition-colors hover:border-white cursor-help`} title="Routine Block"></div>
            )
        })}
      </div>
      <div className="mt-4 flex justify-center gap-4 text-xs text-gray-400">
          <div className="flex items-center gap-1"><div className="w-3 h-3 bg-indigo-500 rounded"></div> High Frequency</div>
          <div className="flex items-center gap-1"><div className="w-3 h-3 bg-indigo-500/50 rounded"></div> Medium Frequency</div>
          <div className="flex items-center gap-1"><div className="w-3 h-3 bg-gray-900 rounded border border-gray-700"></div> Low Frequency</div>
      </div>
    </div>
  );
};

export default RoutineMap;
