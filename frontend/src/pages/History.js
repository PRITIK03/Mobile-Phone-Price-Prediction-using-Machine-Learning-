
import React from 'react';
import { Container, Typography, Paper, Box, List, ListItem, ListItemText, ListItemIcon } from '@mui/material';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import TrendingDownIcon from '@mui/icons-material/TrendingDown';

const dummyHistory = [
  { date: '2026-03-27', input: 'RAM: 4GB, Battery: 3000mAh', result: 'Mid Range' },
  { date: '2026-03-26', input: 'RAM: 8GB, Battery: 4500mAh', result: 'High End' },
];


const getResultIcon = (result) => {
  if (result.includes('High')) return <TrendingUpIcon color="success" />;
  if (result.includes('Low')) return <TrendingDownIcon color="error" />;
  return <CheckCircleIcon color="primary" />;
};

const History = () => {
  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
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
    </Container>
  );
};

export default History;
