import React from 'react';
import '@mantine/core/styles.css';
import { MantineProvider } from '@mantine/core';
import theme from '../theme';

const AppLayout: React.FC = () => {
  return (
    <MantineProvider theme={theme} defaultColorScheme='light'>
      <div>Hello </div>
    </MantineProvider>
  );
};

export default AppLayout;
