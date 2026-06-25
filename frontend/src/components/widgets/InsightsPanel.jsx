import { Lightbulb, Clock, Calendar, PieChart, Activity } from 'lucide-react';

const InsightsPanel = ({ insights }) => {
  if (!insights || insights.length === 0) {
    return <div className="text-slate-500 text-sm text-center py-8">No insights available</div>;
  }

  const getIcon = (type) => {
    switch (type) {
      case 'productivity': return <Clock size={20} className="text-emerald-500" />;
      case 'routine': return <Calendar size={20} className="text-blue-500" />;
      case 'behavior': return <PieChart size={20} className="text-purple-500" />;
      case 'summary': return <Activity size={20} className="text-orange-500" />;
      default: return <Lightbulb size={20} className="text-yellow-500" />;
    }
  };

  const getBgColor = (type) => {
    switch (type) {
      case 'productivity': return 'bg-emerald-50 border-emerald-100';
      case 'routine': return 'bg-blue-50 border-blue-100';
      case 'behavior': return 'bg-purple-50 border-purple-100';
      case 'summary': return 'bg-orange-50 border-orange-100';
      default: return 'bg-yellow-50 border-yellow-100';
    }
  };

  return (
    <div className="space-y-3">
      {insights.map((insight, index) => (
        <div 
          key={index} 
          className={`flex items-start gap-3 p-3 rounded-lg border ${getBgColor(insight.type)}`}
        >
          <div className="shrink-0 mt-0.5">
            {getIcon(insight.type)}
          </div>
          <p className="text-sm text-slate-700 font-medium leading-relaxed">
            {insight.text}
          </p>
        </div>
      ))}
    </div>
  );
};

export default InsightsPanel;
