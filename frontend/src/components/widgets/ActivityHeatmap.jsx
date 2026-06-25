import Plot from 'react-plotly.js';

const ActivityHeatmap = ({ data }) => {
  if (!data || !data.z || data.z.length === 0) {
    return <div className="text-slate-500 text-sm text-center py-8">No heatmap data available</div>;
  }

  return (
    <div className="w-full h-64">
      <Plot
        data={[
          {
            z: data.z,
            x: data.x,
            y: data.y,
            type: 'heatmap',
            colorscale: 'Blues',
            showscale: false,
            hoverongaps: false
          }
        ]}
        layout={{
          autosize: true,
          margin: { t: 10, r: 10, l: 80, b: 40 },
          xaxis: { 
            showgrid: false, 
            color: '#64748b',
            tickangle: -45
          },
          yaxis: { 
            showgrid: false, 
            color: '#64748b',
            autorange: 'reversed' // To have Sunday at top or Monday at top
          },
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

export default ActivityHeatmap;
