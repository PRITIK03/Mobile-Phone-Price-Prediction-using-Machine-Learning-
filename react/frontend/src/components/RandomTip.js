import React, { useState } from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';

const RandomTip = () => {
  const tips = [
    'Did you know? Keeping your phone battery between 20% and 80% can extend its lifespan.',
    'Tip: Regularly updating your phone’s software improves security and performance.',
    'Fun fact: More RAM allows your phone to run more apps smoothly at the same time.',
    'Pro tip: Lowering screen brightness can help save battery life.',
    'Did you know? Using Wi-Fi instead of mobile data can save battery.'
  ];
  const [tip, setTip] = useState(tips[Math.floor(Math.random() * tips.length)]);

  const handleNewTip = () => {
    let newTip;
    do {
      newTip = tips[Math.floor(Math.random() * tips.length)];
    } while (newTip === tip);
    setTip(newTip);
  };

  return (
    <Box mt={4} p={3} borderRadius={3} boxShadow={3} bgcolor="#e3f2fd" textAlign="center" sx={{ maxWidth: 350, mx: 'auto' }}>
      <Typography variant="subtitle1" gutterBottom sx={{ color: '#1976d2', fontWeight: 600 }}>
        📱 {tip}
      </Typography>
      <Button 
        variant="contained" 
        size="small" 
        onClick={handleNewTip}
        sx={{
          background: 'linear-gradient(90deg, #1976d2 60%, #64b5f6 100%)',
          color: '#fff',
          borderRadius: 2,
          boxShadow: 2,
          fontWeight: 600,
          textTransform: 'none',
          ':hover': { background: 'linear-gradient(90deg, #1565c0 60%, #1976d2 100%)' }
        }}
      >
        Show Another Tip
      </Button>
    </Box>
  );
};

export default RandomTip;
