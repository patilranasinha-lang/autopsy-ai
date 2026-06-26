import React from 'react';
import { ShieldCheck } from 'lucide-react';

const RecoverySuggestions = ({ patterns }) => {
  const suggestions = patterns
    .filter(p => p.recovery_suggestion)
    .slice(0, 4);

  return (
    <div className="bg-gray-800 p-6 rounded-xl border border-gray-700 h-full">
      <h2 className="text-xl font-bold mb-4 text-white flex items-center gap-2">
        <ShieldCheck className="text-green-400" /> Recovery Interventions
      </h2>
      <p className="text-sm text-gray-400 mb-6">Actionable advice to reclaim your lost focus time.</p>
      
      <div className="space-y-4">
        {suggestions.length === 0 ? (
           <p className="text-gray-500 text-sm">No interventions generated yet.</p>
        ) : (
          suggestions.map((p, idx) => (
            <div key={idx} className="p-4 bg-green-900/10 border border-green-500/20 rounded-lg">
              <h4 className="text-sm font-semibold text-gray-300 mb-1">For {p.pattern_name}</h4>
              <p className="text-sm text-green-100">{p.recovery_suggestion}</p>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default RecoverySuggestions;
