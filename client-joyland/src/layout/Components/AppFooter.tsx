import { AppShell } from '@mantine/core';
import React from 'react';
import layout from '../styles/layout.module.scss'

const AppFooter: React.FC = () => {
  return <AppShell.Footer className={layout.footer} >footer</AppShell.Footer>;
};

export default AppFooter;
