import React from 'react';
import { Clock } from 'lucide-react';

const TimeLossMetrics = ({ metrics }) => {
  if (!metrics) return null;

  return (
    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
      <div className="bg-gray-800 p-6 rounded-xl border border-gray-700 flex flex-col items-center">
        <h3 className="text-gray-400 text-sm uppercase tracking-wider mb-2">Daily Time Lost</h3>
        <div className="flex items-baseline gap-2">
          <span className="text-3xl font-bold text-rose-400">{metrics.daily_lost_mins}</span>
          <span className="text-gray-500 text-sm">mins</span>
        </div>
      </div>
      
      <div className="bg-gray-800 p-6 rounded-xl border border-gray-700 flex flex-col items-center">
        <h3 className="text-gray-400 text-sm uppercase tracking-wider mb-2">Weekly Time Lost</h3>
        <div className="flex items-baseline gap-2">
          <span className="text-3xl font-bold text-rose-500">{(metrics.weekly_lost_mins / 60).toFixed(1)}</span>
          <span className="text-gray-500 text-sm">hrs</span>
        </div>
      </div>

      <div className="bg-gray-800 p-6 rounded-xl border border-gray-700 flex flex-col items-center">
        <h3 className="text-gray-400 text-sm uppercase tracking-wider mb-2">Monthly Time Lost</h3>
        <div className="flex items-baseline gap-2">
          <span className="text-3xl font-bold text-rose-600">{(metrics.monthly_lost_mins / 60).toFixed(1)}</span>
          <span className="text-gray-500 text-sm">hrs</span>
        </div>
      </div>
      
      <div className="bg-rose-900/20 p-6 rounded-xl border border-rose-500/30 flex flex-col items-center justify-center">
        <Clock className="text-rose-500 mb-2" size={24} />
        <h3 className="text-rose-300 text-sm font-medium text-center">Reclaim your focus.</h3>
      </div>
    </div>
  );
};

export default TimeLossMetrics;
