import React from 'react';
import { ChakraProvider, theme, Flex } from '@chakra-ui/react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import NavBarApp from './components/layout/NavBarApp';
import NavBarHome from './components/layout/NavBarHome';
import HomePage from './views/app/HomePage';
import Signup from './views/authentication/Signup';
import Login from './views/authentication/Login';

function App() {
  return (
    <ChakraProvider theme={theme}>
      <div className="App">
        <Router>
//        <div style={{ position: 'relative', zIndex: '1' }}>
          <NavBarApp />
          <div className="App">
            <Switch>

          <Signup />
              <Route exact path="/">
                <NavBarApp />
                <HomePage />
              </Route>

              <Route path="/Login">
                <NavBarApp />
                <Login />
              </Route>

              <Route path="/Signup">
              <NavBarApp />
                <Signup />

              </Route>


            </Switch>
          </div>
        </Router>
      </div>
      {/* <div className='fill-window'>
        <HomePage />
      </div>*/}
    </ChakraProvider>

  );
}

export default App;
