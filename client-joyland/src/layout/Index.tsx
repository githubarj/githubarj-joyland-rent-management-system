import React from 'react';
import '@mantine/core/styles.css';
import { AppShell, MantineProvider } from '@mantine/core';
import theme from '../theme';
import { useDisclosure } from '@mantine/hooks';
import AppHeader from './Components/AppHeader';
import Navbar from './Components/Navbar';
import AppFooter from './Components/AppFooter';
import layout from './styles/layout.module.scss';
import { Outlet } from 'react-router-dom';

const AppLayout: React.FC = () => {
  const [open, { toggle }] = useDisclosure();

  return (
    <MantineProvider theme={theme} defaultColorScheme='light'>
      <AppShell
        header={{ height: 45 }}
        footer={{ height: 45 }}
        layout='alt'
        withBorder={false}
        navbar={{
          width: 230,
          breakpoint: 'xs',
          collapsed: { mobile: !open, desktop: !open },
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
