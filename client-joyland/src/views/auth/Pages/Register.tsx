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

import { APP_NAME } from '../../../utils/constants/config';
import { register } from '../../../api/services/_auth.service';
import { showNotification } from '@mantine/notifications';
import { useLoadingStore } from '../../../store/useLoadingStore';

const Register: React.FC = () => {
  const { goTo } = useCustomNavigation();
  const { loading } = useLoadingStore();

  const form = useForm({
    initialValues: {
      email: '',
      full_name: '',
      password: '',
      confirm_password: '',
    },
    validate: {
      email: (value) =>
        /^\S+@\S+\.\S+$/.test(value) ? null : 'Invalid email format',
      full_name: (value) =>
        value.trim().length > 0 ? null : 'First name is required',
      password: (value) =>
        value.length >= 8 && /[0-9]/.test(value) && /[!@#$%^&*]/.test(value)
          ? null
          : 'Password must be at least 8 characters and include a number and special character',
      confirm_password: (value, values) =>
        value === values.password ? null : 'Passwords do not match',
    },
  });

  const handleSubmit = form.onSubmit(async ({ email, full_name, password }) => {
    const res = await register({ email, full_name, password });
    if (res) {
      showNotification({
        title: 'User registration successful',
        message: res?.message,
        color: 'green',
      });
      goTo({ to: '/login' });
    }
  });

  return (
    <Container miw={400}>
      <Title ta='center'> {APP_NAME} </Title>
      <Text c='dimmed' size='sm' ta='center' mt={5}>
        Create an account to get started &#128075;
      </Text>

      <Paper withBorder shadow='md' p={30} mt={30} radius='md'>
        <form onSubmit={handleSubmit}>
          <TextInput
            label='Full Name'
            placeholder='Full Name'
            required
            {...form.getInputProps('full_name')}
          />

          <TextInput
            label='Email'
            placeholder='Email'
            required
            mt={'md'}
            {...form.getInputProps('email')}
          />
          <PasswordInput
            label='Password'
            placeholder='Your password'
            required
            mt='md'
            {...form.getInputProps('password')}
          />
          <PasswordInput
            label='Confirm password'
            placeholder='Confirm password'
            required
            mt='md'
            {...form.getInputProps('confirm_password')}
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
          <Button loading={loading['register']} fullWidth mt='xl' type='submit'>
            Register
          </Button>
        </form>
      </Paper>
    </Container>
  );
};

export default Register;
