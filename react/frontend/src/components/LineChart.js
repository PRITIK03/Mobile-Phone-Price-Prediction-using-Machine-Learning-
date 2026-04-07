import React from 'react';

const LineChart = () => {
  // Sample static data
  const data = [10, 30, 20, 40, 25, 35, 15];
  const maxValue = Math.max(...data);
  const points = data.map((d, i) => `${i * 30},${100 - (d / maxValue) * 80}`).join(' ');

  return (
    <div style={{ width: '220px', margin: '20px auto', background: '#e3f2fd', borderRadius: 12, padding: 12 }}>
      <h4 style={{ color: '#1976d2', marginBottom: 8 }}>Sample Line Chart</h4>
      <svg width="200" height="110">
        <polyline
          fill="none"
          stroke="#e15759"
          strokeWidth="3"
          points={points}
        />
        {data.map((d, i) => (
          <circle
            key={i}
            cx={i * 30}
            cy={100 - (d / maxValue) * 80}
            r="3"
            fill="#4e79a7"
          />
        ))}
      </svg>
    </div>
  );
};

export default LineChart;
