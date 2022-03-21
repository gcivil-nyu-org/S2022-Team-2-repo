import React from 'react';
import { ChakraProvider, theme, Flex } from '@chakra-ui/react';
import { BrowserRouter as Router } from 'react-router-dom';
import NavBarApp from './components/layout/NavBarApp';
import HomePage from './views/app/HomePage';
import Authenticate from './views/authentication/Authenticate';

function App() {
  return (
    <ChakraProvider theme={theme}>
      <div className="App">
        <Router>
          <NavBarApp />
          
          <Authenticate />

        </Router>
      </div>
      <div className='fill-window'>
        <HomePage />
      </div>
    </ChakraProvider>
  );
}

export default App;
