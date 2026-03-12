import { createTheme, MantineTheme, } from '@mantine/core';

const theme = createTheme({
  fontFamily: 'Lato, sans-serif',
  black: '#676D75',
  colors: {
    'text-grey': [
      '#eaf8f8',
      '#e5e7ec',
      '#cacdd0',
      '#aeb1b6',
      '#95999e',
      '#858a91',
      '#7d838b',
      '#6a7079',
      '#5c646d',
      '#4c5763',
    ],
  },
 
}) as MantineTheme;

export default theme;
