import {
  Stack,
  Flex,
  VStack,
  Image,
  Text,
  useBreakpointValue,
  useColorModeValue,
} from '@chakra-ui/react';

import dark_bg from '../../assets/images/nyu_night.jpg';
import light_bg from '../../assets/images/nyu_day.png';
import dark_logo from '../../assets/images/full_dark.png';
import light_logo from '../../assets/images/full_light.png';

export default function HomePage() {
  const bg = useColorModeValue(light_bg, dark_bg);
  const logo = useColorModeValue(dark_logo, light_logo);
  const mask = useColorModeValue(
    'linear(whiteAlpha.700, whiteAlpha.700, whiteAlpha.700)',
    'linear(blackAlpha.700, blackAlpha.700, blackAlpha.700)'
  );
  return (
    <Flex
      w={'100vw'}
      h={'88vh'}
      backgroundImage={bg}
      backgroundSize={'cover'}
      backgroundPosition={'center center'}
    >
      <VStack
        w={'full'}
        align={'center'}
        justify={'center'}
        px={useBreakpointValue({ base: 4, md: 8 })}
        bgGradient={mask}
      >
        <Stack maxW={'2xl'} align={'center'} spacing={6}>
          <Image src={logo} />
          
          <Text fontSize="3xl" align={'center'}>
            An all-in-one place for NYU students to connect!
          </Text>
        </Stack>
      </VStack>
    </Flex>
  );
}
