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
 
  export default function Signup() {
    return (
      <Stack
      height={'865px'}
    //   minH={'10vh'}
        direction={{ base: 'column', md: 'row' }}
        bgColor={'#330662'}
      >
          
        <Flex flex={1} w='100%' height='100%' >
          <Image width='100%' height='860px'  alt={'Login Image'} objectFit={'fill'} src={loginphoto}   />
        </Flex>
        
        <Flex
          p={8}
          flex={1}
          align={'center'}
          justify={'center'}
          bgColor={'#230542'}
          >
          <Box bg="white" w="50%" p={0} color="black" borderRadius="lg">
            <Stack spacing={4} w={'full'} maxW={'md'}>
              <Box  w='100%' bg="#a69db2" borderRadius="lg" p={3}>
                <Heading align={'center'} fontSize={'xl'}>
                  Sign Up
                </Heading>
              </Box>
            </Stack>
  
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
                    placeholder="NetID"
                    _placeholder={{ color: '#57068c' }}
                  />
                </FormControl>
                <FormControl id="Name" border={'#57068c'}>
                  <Input
                    borderWidth={'2px'}
                    width="50%"
                    type="text"
                    placeholder="FirstName"
                    _placeholder={{ color: '#57068c' }}
                  />
                  <Input
                    borderWidth={'2px'}
                    width="40%"
                    ml="10px"
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
                    _placeholder={{ color: '#57068c' }}
                  />
                </FormControl>
                <FormControl id="reset_password" border={'#57068c'}>
                  <Input
                    borderWidth={'2px'}
                    type="password"
                    placeholder="Retype Password"
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