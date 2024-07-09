import React from 'react';
import '@mantine/core/styles.css';
import {
  Affix,
  AppShell,
  Button,
  MantineProvider,
  Transition,
} from '@mantine/core';
import theme from '../theme';
import { useDisclosure, useWindowScroll } from '@mantine/hooks';
import AppHeader from './Components/Header/AppHeader';
import Navbar from './Components/Navbar/Navbar';
import AppFooter from './Components/Footer/AppFooter';
import layout from './styles/layout.module.scss';
import { Outlet } from 'react-router-dom';
import { FaArrowUpLong } from 'react-icons/fa6';

const AppLayout: React.FC = () => {
  const [open, { toggle }] = useDisclosure();
   const [scroll, scrollTo] = useWindowScroll();

  return (
    <MantineProvider theme={theme} defaultColorScheme={'auto'}>
      <AppShell
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
          <Affix position={{ bottom: 5, right: 20 }}>
            <Transition transition='slide-up' mounted={scroll.y > 0}>
              {(transitionStyles) => (
                <Button
                  size='xs'
                  leftSection={<FaArrowUpLong width={16} />}
                  style={transitionStyles}
                  onClick={() => scrollTo({ y: 0 })}
                >
                  Scroll to top
                </Button>
              )}
            </Transition>
          </Affix>
          <Outlet />
        </AppShell.Main>
        <AppFooter />
      </AppShell>
    </MantineProvider>
  );
};

export default AppLayout;
