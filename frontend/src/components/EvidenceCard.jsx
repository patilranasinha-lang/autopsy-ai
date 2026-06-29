import React from 'react';
import { Database, FileText, Activity } from 'lucide-react';

const EvidenceCard = ({ evidence }) => {
  const getIcon = (type) => {
    switch (type) {
      case 'Habit': return <Activity size={14} className="text-purple-400" />;
      case 'Session': return <FileText size={14} className="text-blue-400" />;
      default: return <Database size={14} className="text-gray-400" />;
    }
  };

  return (
    <div className="bg-gray-800 border border-gray-700 rounded-lg p-3 mt-2 mb-4 w-full md:w-3/4">
      <h4 className="text-xs uppercase tracking-wider text-gray-500 mb-2 font-semibold">Evidence Used</h4>
      <div className="space-y-2">
        {evidence.map((item, idx) => (
          <div key={idx} className="flex items-start gap-2 text-sm text-gray-300">
            <div className="mt-0.5">{getIcon(item.document_type)}</div>
            <p className="leading-snug">"{item.text}"</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default EvidenceCard;
