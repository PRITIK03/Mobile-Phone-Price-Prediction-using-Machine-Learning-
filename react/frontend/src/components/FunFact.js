import React, { useState } from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';

const FunFact = () => {
  const facts = [
    'The first mobile phone weighed over 1 kg and was 23 cm long.',
    'More people in the world own a mobile phone than a toothbrush.',
    'The best-selling mobile phone ever is the Nokia 1100.',
    'Mobile phones have more computing power than the computers used for the Apollo 11 moon landing.',
    'Over 5 billion people in the world own a mobile device.'
  ];
  const [fact, setFact] = useState(facts[Math.floor(Math.random() * facts.length)]);

  const handleNewFact = () => {
    let newFact;
    do {
      newFact = facts[Math.floor(Math.random() * facts.length)];
    } while (newFact === fact);
    setFact(newFact);
  };

  return (
    <Box mt={4} p={2} borderRadius={2} boxShadow={1} bgcolor="#e3f2fd" textAlign="center">
      <Typography variant="subtitle1" gutterBottom>
        🤔 {fact}
      </Typography>
      <Button variant="outlined" size="small" onClick={handleNewFact}>
        Show Another Fact
      </Button>
    </Box>
  );
};

export default FunFact;
