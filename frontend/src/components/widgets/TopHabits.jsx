import React from 'react';
import { Target } from 'lucide-react';

const TopHabits = ({ habits }) => {
  return (
    <div className="bg-gray-800 p-6 rounded-xl border border-gray-700">
      <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
        <Target className="text-teal-400" /> Top Confirmed Habits
      </h2>
      <div className="space-y-4">
        {habits.map(habit => (
          <div key={habit.id} className="p-4 bg-gray-900 rounded-lg border border-gray-700 hover:border-teal-500 transition-colors">
            <div className="flex justify-between items-start mb-2">
              <h3 className="font-semibold text-lg text-gray-100">{habit.habit_name}</h3>
              <span className="text-xs font-bold px-2 py-1 bg-teal-500/20 text-teal-400 rounded-full">
                {habit.confidence_score}% Confidence
              </span>
            </div>
            <p className="text-sm text-gray-400 mb-2">{habit.description}</p>
            <div className="flex gap-2">
                <span className="text-xs bg-gray-800 text-gray-400 px-2 py-1 rounded">
                    Category: {habit.habit_type}
                </span>
                <span className="text-xs bg-gray-800 text-gray-400 px-2 py-1 rounded">
                    Frequency: {habit.frequency}
                </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default TopHabits;
