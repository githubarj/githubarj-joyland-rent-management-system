import {
  AppShell,
  Center,
  Flex,
  Image,
  Title,
} from '@mantine/core';
import React from 'react';
import layout from '../../styles/layout.module.scss';
import freelance from '../../assets/freeLance.png';
import { TbLayoutSidebarLeftExpandFilled } from 'react-icons/tb';
import Navlinks from './Navlinks';

interface navProps {
  open: boolean;
  toggle: () => void;
}

const Navbar: React.FC<navProps> = ({ toggle, open }) => {
  return (
    <AppShell.Navbar px={'sm'} className={layout.navbar}>
      <AppShell.Section h={55}>
        <Flex align={'center'} mih={'100%'} gap={'md'} justify={'center'}>
          <Image src={freelance} fit='contain' h={'xl'} />{' '}
          <Title order={1}>Joyland</Title>
          <Center hiddenFrom='xs' inline style={{ marginLeft: 'auto' }}>
            <TbLayoutSidebarLeftExpandFilled
              data-open={!open}
              className={layout.icon}
              size={32}
              onClick={toggle}
            />
          </Center>
        </Flex>
      </AppShell.Section>
      <Navlinks />
      <AppShell.Section h={45}>

      </AppShell.Section>
    </AppShell.Navbar>
  );
};

export default Navbar;
