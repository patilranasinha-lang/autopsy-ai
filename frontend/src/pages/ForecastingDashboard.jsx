import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';

const ForecastingDashboard = () => {
  const [forecast, setForecast] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchDashboardData = async () => {
    try {
      const token = localStorage.getItem('token');
      const headers = { Authorization: `Bearer ${token}` };
      
      const res = await axios.get('/api/forecasts/tomorrow', { headers });
      setForecast(res.data.forecast);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const generateForecast = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      await axios.post('/api/forecasts/generate', {}, {
        headers: { Authorization: `Bearer ${token}` }
      });
      await fetchDashboardData();
    } catch (err) {
      console.error(err);
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  if (loading) return <div className="text-white p-6">Generating productivity forecasts...</div>;

  return (
    <div className="p-6 text-white space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-green-400 to-emerald-600">
            Productivity Forecasting
          </h1>
          <p className="text-gray-400 mt-2">Predictive analytics for your upcoming performance.</p>
        </div>
        <button 
          onClick={generateForecast}
          className="flex items-center gap-2 px-4 py-2 bg-emerald-600 hover:bg-emerald-700 rounded-lg transition-colors"
        >
          Generate Forecast
        </button>
      </div>
      
      {!forecast ? (
        <div className="bg-gray-800 p-8 rounded-xl text-center border border-gray-700">
          <p className="text-gray-400">No forecast for tomorrow. Click "Generate Forecast".</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-gray-800 p-6 rounded-xl border border-gray-700 flex flex-col items-center justify-center">
             <h3 className="text-gray-400 text-sm uppercase tracking-wider mb-2">Tomorrow's Expected Score</h3>
             <span className="text-5xl font-bold text-white">{forecast.forecasted_productivity_score.toFixed(0)}</span>
             <span className="text-gray-500 mt-1">/100</span>
          </div>

          <div className="bg-gray-800 p-6 rounded-xl border border-gray-700 flex flex-col items-center justify-center">
             <h3 className="text-gray-400 text-sm uppercase tracking-wider mb-2">Trajectory</h3>
             <div className="flex items-center gap-2">
                 {forecast.trajectory_trend === 'up' && <TrendingUp className="text-emerald-400" size={32} />}
                 {forecast.trajectory_trend === 'down' && <TrendingDown className="text-red-400" size={32} />}
                 {forecast.trajectory_trend === 'stable' && <Minus className="text-blue-400" size={32} />}
                 <span className="text-2xl font-semibold capitalize">{forecast.trajectory_trend}</span>
             </div>
          </div>

          <div className="bg-gray-800 p-6 rounded-xl border border-gray-700 flex flex-col items-center justify-center">
             <h3 className="text-gray-400 text-sm uppercase tracking-wider mb-2">Expected Deep Work</h3>
             <span className="text-3xl font-bold text-blue-300">
                 {Math.floor(forecast.forecasted_deep_work_minutes / 60)}h {forecast.forecasted_deep_work_minutes % 60}m
             </span>
          </div>
        </div>
      )}
    </div>
  );
};

export default ForecastingDashboard;
