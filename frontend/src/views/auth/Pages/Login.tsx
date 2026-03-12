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
import { APP_NAME } from '../../../utils/constants/config';
import { useForm } from '@mantine/form';
import { login } from '../../../api/services/_auth.service';
import { showNotification } from '@mantine/notifications';
import { useLoadingStore } from '../../../store/useLoadingStore';

const Login: React.FC = () => {
  const { goTo } = useCustomNavigation();
  const { loading } = useLoadingStore();

  const form = useForm({
    initialValues: {
      email: '',
      password: '',
    },
    validate: {
      email: (value) =>
        /^\S+@\S+\.\S+$/.test(value) ? null : 'Invalid email format',

      password: (value) =>
        value.length >= 8 && /[0-9]/.test(value) && /[!@#$%^&*]/.test(value)
          ? null
          : 'Password must be at least 8 characters and include a number and special character',
    },
  });

 const handleSubmit = form.onSubmit(async ({ email, password }) => {
   const res = await login({ email, password });
   if (res) {
     showNotification({
       title: 'Login successful',
       message: 'Welcome!',
     });
     goTo({ to: '/home' }); 
   }
 });

  return (
    <Container miw={400}>
      <Title ta='center'> {APP_NAME} </Title>
      <Text c='dimmed' size='sm' ta='center' mt={5}>
        Welcome to your rent management system &#128075;
      </Text>

      <Paper withBorder shadow='md' p={30} mt={30} radius='md'>
        <form onSubmit={handleSubmit}>
          <TextInput
            label='Email'
            placeholder='Email'
            required
            {...form.getInputProps('email')}
          />
          <PasswordInput
            label='Password'
            placeholder='Your password'
            required
            mt='md'
            {...form.getInputProps('password')}
          />
          <Group justify='space-between' mt='lg'>
            <Anchor
              onClick={() => goTo({ to: '/forgot-password' })}
              component='button'
              size='sm'
            >
              Forgot password?
            </Anchor>
          </Group>
          <Button loading={loading['login']} fullWidth mt='xl' type='submit'>
            Log in
          </Button>
        </form>
      </Paper>
    </Container>
  );
};

export default Login;
