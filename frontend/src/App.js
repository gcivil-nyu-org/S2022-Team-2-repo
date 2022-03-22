import React from 'react';
import { ChakraProvider, theme, Flex } from '@chakra-ui/react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import NavBarApp from './components/layout/NavBarApp';
import HomePage from './views/app/HomePage';
import Authenticate from './views/authentication/Authenticate';

function App() {
  return (
    <ChakraProvider theme={theme}>
        <Router>
          <div className="App">
            <Switch>

              <Route exact path="/">
                <NavBarApp />
                <HomePage />
              </Route>
    
              <Route path="/login">
                <NavBarApp />
                <Authenticate />
              </Route>

              <Route path="/signup">
                
              </Route>


            </Switch>          
          </div>
        </Router>
    </ChakraProvider>
  );
}

export default App;

/*
<div className='fill-window'>
<HomePage />
</div>

*/