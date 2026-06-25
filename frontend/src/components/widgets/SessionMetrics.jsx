import React from 'react';
import Card from '../Card';
import { Clock, Briefcase, PlayCircle, GitCommit } from 'lucide-react';

const SessionMetrics = ({ summary }) => {
  if (!summary) return null;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <Card className="p-6">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-slate-500 font-medium">Total Sessions</p>
            <p className="text-2xl font-bold text-slate-900 mt-1">{summary.total_sessions}</p>
          </div>
          <div className="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center text-blue-600">
            <GitCommit size={24} />
          </div>
        </div>
      </Card>
      
      <Card className="p-6">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-slate-500 font-medium">Longest Focus</p>
            <p className="text-2xl font-bold text-slate-900 mt-1">{summary.longest_session_minutes}m</p>
          </div>
          <div className="w-12 h-12 bg-emerald-100 rounded-xl flex items-center justify-center text-emerald-600">
            <Clock size={24} />
          </div>
        </div>
      </Card>

      <Card className="p-6">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-slate-500 font-medium">Deep Work Hours</p>
            <p className="text-2xl font-bold text-slate-900 mt-1">{summary.deep_work_hours}h</p>
          </div>
          <div className="w-12 h-12 bg-purple-100 rounded-xl flex items-center justify-center text-purple-600">
            <Briefcase size={24} />
          </div>
        </div>
      </Card>

      <Card className="p-6">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-slate-500 font-medium">Context Switch Score</p>
            <p className="text-2xl font-bold text-slate-900 mt-1">{summary.context_switching_score}%</p>
          </div>
          <div className="w-12 h-12 bg-orange-100 rounded-xl flex items-center justify-center text-orange-600">
            <PlayCircle size={24} />
          </div>
        </div>
      </Card>
    </div>
  );
};

export default SessionMetrics;
