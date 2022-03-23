import {
    Slider,
    SliderTrack,
    SliderFilledTrack,
    SliderThumb,
    SliderMark,
    Box,
  } from '@chakra-ui/react'

export default function slideBar() {
    const boxSize='30%';
    const max=5;
    const min=1;
    const defaultValue=(max+min)/2;

    return(
        <Box w={boxSize}>
            <Slider aria-label='slider-ex-1' min={min} max={max} defaultValue={defaultValue} step={1} colorScheme={'purple'} onChangeEnd={(value)=>{console.log(value)}}>
                <SliderTrack>
                    <SliderFilledTrack />
                </SliderTrack>
                <SliderThumb />
            </Slider>
        </Box>
    );
}