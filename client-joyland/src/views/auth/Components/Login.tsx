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
import { useForm } from '@mantine/form';
import { handleLogin } from '../../../api/services/__auth.service';
import { showNotification } from '@mantine/notifications';
import { AxiosError } from 'axios';

const Login: React.FC = () => {
  const { goTo } = useCustomNavigation();

  const form = useForm({
    initialValues: {
      username: '',
      password: '',
    },
    validate: {
      username: (value) =>
        /^\S+@\S+\.\S+$/.test(value) ? null : 'Invalid email format',
      password: (value) =>
        /^(?=.*[A-Z])(?=.*\d).{8,}$/.test(value)
          ? null
          : 'Must contain 8+ chars, a number & uppercase letter',
    },
  });

  const handleSubmit = form.onSubmit(async ({ username, password }) => {
    try {
      const response = await handleLogin({
        username,
        password,
      });
      const { access, refresh } = response.data;
      localStorage.setItem('token', access);
      localStorage.setItem('refreshToken', refresh);
      goTo({ to: '/home' });
    } catch (err) {
      const error = err as AxiosError<{ message?: string }>;
      if (error?.response?.status !== 500 || 401) {
        showNotification({
          title: 'Registration Failed',
          message: error?.response?.data?.message || 'Something went wrong',
          color: 'red',
        });
      }
    }
  });

  return (
    <Container size={540}>
      <Title ta='center'> Joyland </Title>
      <Text c='dimmed' size='sm' ta='center' mt={5}>
        Welcome to your rent management system &#128075;
      </Text>

      <form onSubmit={handleSubmit}>
        <Paper withBorder shadow='md' p={30} mt={30} radius='md'>
          <TextInput
            label='Email'
            placeholder='Email'
            required
            {...form.getInputProps('username')}
          />
          <PasswordInput
            label='Password'
            placeholder='Your password'
            required
            mt='md'
            {...form.getInputProps('password')}
          />
          <Group justify='space-between' mt='lg'>
            <Checkbox label='Remember me' />
            <Anchor
              onClick={() => goTo({ to: '/forgot-password' })}
              component='button'
              size='sm'
            >
              Forgot password?
            </Anchor>
          </Group>
          <Button fullWidth mt='xl'>
            Log in
          </Button>
        </Paper>
      </form>
    </Container>
  );
};

export default Login;
