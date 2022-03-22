import React from "react";
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
} from "@chakra-ui/react";

import { FaMoon, FaSun } from "react-icons/fa";
import logo_white from "../../assets/images/logo_white.png";
import logo_black from "../../assets/images/logo_black.png";
import '../../style.css';

export default function WfWf() {
  const bg = useColorModeValue("#ab82c5", "#330662");
  const { toggleColorMode: toggleMode } = useColorMode();
  const text = useColorModeValue("dark", "light");
  const SwitchIcon = useColorModeValue(FaMoon, FaSun);
  const logo = useColorModeValue(logo_black, logo_white)

  return (
    <React.Fragment>
      <chakra.header h="full" bg={bg} w="full" px={{ base: 2, sm: 4 }} py={4}>
        <Flex alignItems="center" justifyContent="space-between" mx="auto">
          <Link display="flex" alignItems="center" href="/">
            <img  src={logo} className="photo" alt="NYUnite"/>
          </Link>
          <Spacer />
          <Box display="flex" alignItems="center">
            <HStack spacing={1}>
            <Link display="flex" alignItems="center" href="/login">
              <Button colorScheme="brand" variant="ghost" size="sm">
                Log in
              </Button>
              </Link>
              <Link display="flex" alignItems="center" href="/Signup">
              <Button colorScheme="brand" variant="ghost" size="sm">
                Sign Up
              </Button>
              </Link>
            </HStack>
            <IconButton
              size="md"
              fontSize="lg"
              aria-label={`Switch to ${text} mode`}
              variant="ghost"
              color="current"
              ml={{ base: "0", md: "3" }}
              onClick={toggleMode}
              icon={<SwitchIcon />}
            />
          </Box>
        </Flex>
      </chakra.header>
    </React.Fragment>
  );
}