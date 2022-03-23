import {
  Button,
  Flex,
  FormControl,
  Heading,
  Input,
  Stack,
  Box,
} from '@chakra-ui/react';

export default function PasswordReset() {
  return (
    <Stack
      minH={'100vh'}
      direction={{ base: 'column', md: 'row' }}
      bgColor={'#330662'}
    >
      <Flex p={8} flex={1} align={'center'} justify={'center'}>
        <Box bg="white" w="40%" p={0} align={'center'} borderRadius="lg">
          <Box bg="#a69db2" borderRadius="5px" p={3} color={'black'}>
            <Heading fontSize={'xl'}>Reset Password</Heading>
          </Box>

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
              <FormControl>
                <Input
                  mb={1}
                  id="netIdPwReset"
                  borderColor={'#330662'}
                  maxW="200px"
                  type="text"
                  placeholder="NetID"
                  color={'#330662'}
                  _placeholder={{ color: '#330662' }}
                  borderWidth={'2px'}
                />
              </FormControl>
            </Stack>

            <Stack spacing={6} align={'center'}>
              <Button
                borderRadius="md"
                bg="#330662"
                color="white"
                px={20}
                fontSize={20}
                maxW="300px"
                h="45px"
                _hover={{ bg: '#7b5aa6' }}
              >
                Sent Password Reset Email
              </Button>
            </Stack>
          </Stack>
        </Box>
      </Flex>
    </Stack>
  );
}
