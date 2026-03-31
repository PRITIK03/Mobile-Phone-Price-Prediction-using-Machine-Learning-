import React from 'react';

const DonutChart = () => {
  // Sample static data
  const data = [
    { label: 'A', value: 45, color: '#4e79a7' },
    { label: 'B', value: 25, color: '#f28e2b' },
    { label: 'C', value: 30, color: '#e15759' },
  ];
  const total = data.reduce((sum, d) => sum + d.value, 0);
  let cumulative = 0;

  return (
    <div style={{ width: '180px', margin: '20px auto' }}>
      <h4>Sample Donut Chart</h4>
      <svg width="150" height="150" viewBox="0 0 32 32">
        {data.map((d, i) => {
          const startAngle = (cumulative / total) * 2 * Math.PI;
          const endAngle = ((cumulative + d.value) / total) * 2 * Math.PI;
          const x1 = 16 + 14 * Math.sin(startAngle);
          const y1 = 16 - 14 * Math.cos(startAngle);
          const x2 = 16 + 14 * Math.sin(endAngle);
          const y2 = 16 - 14 * Math.cos(endAngle);
          const largeArc = d.value / total > 0.5 ? 1 : 0;
          const pathData = `M16,16 L${x1},${y1} A14,14 0 ${largeArc} 1 ${x2},${y2} Z`;
          cumulative += d.value;
          return (
            <path key={d.label} d={pathData} fill={d.color} stroke="#fff" strokeWidth="0.5" />
          );
        })}
        <circle cx="16" cy="16" r="7" fill="#fff" />
      </svg>
      <div style={{ display: 'flex', justifyContent: 'center', gap: '8px', marginTop: '8px' }}>
        {data.map(d => (
          <span key={d.label} style={{ fontSize: '12px' }}>
            <span style={{ display: 'inline-block', width: 10, height: 10, background: d.color, marginRight: 4 }} />
            {d.label}
          </span>
        ))}
      </div>
    </div>
  );
};

export default DonutChart;
