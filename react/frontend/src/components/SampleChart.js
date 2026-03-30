import React from 'react';

const SampleChart = () => {
  // Sample static data for demonstration
  const data = [
    { label: 'A', value: 30 },
    { label: 'B', value: 50 },
    { label: 'C', value: 20 },
  ];

  const maxValue = Math.max(...data.map(d => d.value));

  return (
    <div style={{ width: '300px', margin: '20px auto' }}>
      <h3>Sample Bar Chart</h3>
      <svg width="300" height="150">
        {data.map((d, i) => (
          <g key={d.label}>
            <rect
              x={i * 100 + 10}
              y={150 - (d.value / maxValue) * 120}
              width="60"
              height={(d.value / maxValue) * 120}
              fill="#4e79a7"
            />
            <text
              x={i * 100 + 40}
              y={145}
              textAnchor="middle"
              fontSize="14"
            >
              {d.label}
            </text>
            <text
              x={i * 100 + 40}
              y={150 - (d.value / maxValue) * 120 - 5}
              textAnchor="middle"
              fontSize="12"
              fill="#333"
            >
              {d.value}
            </text>
          </g>
        ))}
      </svg>
    </div>
  );
};

export default SampleChart;
