import Plot from 'react-plotly.js';

const ActivityDistribution = ({ data }) => {
  const keys = Object.keys(data);
  if (keys.length === 0) {
    return <div className="text-slate-500 text-sm text-center py-8">No distribution data available</div>;
  }

  const values = Object.values(data);
  
  return (
    <div className="w-full h-64">
      <Plot
        data={[
          {
            values: values,
            labels: keys,
            type: 'pie',
            hole: 0.6,
            textinfo: 'label+percent',
            hoverinfo: 'label+percent',
            marker: {
              colors: [
                '#3b82f6', // blue-500
                '#8b5cf6', // violet-500
                '#10b981', // emerald-500
                '#f59e0b', // amber-500
                '#ef4444', // red-500
                '#64748b'  // slate-500
              ]
            }
          }
        ]}
        layout={{
          autosize: true,
          margin: { t: 10, r: 10, l: 10, b: 10 },
          showlegend: false,
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

export default ActivityDistribution;
