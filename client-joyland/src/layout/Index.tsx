import React from 'react';
import '@mantine/core/styles.css';
import { AppShell, MantineProvider } from '@mantine/core';
import theme from '../theme';
import { useDisclosure } from '@mantine/hooks';
import AppHeader from './Components/Header/AppHeader';
import Navbar from './Components/Navbar/Navbar';
import AppFooter from './Components/Footer/AppFooter';
import layout from './styles/layout.module.scss';
import { Outlet } from 'react-router-dom';

const AppLayout: React.FC = () => {
  const [open, { toggle }] = useDisclosure();

  return (
    <MantineProvider theme={theme} defaultColorScheme={'auto'}>
      <AppShell
      padding={'sm'}
        header={{ height: 55 }}
        footer={{ height: 45 }}
        layout='alt'
        withBorder={false}
        navbar={{
          width: 200,
          breakpoint: 'xs',
          collapsed: { mobile: !open, desktop: open },
        }}
      >
        <AppHeader open={open} toggle={toggle} />
        <Navbar open={open} toggle={toggle} />
        <AppShell.Main className={layout.main}>
          <Outlet />
        </AppShell.Main>
        <AppFooter />
      </AppShell>
    </MantineProvider>
  );
};

export default AppLayout;
