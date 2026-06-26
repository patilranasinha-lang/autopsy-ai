import React from 'react';
import { HeartPulse } from 'lucide-react';

const ActionPlan = ({ actions }) => {
  return (
    <div className="bg-gray-800 p-6 rounded-xl border border-gray-700">
      <h2 className="text-xl font-bold mb-4 text-white flex items-center gap-2">
        <HeartPulse className="text-purple-400" /> Recommended Action Plan
      </h2>
      
      {(!actions || actions.length === 0) ? (
        <p className="text-gray-500">No actions required currently.</p>
      ) : (
        <div className="space-y-4">
          {actions.map((action, idx) => (
            <div key={idx} className="p-4 bg-purple-900/20 border border-purple-500/30 rounded-lg flex items-start gap-3">
               <div className="mt-1 w-6 h-6 rounded-full bg-purple-500/20 text-purple-400 flex items-center justify-center text-xs font-bold border border-purple-500/50">
                   {idx + 1}
               </div>
               <p className="text-purple-100 text-sm leading-relaxed pt-0.5">{action}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ActionPlan;
