import { AppShell, Flex, Text } from '@mantine/core';
import React from 'react';
import layout from '../../styles/layout.module.scss';
import { FcLike } from 'react-icons/fc';

const AppFooter: React.FC = () => {
  return (
    <AppShell.Footer className={layout.footer} px={'sm'}>
      <Flex align={'center'} gap={'sm'}>
        <Text>
          Made with <FcLike /> by
        </Text>
        <Text
          component='a'
          href='https://githuba.netlify.app/'
          target='_blank'
          size='l'
          fw={400}
          variant='gradient'
          gradient={{ from: 'teal', to: 'pink', deg: 152 }}
        >
          GithubaRJ
        </Text>
      </Flex>
    </AppShell.Footer>
  );
};

export default AppFooter;
