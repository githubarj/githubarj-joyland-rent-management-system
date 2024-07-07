import { IoMdNotificationsOutline } from 'react-icons/io';
import { Indicator, Tooltip, UnstyledButton } from '@mantine/core';
import React from 'react';
import layout from '../../styles/layout.module.scss'

const Notifications: React.FC = () => {
  return (
    <Tooltip
      label='Notifications'
      openDelay={500}
      transitionProps={{ transition: 'pop' }}
    >
      <UnstyledButton>
        <Indicator
          size={10}
          className={layout.centerIcons}
          offset={5.5}
          withBorder
          color='red'
        >
          <IoMdNotificationsOutline size={24} />
        </Indicator>
      </UnstyledButton>
    </Tooltip>
  );
};

export default Notifications;
