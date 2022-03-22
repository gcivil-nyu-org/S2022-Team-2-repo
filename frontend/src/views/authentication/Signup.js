import {
    Button,
    Checkbox,
    Flex,
    FormControl,
    FormLabel,
    Heading,
    Input,
    Link,
    Stack,
    HStack,
    VStack,
    Image,
    Box,
  } from '@chakra-ui/react';
  import loginphoto from '../../assets/images/login.jpg';
  import { useHistory } from "react-router-dom/cjs/react-router-dom.min";
 
  export default function Signup() {
    const history=useHistory();
    const handleClickSignUp = () => {
      history.push('/Signup');
    }
    const handleClickLogIn = () => {
      history.push('/login');
    }
    return (
      <Stack
      height={'865px'}
    //   minH={'10vh'}
        direction={{ base: 'column', md: 'row' }}
        bgColor={'#330662'}
      >
          
        <Flex flex={1} w='100%' height='100%' >
          <Image width='100%' height='860px'  alt={'SignUp Image'} objectFit={'fill'} src={loginphoto}   />
        </Flex>
        
        <Flex
          p={8}
          flex={1}
          align={'center'}
          justify={'center'}
          bgColor={'#230542'}
          >
          <Box bg="white" h='48%' w='50%' p={0} color="black" borderRadius="lg">

          <Flex color={'black'} >       
            <Box as='button' borderColor={'white'} borderWidth={3}   bg='#a69db2' borderRadius='5px 0px 0px 5px' p={3} onClick={handleClickSignUp} w={'50%'}_hover={{ bg:'#D6BCFA'}}>
              <Heading fontSize={'xl'}>Sign Up</Heading>
            </Box>
            <Box as='button' bg='#c7d0d8' borderRadius='0px 5px 5px 0px' p={3} onClick={handleClickLogIn} w={'50%'}_hover={{ bg:'#D6BCFA'}}>
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
                <FormControl id="netid" border={'#57068c'}>
                  <Input
                    borderWidth={'2px'}
                    type="text"
                    padding='8px'
                    height="100%"
                    placeholder="NetID"
                    _placeholder={{ color: '#57068c' }}
                  />
                </FormControl>
                <FormControl id="Name" border={'#57068c'}>
                  <Input
                    borderWidth={'2px'}
                    height="100%"
                    width="40%"
                    type="text"
                    padding='8px'
                    placeholder="FirstName"
                    _placeholder={{ color: '#57068c' }}
                  />
                  <Input
                    borderWidth={'2px'}
                    marginLeft='5px'
                    padding='8px'
                    height="100%"
                    width="15%"
                    type="text"
                    placeholder="MI"
                    _placeholder={{ color: '#57068c' }}
                  />
                  <Input
                    borderWidth={'2px'}
                    width="40%"
                    height="100%"
                    ml="5px"
                    padding='8px'
                    type="text"
                    placeholder="LastName"
                    _placeholder={{ color: '#57068c' }}
                  />
                </FormControl>
                <FormControl
                  id="password"
                  border={'#57068c'}
                  borderWidth="-moz-initial"
                >
                  <Input
                    borderWidth={'2px'}
                    type="password"
                    placeholder="Password"
                    padding='8px'
                    height="100%"
                    _placeholder={{ color: '#57068c' }}
                  />
                </FormControl>
                <FormControl id="reset_password" border={'#57068c'}>
                  <Input
                    borderWidth={'2px'}
                    type="password"
                    placeholder="Retype Password"
                    padding='8px'
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