import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.tsx';

// styling files
import './scss/index.scss';
import '@mantine/dates/styles.css';
import '@mantine/notifications/styles.css';
import { Notifications } from '@mantine/notifications';

import { MantineProvider } from '@mantine/core';
import theme from './theme.ts';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <MantineProvider theme={theme} defaultColorScheme={'auto'}>
    <Notifications position="top-right" />
    <App />
  </MantineProvider>
);
