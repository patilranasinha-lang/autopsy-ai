import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const BurnoutTrendChart = ({ history }) => {
  if (!history || history.length === 0) {
    return (
      <div className="bg-gray-800 p-6 rounded-xl border border-gray-700 h-full flex items-center justify-center text-gray-500">
        Not enough history for trend chart.
      </div>
    );
  }

  // Reverse to chronological
  const chartData = [...history].reverse().map(h => ({
    date: new Date(h.generated_at).toLocaleDateString(undefined, { month: 'short', day: 'numeric' }),
    score: h.risk_score
  }));

  return (
    <div className="bg-gray-800 p-6 rounded-xl border border-gray-700 h-full flex flex-col">
      <h2 className="text-xl font-bold mb-6 text-white">Risk Trend</h2>
      <div className="flex-1 min-h-[200px]">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartData} margin={{ top: 5, right: 5, left: -20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" vertical={false} />
            <XAxis dataKey="date" stroke="#9CA3AF" tick={{ fill: '#9CA3AF', fontSize: 12 }} />
            <YAxis stroke="#9CA3AF" tick={{ fill: '#9CA3AF', fontSize: 12 }} domain={[0, 100]} />
            <Tooltip 
              contentStyle={{ backgroundColor: '#1F2937', border: '1px solid #374151', borderRadius: '0.5rem' }}
              itemStyle={{ color: '#F43F5E' }}
            />
            <Line type="monotone" dataKey="score" stroke="#F43F5E" strokeWidth={3} dot={{ r: 4, fill: '#F43F5E', strokeWidth: 0 }} activeDot={{ r: 6 }} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default BurnoutTrendChart;
