import React from 'react';
import { ChakraProvider, theme, Flex, Container } from '@chakra-ui/react';
import { BrowserRouter as Router, Switch, Route, Link } from 'react-router-dom';
import NavBarApp from './components/layout/NavBarApp';
import NavBarHome from './components/layout/NavBarHome';
import HomePage from './views/app/HomePage';
import Signup from './views/authentication/Signup';
import Signin from './views/authentication/Signin';

function App() {
  return (
    <ChakraProvider theme={theme}>
      <div className="App">
        <Router>
          {/*  */}
          <Switch>
            <Route exact path="/">
              <div
                className="header"
                style={{ position: 'relative', zIndex: '1' }}
              >
                <NavBarApp />
              </div>
              <HomePage />
            </Route>

            <Route path="/signin">
              <div
                className="header"
                style={{ position: 'relative', zIndex: '1' }}
              >
                <NavBarApp />
              </div>
              <Signin />
            </Route>

            <Route path="/signup">
              <div
                className="header"
                style={{ position: 'relative', zIndex: '1' }}
              >
                <NavBarApp />
              </div>
              <Signup />
            </Route>
          </Switch>
        </Router>
      </div>
      {/* <div className='fill-window'>
        <HomePage />
      </div>*/}
    </ChakraProvider>
  );
}

export default App;
