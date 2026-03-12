import { Tooltip, UnstyledButton, useMantineColorScheme } from '@mantine/core';
import React from 'react';
import { MdOutlineDarkMode, MdOutlineLightMode } from 'react-icons/md';
import layout from '../../styles/layout.module.scss';

const ThemeSwitch: React.FC = () => {
  const { toggleColorScheme, colorScheme } = useMantineColorScheme();

  return (
    <Tooltip
      label='Switch themes'
      openDelay={500}
      transitionProps={{ transition: 'pop' }}
    >
      <UnstyledButton className={layout.centerIcons}>
        {colorScheme === 'dark' ? (
          <MdOutlineLightMode size={24} onClick={toggleColorScheme} />
        ) : (
          <MdOutlineDarkMode size={24} onClick={toggleColorScheme} />
        )}
      </UnstyledButton>
    </Tooltip>
  );
};

export default ThemeSwitch;
