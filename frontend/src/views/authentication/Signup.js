import {
  Button,
  Flex,
  FormControl,
  Heading,
  Input,
  Stack,
  Image,
  Box,
  HStack,
} from '@chakra-ui/react';
import { useState } from 'react';
import axios from 'axios';
import loginphoto from '../../assets/images/login_photo.jpg';
import { useHistory } from 'react-router-dom/cjs/react-router-dom.min';

export default function Signup() {
  const history = useHistory();
  const handleClickSignUp = () => {
    history.push('/signup');
  };
  const handleClickLogIn = () => {
    history.push('/signin');
  };

  const [form_data, setFormData] = useState('');

  function signup(event) {
    axios({
      method: 'POST',
      url: '/signup',
      data: {
        username: form_data.username,
        first_name: form_data.first_name,
        last_name: form_data.last_name,
        password1: form_data.password,
        password2: form_data.password2,
      },
    }).then();

    event.preventDefault();
  }

  function handleChange(event) {
    const { value, name } = event.target;
    setFormData(data => ({
      ...data,
      [name]: value,
    }));
  }

  return (
    <Stack direction={{ base: 'column', md: 'row' }} bgColor={'#330662'}>
      <Flex flex={1} maxW={'30vw'} maxH={'88vh'} align={'stretch'}>
        <Image alt={'Login Image'} objectFit={'scale-down'} src={loginphoto} />
      </Flex>

      <Flex p={8} flex={1} align={'center'} justify={'center'}>
        <Box
          bg="white"
          w="50%"
          p={0}
          color="black"
          borderRadius="lg"
          align="center"
        >
          <Flex color={'black'}>
            <Box
              as="button"
              borderColor={'white'}
              borderWidth={3}
              bg="#a69db2"
              borderRadius="5px 0px 0px 5px"
              p={3}
              onClick={handleClickSignUp}
              w={'50%'}
              _hover={{ bg: '#D6BCFA' }}
            >
              <Heading fontSize={'xl'}>Sign Up</Heading>
            </Box>
            <Box
              as="button"
              bg="#c7d0d8"
              borderRadius="0px 5px 5px 0px"
              p={3}
              onClick={handleClickLogIn}
              w={'50%'}
              h={'97%'}
              _hover={{ bg: '#D6BCFA' }}
            >
              <Heading fontSize={'xl'}>Log In</Heading>
            </Box>
          </Flex>

          <Stack
            spacing={4}
            w={'full'}
            maxW={'md'}
            color={'black'}
            bg="white"
            p={6}
            borderRadius="lg"
          >
            <Stack align={'center'}>
              <FormControl
                id="username"
                onChange={handleChange}
                value={form_data.username}
                border={'#57068c'}
                isRequired
              >
                <Input
                  borderWidth={'2px'}
                  type="text"
                  padding="8px"
                  height="100%"
                  placeholder="NetID"
                  _placeholder={{ color: '#57068c' }}
                />
              </FormControl>
              <HStack spacing={'0px'}>
                <FormControl
                  id="first_name"
                  onChange={handleChange}
                  value={form_data.first_name}
                  border={'#57068c'}
                >
                  <Input
                    borderWidth={'2px'}
                    height="100%"
                    width="100%"
                    type="text"
                    padding="8px"
                    placeholder="FirstName"
                    _placeholder={{ color: '#57068c' }}
                  />
                </FormControl>
                <FormControl
                  id="last_name"
                  onChange={handleChange}
                  value={form_data.last_name}
                  border={'#57068c'}
                >
                  <Input
                    borderWidth={'2px'}
                    width="99%"
                    height="100%"
                    ml="5px"
                    padding="8px"
                    type="text"
                    placeholder="LastName"
                    _placeholder={{ color: '#57068c' }}
                  />
                </FormControl>
              </HStack>
              <FormControl
                id="password1"
                onChange={handleChange}
                value={form_data.password1}
                border={'#57068c'}
                borderWidth="-moz-initial"
              >
                <Input
                  borderWidth={'2px'}
                  type="password"
                  placeholder="Password"
                  padding="8px"
                  height="100%"
                  _placeholder={{ color: '#57068c' }}
                />
              </FormControl>
              <FormControl
                id="password2"
                onChange={handleChange}
                value={form_data.password2}
                border={'#57068c'}
              >
                <Input
                  borderWidth={'2px'}
                  type="password"
                  placeholder="Retype Password"
                  padding="8px"
                  height="100%"
                  _placeholder={{ color: '#57068c' }}
                />
              </FormControl>
            </Stack>

            <Stack spacing={6} align="center">
              <Button
                width="40%"
                borderRadius={'md'}
                bg="#57068c"
                color="white"
                px={4}
                h={10}
                _hover={{ bg: '#57068c' }}
                onClick={signup}
              >
                REGISTER
              </Button>
            </Stack>
          </Stack>
        </Box>
      </Flex>
    </Stack>
  );
}
