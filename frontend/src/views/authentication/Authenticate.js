import {
  Button,  Flex,  FormControl, Heading, Input, Link,  Stack,  Image, Text, Box,
} from '@chakra-ui/react';
import loginPhoto from '../../assets/images/login_photo.jpg';

export default function LogInPage() {
  return (
    <Stack minH={'10vh'} direction={{ base: 'column', md: 'row' }}  bgColor={'#330662'}>
      <Flex flex={1}>
        <Image
          alt={'Login Image'}
          objectFit={'cover'}
          src={loginPhoto}
        />
      </Flex>

      
      <Flex p={8} flex={1} align={'center'} justify={'center'}>
        <Box bg='white' w='100%' p={0} align={'center'} borderRadius='lg'>

          <Stack color={'black'} >       
            <Box bg='#a69db2' borderRadius='lg' p={3}>
              <Heading fontSize={'xl'}>Log In</Heading>
            </Box>
          </Stack>

          <Stack spacing={4} w={'full'} maxW={'md'} color={'black'} bg='white' p={6} borderRadius='lg'>


            <Stack align={'center'}>
            <FormControl id="netId" borderColor={'#330662'} maxW='200px'>
              <Input type="text"  placeholder='NetID' color={'#330662'} _placeholder={{ color: '#330662' }} />
            </FormControl>
            <FormControl id="password" borderColor={'#330662'} maxW='200px'>
              <Input type="password" placeholder='Password' color={'#330662'} _placeholder={{ color: '#330662' }}/>
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
