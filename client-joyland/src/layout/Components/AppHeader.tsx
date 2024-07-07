import { AppShell, Center } from '@mantine/core';
import React from 'react';
import layout from '../styles/layout.module.scss';
import { TbLayoutSidebarLeftExpandFilled } from 'react-icons/tb';

interface headerProps {
  open: boolean;
  toggle: () => void;
}

const AppHeader: React.FC<headerProps> = ({ open, toggle }) => {
  return (
    <AppShell.Header className={layout.header}>
      <Center inline>
        <TbLayoutSidebarLeftExpandFilled
          data-open={open}
          className={layout.icon}
          size={32}
          onClick={toggle}
        />
        header
      </Center>
    </AppShell.Header>
  );
};

export default AppHeader;
