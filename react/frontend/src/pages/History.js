import React from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Paper from '@mui/material/Paper';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import ListItemIcon from '@mui/material/ListItemIcon';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import TrendingDownIcon from '@mui/icons-material/TrendingDown';

const dummyHistory = [
  { date: '2026-03-27', input: 'RAM: 4GB, Battery: 3000mAh', result: 'Mid Range' },
  { date: '2026-03-26', input: 'RAM: 8GB, Battery: 4500mAh', result: 'High End' },
  { date: '2026-03-25', input: 'RAM: 2GB, Battery: 2000mAh', result: 'Low End' },
];

const getResultIcon = (result) => {
  if (result.includes('High')) return <TrendingUpIcon color="success" />;
  if (result.includes('Low')) return <TrendingDownIcon color="error" />;
  return <CheckCircleIcon color="primary" />;
};

function History() {
  return (
    <Box mt={4} textAlign="center">
      <Paper elevation={3} sx={{ p: 4, background: 'linear-gradient(135deg, #f5faff 0%, #fff 100%)' }}>
        <Typography variant="h5" gutterBottom sx={{ fontWeight: 600 }}>
          🕑 Prediction History
        </Typography>
        <Box sx={{ mt: 2 }}>
          <List>
            {dummyHistory.map((item, idx) => (
              <ListItem
                key={idx}
                divider
                sx={{
                  background: idx % 2 === 0 ? '#e3f2fd' : '#fff',
                  borderRadius: 2,
                  mb: 1,
                }}
              >
                <ListItemIcon>
                  {getResultIcon(item.result)}
                </ListItemIcon>
                <ListItemText
                  primary={`Input: ${item.input}`}
                  secondary={`Date: ${item.date} | Result: ${item.result}`}
                />
              </ListItem>
            ))}
          </List>
        </Box>
      </Paper>
    </Box>
  );
}

export default History;
