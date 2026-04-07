import React from 'react';

const AreaChart = () => {
  // Sample static data
  const data = [12, 28, 18, 35, 22, 30, 16];
  const maxValue = Math.max(...data);
  const points = data.map((d, i) => `${i * 30},${100 - (d / maxValue) * 80}`).join(' ');
  const areaPoints = `0,100 ${points} ${180},100`;

  return (
    <div style={{ width: '220px', margin: '20px auto', background: '#e8f5e9', borderRadius: 12, padding: 12 }}>
      <h4 style={{ color: '#388e3c', marginBottom: 8 }}>Sample Area Chart</h4>
      <svg width="200" height="110">
        <polygon
          fill="#4e79a7"
          fillOpacity="0.3"
          stroke="#4e79a7"
          strokeWidth="2"
          points={areaPoints}
        />
        <polyline
          fill="none"
          stroke="#e15759"
          strokeWidth="2"
          points={points}
        />
      </svg>
    </div>
  );
};

export default AreaChart;
