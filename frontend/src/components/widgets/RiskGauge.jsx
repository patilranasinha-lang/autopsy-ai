import React from 'react';

const RiskGauge = ({ assessment }) => {
  if (!assessment) return null;

  const score = assessment.risk_score;
  const level = assessment.risk_level;
  
  let colorClass = 'text-green-500';
  let borderClass = 'border-green-500';
  let bgClass = 'bg-green-500/20';
  
  if (level === 'Moderate') {
      colorClass = 'text-yellow-500';
      borderClass = 'border-yellow-500';
      bgClass = 'bg-yellow-500/20';
  } else if (level === 'High') {
      colorClass = 'text-orange-500';
      borderClass = 'border-orange-500';
      bgClass = 'bg-orange-500/20';
  } else if (level === 'Critical') {
      colorClass = 'text-red-500';
      borderClass = 'border-red-500';
      bgClass = 'bg-red-500/20';
  }

  return (
    <div className="bg-gray-800 p-6 rounded-xl border border-gray-700 flex flex-col items-center justify-center text-center h-full">
      <h2 className="text-xl font-bold mb-6 text-white">Burnout Risk</h2>
      
      <div className={`w-40 h-40 rounded-full border-4 flex items-center justify-center mb-6 shadow-[0_0_15px_rgba(0,0,0,0.5)] ${borderClass} ${bgClass}`}>
          <div className="flex flex-col">
              <span className={`text-5xl font-black ${colorClass}`}>{score.toFixed(0)}</span>
              <span className="text-gray-400 text-sm">/ 100</span>
          </div>
      </div>
      
      <div className={`px-4 py-1 rounded-full font-bold uppercase tracking-wider text-sm ${colorClass} ${bgClass} border ${borderClass}`}>
          {level} RISK
      </div>
      
      <p className="mt-4 text-xs text-gray-500">Confidence: {assessment.confidence_score.toFixed(0)}%</p>
    </div>
  );
};

export default RiskGauge;
