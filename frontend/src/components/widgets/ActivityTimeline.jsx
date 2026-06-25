import Plot from 'react-plotly.js';

const ActivityTimeline = ({ data }) => {
  if (!data || data.length === 0) {
    return <div className="text-slate-500 text-sm text-center py-8">No timeline data available</div>;
  }

  const x = data.map(item => item.date);
  const y = data.map(item => item.count);

  return (
    <div className="w-full h-64">
      <Plot
        data={[
          {
            x: x,
            y: y,
            type: 'scatter',
            mode: 'lines+markers',
            marker: { color: '#0ea5e9' }, // Tailwind sky-500
            line: { shape: 'spline', smoothing: 1.3 }
          }
        ]}
        layout={{
          autosize: true,
          margin: { t: 10, r: 10, l: 40, b: 40 },
          xaxis: { showgrid: false, color: '#64748b' },
          yaxis: { showgrid: true, gridcolor: '#f1f5f9', color: '#64748b' },
          paper_bgcolor: 'transparent',
          plot_bgcolor: 'transparent',
        }}
        useResizeHandler={true}
        style={{ width: '100%', height: '100%' }}
        config={{ displayModeBar: false }}
      />
    </div>
  );
};

export default ActivityTimeline;
