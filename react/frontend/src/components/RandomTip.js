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
    <Box mt={4} p={2} borderRadius={2} boxShadow={1} bgcolor="#f5f5f5" textAlign="center">
      <Typography variant="subtitle1" gutterBottom>
        📱 {tip}
      </Typography>
      <Button variant="outlined" size="small" onClick={handleNewTip}>
        Show Another Tip
      </Button>
    </Box>
  );
};

export default RandomTip;
