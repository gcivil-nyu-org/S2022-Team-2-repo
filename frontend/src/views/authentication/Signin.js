import {
  Button,
  Flex,
  FormControl,
  Heading,
  Input,
  Link,
  Stack,
  Image,
  Text,
  Box,
} from '@chakra-ui/react';
import { useHistory } from 'react-router-dom/cjs/react-router-dom.min';
import loginPhoto from '../../assets/images/login_photo.jpg';
import { useState, useEffect } from 'react';
import axios from 'axios';

export default function LogInPage() {
  const history = useHistory();
  const handleClickSignUp = () => {
    history.push('/signup');
  };
  const handleClickLogIn = () => {
    history.push('/signin');
  };

  const [form_data, setFormData] = useState('');

  function login(event) {
    axios({
      method: 'POST',
      url: '/login',
      data: {
        username: form_data.username,
        password: form_data.password,
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
        <Image alt={'Login Image'} objectFit={'scale-down'} src={loginPhoto} />
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
              bg="#c7d0d8"
              borderRadius="5px 0 0px 5px"
              p={3}
              onClick={handleClickSignUp}
              w={'50%'}
              h={'97%'}
              _hover={{ bg: '#D6BCFA' }}
            >
              <Heading fontSize={'xl'}>Sign Up</Heading>
            </Box>
            <Box
              as="button"
              bg="#a69db2"
              borderRadius="0px 5px 5px 0px"
              p={3}
              onClick={handleClickLogIn}
              w={'50%'}
              _hover={{ bg: '#D6BCFA' }}
              borderColor={'white'}
              borderWidth={3}
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
              <FormControl isRequired>
                <Input
                  mb={1}
                  id="username"
                  onChange={handleChange}
                  value={form_data.username}
                  borderColor={'#330662'}
                  maxW="200px"
                  type="text"
                  placeholder="NetID"
                  color={'#330662'}
                  _placeholder={{ color: '#330662' }}
                  borderWidth={'2px'}
                />
              </FormControl>
              <FormControl isRequired>
                <br />
                <Input
                  id="password"
                  onChange={handleChange}
                  value={form_data.password}
                  borderColor={'#330662'}
                  maxW="200px"
                  type="password"
                  placeholder="Password"
                  color={'#330662'}
                  _placeholder={{ color: '#330662' }}
                  borderWidth={'2px'}
                />
              </FormControl>
            </Stack>

            <Stack spacing={6} align={'center'}>
              <Button
                onClick={login}
                borderRadius="md"
                bg="#330662"
                color="white"
                px={20}
                fontSize={20}
                maxW="150px"
                h="45px"
                _hover={{ bg: '#7b5aa6' }}
              >
                SIGN IN
              </Button>
            </Stack>

            <Stack>
              <Text fontSize={'x1'} color={'black'} fontWeight={'bold'}>
                Forget your password?
              </Text>
              <Link href="/password_reset" color={'black'} fontWeight={'bold'}>
                {' '}
                <Text as="u">Reset your password</Text>{' '}
              </Link>
            </Stack>
          </Stack>
        </Box>
      </Flex>
    </Stack>
  );
}
