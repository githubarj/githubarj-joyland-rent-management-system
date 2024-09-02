import {
  TextInput,
  PasswordInput,
  Checkbox,
  Anchor,
  Paper,
  Title,
  Text,
  Container,
  Group,
  Button,
} from '@mantine/core';
import React from 'react';
import useCustomNavigation from '../../../hooks/useCustomNavigation';

const Login: React.FC = () => {
  const { goTo } = useCustomNavigation();
  return (
    <Container size={540} >
      <Title ta="center" > Joyland </Title>
      <Text c="dimmed" size="sm" ta="center" mt={5}>
        Welcome to your rent management system &#128075;
      </Text>

      <Paper withBorder shadow="md" p={30} mt={30} radius="md">
        <TextInput label="Email" placeholder="Email" required />
        <PasswordInput label="Password" placeholder="Your password" required mt="md" />
        <Group justify="space-between" mt="lg">
          <Checkbox label="Remember me" />
          <Anchor onClick={() => goTo({ to: '/forgot-password' })} component="button" size="sm">
            Forgot password?
          </Anchor>
        </Group>
        <Button fullWidth mt="xl">
          Log in
        </Button>
      </Paper>
    </Container>
  );
}

export default Login
