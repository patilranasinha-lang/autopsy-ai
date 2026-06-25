import React from 'react';
import Plot from 'react-plotly.js';

const SessionTimeline = ({ sessions }) => {
  if (!sessions || sessions.length === 0) {
    return <div className="text-slate-500 text-sm text-center py-8">No sessions available</div>;
  }

  // Create a Gantt-like chart using Plotly timeline or horizontal bar
  // Plotly handles timeline with type 'bar', orientation 'h', and base
  
  const yCategories = [...new Set(sessions.map(s => s.session_type))];
  
  const plotData = sessions.map((s, i) => {
    return {
      x: [s.duration_minutes],
      y: [s.session_type],
      base: [new Date(s.start_time).getTime() - new Date(sessions[0].start_time).getTime()], // relative for simplicity or use dates directly
      type: 'bar',
      orientation: 'h',
      name: s.session_type,
      text: `${s.duration_minutes}m`,
      hoverinfo: 'text+name',
      marker: {
        color: getColorForType(s.session_type)
      }
    };
  });

  // For proper Plotly Gantt / Timeline with datetime:
  const timelineData = sessions.map(s => ({
    x: [s.start_time, s.end_time],
    y: [s.session_type, s.session_type],
    type: 'scatter',
    mode: 'lines',
    line: { width: 20, color: getColorForType(s.session_type) },
    name: s.session_type,
    text: `${s.duration_minutes}m (${s.productivity_score} score)`,
    hoverinfo: 'text+name'
  }));

  function getColorForType(type) {
    if (type.includes("Deep Work")) return "#10b981"; // emerald
    if (type.includes("Coding")) return "#3b82f6"; // blue
    if (type.includes("Entertainment")) return "#f59e0b"; // amber
    if (type.includes("Switching")) return "#ef4444"; // red
    if (type.includes("Study")) return "#8b5cf6"; // purple
    return "#64748b"; // slate
  }

  return (
    <div className="w-full h-80">
      <Plot
        data={timelineData}
        layout={{
          autosize: true,
          margin: { t: 20, r: 20, l: 150, b: 40 },
          showlegend: false,
          paper_bgcolor: 'transparent',
          plot_bgcolor: 'transparent',
          xaxis: { type: 'date', showgrid: true, gridcolor: '#f1f5f9' },
          yaxis: { showgrid: true, gridcolor: '#f1f5f9', categoryorder: 'category ascending' }
        }}
        useResizeHandler={true}
        style={{ width: '100%', height: '100%' }}
        config={{ displayModeBar: false }}
      />
    </div>
  );
};

export default SessionTimeline;
