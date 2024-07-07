import { Avatar, Indicator } from '@mantine/core';
import React from 'react';

const UserMenu : React.FC = () => {
  return (
    <Indicator offset={6} color='green' position='bottom-end' size={12} withBorder>
      <Avatar color='cyan' radius='xl'>
        RG
      </Avatar>
    </Indicator>
  );
};

export default UserMenu;
