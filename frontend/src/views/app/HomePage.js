import {
  Stack,
  Flex,
  VStack,
  useBreakpointValue,
  useColorModeValue,
  useColorMode,
} from '@chakra-ui/react';

import dark_bg from '../../assets/images/nyu_night.jpg';
import light_bg from '../../assets/images/nyu_day.png';

export default function HomePage() {
  const bg = useColorModeValue(light_bg, dark_bg)
  return (
    <Flex
      w={'full'}
      h={'full'}
      backgroundImage={bg}
      backgroundSize={'cover'}
      backgroundPosition={'center center'}
    >
      <VStack
        w={'full'}
        justify={'center'}
        px={useBreakpointValue({ base: 4, md: 8 })}
        bgGradient={'linear(blackAlpha.700, blackAlpha.700, blackAlpha.700)'}
      >
        <Stack maxW={'2xl'} align={'flex-start'} spacing={6}>

        </Stack>
      </VStack>
    </Flex>
  );
}
