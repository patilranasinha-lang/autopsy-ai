import React from 'react';
import { AlertTriangle } from 'lucide-react';

const RiskFactorsList = ({ factors }) => {
  return (
    <div className="bg-gray-800 p-6 rounded-xl border border-gray-700">
      <h2 className="text-xl font-bold mb-4 text-white flex items-center gap-2">
        <AlertTriangle className="text-orange-400" /> Primary Risk Factors
      </h2>
      
      {(!factors || factors.length === 0) ? (
        <p className="text-gray-500">No significant risk factors detected.</p>
      ) : (
        <ul className="space-y-3">
          {factors.map((factor, idx) => (
            <li key={idx} className="flex items-start gap-3 bg-gray-900/50 p-3 rounded-lg border border-gray-700/50">
              <span className="text-orange-500 mt-0.5">•</span>
              <span className="text-gray-300 text-sm">{factor}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default RiskFactorsList;
