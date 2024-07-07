import { AppShell } from '@mantine/core';
import React from 'react';
import layout from '../../styles/layout.module.scss';

interface navProps {
  open: boolean;
  toggle: () => void;
}

const Navbar: React.FC<navProps> = () => {
  return <AppShell.Navbar className={layout.navbar}>nav</AppShell.Navbar>;
};

export default Navbar;
