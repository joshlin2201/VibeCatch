import { Box, Container, Typography, CssBaseline } from '@mui/material';
import SongRecognition from './components/SongRecognition';

function App() {
  return (
    <>
      <CssBaseline />
      <Container maxWidth="sm">
        <Box sx={{ 
          minHeight: '100vh',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          py: 4
        }}>
          <Typography 
            variant="h3" 
            component="h1" 
            gutterBottom 
            sx={{ 
              fontWeight: 'bold',
              background: 'linear-gradient(45deg, #FE6B8B 30%, #FF8E53 90%)',
              backgroundClip: 'text',
              textFillColor: 'transparent',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              mb: 4
            }}
          >
            VibeCatch
          </Typography>
          
          <Typography 
            variant="subtitle1" 
            color="text.secondary" 
            align="center" 
            sx={{ mb: 4 }}
          >
            Feel the Music. Curate the Mood.
          </Typography>

          <SongRecognition />
        </Box>
      </Container>
    </>
  );
}

export default App;
