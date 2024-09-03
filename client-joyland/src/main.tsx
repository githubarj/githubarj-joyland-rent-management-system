import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.tsx';
import './scss/index.scss';
import '@mantine/dates/styles.css';
import { MantineProvider } from '@mantine/core';
import theme from './theme.ts';


ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <MantineProvider theme={theme} defaultColorScheme={'auto'}>
      <App />
    </MantineProvider >
  </React.StrictMode>
);
