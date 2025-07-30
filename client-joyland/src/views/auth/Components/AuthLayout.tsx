import { Container } from '@mantine/core';

import { Outlet } from 'react-router-dom';
import authLayout from '../styles/authLayout.module.scss';

const AuthLayout = () => {
  return (
    <Container
      fluid
      className={`${authLayout.background} ${authLayout.container}`}
    >
      <Outlet />
    </Container>
  );
};

export default AuthLayout;