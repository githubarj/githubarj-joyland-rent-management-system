import { AppShell, Flex, Group } from '@mantine/core';
import React from 'react';
import layout from '../../styles/layout.module.scss';
import { TbLayoutSidebarLeftExpandFilled } from 'react-icons/tb';
import ThemeSwitch from './ThemeSwitch';
import Notifications from './Notifications';
import UserMenu from './UserMenu';

interface headerProps {
  open: boolean;
  toggle: () => void;
}

const AppHeader: React.FC<headerProps> = ({ open, toggle }) => {
  return (
    <AppShell.Header px={'sm'} className={layout.header}>
      <Flex mih='100%' justify='space-between' align='center'>
        <TbLayoutSidebarLeftExpandFilled
          data-open={!open}
          className={layout.icon}
          size={32}
          onClick={toggle}
        />
        <Group>
          <ThemeSwitch />
          <Notifications />
          <UserMenu />
        </Group>
      </Flex>
    </AppShell.Header>
  );
};

export default AppHeader;
