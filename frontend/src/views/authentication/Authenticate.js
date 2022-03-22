import {
  Button,  Flex,  FormControl, Heading, Input, Link,  Stack,  Image, Text, Box,
} from '@chakra-ui/react';
import { useHistory } from "react-router-dom/cjs/react-router-dom.min";

import loginPhoto from '../../assets/images/login_photo.jpg';

export default function LogInPage() {
  const history=useHistory();
  const handleClickSignUp = () => {
    history.push('/signup');
  }
  const handleClickLogIn = () => {
    history.push('/login');
  }

  return (
    
    <Stack minH={'100vh'} direction={{ base: 'column', md: 'row' }}  bgColor={'#330662'}>

      <Flex flex={1} maxH={'100vh'}>
        <Image
          alt={'Login Image'}
          objectFit={'cover'}
          src={loginPhoto}
        />
      </Flex>

      
      <Flex p={8} flex={1} align={'center'} justify={'center'} >
        <Box bg='white' w='50%' p={0} align={'center'} borderRadius='lg'>

          <Flex color={'black'} >       
            <Box as='button' bg='#c7d0d8' borderRadius='5px 0 0px 5px' p={3} onClick={handleClickSignUp} w={'50%'}_hover={{ bg:'#D6BCFA'}}>
              <Heading fontSize={'xl'}>Sign Up</Heading>
            </Box>
            <Box as='button' bg='#a69db2' borderRadius='0px 5px 5px 0px' p={3} onClick={handleClickLogIn} w={'50%'}_hover={{ bg:'#D6BCFA'}}>
              <Heading fontSize={'xl'}>Log In</Heading>
            </Box>
          </Flex>

          <Stack spacing={4} w={'full'} maxW={'md'} color={'black'} bg='white' p={6} borderRadius='lg'>

            <Stack align={'center'}>
              <FormControl >
                <Input mb={1} id="netId" borderColor={'#330662'} maxW='200px' type="text"  placeholder='NetID' color={'#330662'} _placeholder={{ color: '#330662' }} borderWidth={'2px'} />
                <br />
                <Input  id="password" borderColor={'#330662'} maxW='200px' type="password" placeholder='Password' color={'#330662'} _placeholder={{ color: '#330662' }} borderWidth={'2px'}/>
              </FormControl>
            </Stack>

            <Stack spacing={6} align={'center'}>
              
                <Button borderRadius='md' bg='#330662' color='white' px={20} fontSize={20} maxW='150px' h='45px' _hover={{ bg:'#7b5aa6'}}>
                  SIGN IN
                </Button>
            </Stack>

            <Stack>
              <Text fontSize={'x1'} color={'black'} fontWeight={'bold'}>Forget your password?</Text>                       
              <Link href="/" color={'black'} fontWeight={'bold'} > <Text as ='u'>Reset your password</Text> </Link>
            </Stack>

          </Stack>

        </Box>
      </Flex>

    </Stack>
  );
}
