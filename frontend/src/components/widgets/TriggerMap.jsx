import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Zap, AlertTriangle } from 'lucide-react';

const TriggerMap = () => {
  const [triggers, setTriggers] = useState([]);
  
  useEffect(() => {
    const fetchTriggers = async () => {
      try {
        const token = localStorage.getItem('token');
        const res = await axios.get('/api/habits/triggers', {
          headers: { Authorization: `Bearer ${token}` }
        });
        setTriggers(res.data.triggers || []);
      } catch (err) {
        console.error(err);
      }
    };
    fetchTriggers();
  }, []);

  const positiveTriggers = triggers.filter(t => t.habit_type === 'Productivity Habits');
  const negativeTriggers = triggers.filter(t => t.habit_type === 'Procrastination Habits');

  return (
    <div className="bg-gray-800 p-6 rounded-xl border border-gray-700">
      <h2 className="text-xl font-bold mb-6">Behavioral Triggers</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <h3 className="text-lg font-semibold text-green-400 flex items-center gap-2 mb-4">
            <Zap size={18} /> Productivity Triggers
          </h3>
          {positiveTriggers.length === 0 && <p className="text-gray-500 text-sm">No positive triggers detected yet.</p>}
          <div className="space-y-3">
            {positiveTriggers.map(t => (
              <div key={t.id} className="p-3 bg-gray-900/50 border border-green-500/30 rounded-lg">
                <p className="text-sm text-gray-300">{t.description}</p>
              </div>
            ))}
          </div>
        </div>
        
        <div>
          <h3 className="text-lg font-semibold text-red-400 flex items-center gap-2 mb-4">
            <AlertTriangle size={18} /> Procrastination Triggers
          </h3>
          {negativeTriggers.length === 0 && <p className="text-gray-500 text-sm">No negative triggers detected yet.</p>}
          <div className="space-y-3">
            {negativeTriggers.map(t => (
              <div key={t.id} className="p-3 bg-gray-900/50 border border-red-500/30 rounded-lg">
                <p className="text-sm text-gray-300">{t.description}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default TriggerMap;
