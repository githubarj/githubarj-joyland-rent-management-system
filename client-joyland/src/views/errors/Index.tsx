import { Button, Center, Container, Stack, Tooltip } from '@mantine/core';
import React from 'react';
import Error404 from './Components/Error404';
import error from '../errors/assets/cuate.png';
import useCustomNavigation from '../../hooks/useCustomNavigation';

const ErrorPage: React.FC = () => {
  const { goBack } = useCustomNavigation();
  return (
    <Stack mt={30} align='center' className={error}>
      <Error404 />
      <Tooltip
        label='Go back to the previos page'
        openDelay={500}
        withArrow
        mt={20}
        offset={-10}
        position='bottom'
        arrowPosition='center'
      >
        <Button w={'fit-content'} onClick={goBack}>
          Go back
        </Button>
      </Tooltip>
    </Stack>
  );
};

export default ErrorPage;
