import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Flame } from 'lucide-react';
import RiskGauge from '../components/widgets/RiskGauge';
import RiskFactorsList from '../components/widgets/RiskFactorsList';
import ActionPlan from '../components/widgets/ActionPlan';
import BurnoutTrendChart from '../components/widgets/BurnoutTrendChart';

const Burnout = () => {
  const [assessment, setAssessment] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchDashboardData = async () => {
    try {
      const token = localStorage.getItem('token');
      const headers = { Authorization: `Bearer ${token}` };
      
      const [currentRes, historyRes] = await Promise.all([
        axios.get('/api/burnout/current', { headers }),
        axios.get('/api/burnout/history', { headers })
      ]);
      
      setAssessment(currentRes.data);
      setHistory(historyRes.data.history);
    } catch (err) {
      if (err.response && err.response.status === 404) {
        setAssessment(null);
      }
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const generateAssessment = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      await axios.post('/api/burnout/generate', {}, {
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

  if (loading) return <div className="text-white p-6">Analyzing burnout signals...</div>;

  return (
    <div className="p-6 text-white space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-rose-600">
            Burnout Intelligence
          </h1>
          <p className="text-gray-400 mt-2">Predictive cognitive overload detection and prevention.</p>
        </div>
        <button 
          onClick={generateAssessment}
          className="flex items-center gap-2 px-4 py-2 bg-purple-600 hover:bg-purple-700 rounded-lg transition-colors"
        >
          <Flame size={18} />
          Assess Risk
        </button>
      </div>
      
      {!assessment ? (
        <div className="bg-gray-800 p-8 rounded-xl text-center border border-gray-700">
          <p className="text-gray-400">No burnout assessment found. Click "Assess Risk" to evaluate your current trajectory.</p>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <RiskGauge assessment={assessment} />
            <div className="md:col-span-2">
              <BurnoutTrendChart history={history} />
            </div>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <RiskFactorsList factors={assessment.primary_risk_factors} />
            <ActionPlan actions={assessment.recommended_actions} />
          </div>
        </>
      )}
    </div>
  );
};

export default Burnout;
