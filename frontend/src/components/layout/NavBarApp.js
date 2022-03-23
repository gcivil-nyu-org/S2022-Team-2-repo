import React, { useState, useEffect } from 'react';
import {
  chakra,
  Flex,
  HStack,
  Link,
  Button,
  useColorModeValue,
  Box,
  Spacer,
  IconButton,
  useColorMode,
} from '@chakra-ui/react';

import { FaMoon, FaSun } from 'react-icons/fa';
import logo_white from '../../assets/images/logo_white.png';
import logo_black from '../../assets/images/logo_black.png';
import '../../style.css';
import { useHistory } from 'react-router-dom/cjs/react-router-dom.min';

export default function WfWf() {
  const bg = useColorModeValue('#8900e1', '#330662');
  const { toggleColorMode: toggleMode } = useColorMode();
  const text = useColorModeValue('dark', 'light');
  const SwitchIcon = useColorModeValue(FaMoon, FaSun);
  const logo = useColorModeValue(logo_black, logo_white);

  const history = useHistory();
  const handleClickSignUp = () => {
    history.push('/signup');
  };
  const handleClickLogIn = () => {
    history.push('/signin');
  };

  const [isAuth, setIsAuth] = useState(false);

  useEffect(() => {
    if (localStorage.getItem('token') !== null) {
      setIsAuth(true);
    }
  }, []);

  return (
    <React.Fragment>
      <chakra.header
        h="full"
        bg={bg}
        w="full"
        px={{ base: 2, sm: 4 }}
        py={4}
        sticky
      >
        <Flex alignItems="center" justifyContent="space-between" mx="auto">
          <Link display="flex" alignItems="center" href="/">
            <img src={logo} className="logo" alt="NYUnite" />
          </Link>
          <Spacer />
          <Box display="flex" alignItems="center">
            {isAuth === false ? (
              <HStack>
                <Button
                  colorScheme="brand"
                  variant="ghost"
                  size="lg"
                  onClick={handleClickLogIn}
                >
                  Sign in
                </Button>
                <Button
                  colorScheme="brand"
                  variant="ghost"
                  size="lg"
                  onClick={handleClickSignUp}
                >
                  Sign Up
                </Button>
              </HStack>
            ) : (
              <HStack>
                <Link display="flex" alignItems="center" href="/dashboard">
                  <Button colorScheme="brand" variant="ghost" size="lg">
                    Dashboard
                  </Button>
                </Link>
                <Link display="flex" alignItems="center" href="/logout">
                  <Button colorScheme="brand" variant="ghost" size="lg">
                    Logout
                  </Button>
                </Link>
              </HStack>
            )}
            <IconButton
              size="md"
              aria-label={`Switch to ${text} mode`}
              variant="ghost"
              onClick={toggleMode}
              icon={<SwitchIcon />}
            />
          </Box>
        </Flex>
      </chakra.header>
    </React.Fragment>
  );
}
