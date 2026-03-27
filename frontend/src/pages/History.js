import React from 'react';
import { Container, Typography, Paper, Box, List, ListItem, ListItemText } from '@mui/material';

const dummyHistory = [
  { date: '2026-03-27', input: 'RAM: 4GB, Battery: 3000mAh', result: 'Mid Range' },
  { date: '2026-03-26', input: 'RAM: 8GB, Battery: 4500mAh', result: 'High End' },
];

const History = () => {
  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <Paper elevation={3} sx={{ p: 4 }}>
        <Typography variant="h5" gutterBottom>
          🕑 Prediction History
        </Typography>
        <Box sx={{ mt: 2 }}>
          <List>
            {dummyHistory.map((item, idx) => (
              <ListItem key={idx} divider>
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
