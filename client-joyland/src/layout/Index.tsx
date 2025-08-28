import React, { useEffect } from 'react';
import '@mantine/core/styles.css';
import {
  Affix,
  AppShell,
  Button,
  Center,
  Flex,
  Loader,
  Transition,
} from '@mantine/core';
import { useDisclosure, useWindowScroll } from '@mantine/hooks';
import AppHeader from './Components/Header/AppHeader';
import Navbar from './Components/Navbar/Navbar';
import AppFooter from './Components/Footer/AppFooter';
import layout from './styles/layout.module.scss';
import { Outlet } from 'react-router-dom';
import { FaArrowUpLong } from 'react-icons/fa6';
import { fetchCurrentUser } from '../api/services/_auth.service';
import { useLoadingStore } from '../store/useLoadingStore';

const AppLayout: React.FC = () => {
  const [open, { toggle }] = useDisclosure();
  const [scroll, scrollTo] = useWindowScroll();
  const { loading } = useLoadingStore();

  useEffect(() => {
    const initUser = async () => {
      await fetchCurrentUser();
    };

    initUser();
  }, []);

  return (
    <AppShell
      header={{ height: 55 }}
      footer={{ height: 45 }}
      layout='alt'
      withBorder={true}
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
        {loading['user'] ? (
          <Center h='100%' style={{ minHeight: '80vh' }}>
            <Loader size={64} />
          </Center>
        ) : (
          <Outlet />
        )}
      </AppShell.Main>
      <AppFooter />
    </AppShell>
  );
};

export default AppLayout;
