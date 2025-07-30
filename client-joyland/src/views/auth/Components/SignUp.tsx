import {
  TextInput,
  PasswordInput,
  Checkbox,
  Anchor,
  Paper,
  Title,
  Text,
  Container,
  Button,
  Flex,
} from '@mantine/core';

import { useForm } from '@mantine/form';

import { Progress } from '@mantine/core';
import { useMemo } from 'react';
import useCustomNavigation from '../../../hooks/useCustomNavigation';
import { showNotification } from '@mantine/notifications';
import { handleRegister } from '../../../api/services/__auth.service';
import { AxiosError } from 'axios';
import {
  getPasswordStrength,
  passwordStrengthColor,
} from '../../../utils/functions/auth';

const SignUp: React.FC = () => {
  const { goTo } = useCustomNavigation();

  const form = useForm({
    initialValues: {
      username: '',
      firstName: '',
      lastName: '',
      password: '',
      confirmPassword: '',
      terms: false,
    },
    validate: {
      username: (value) =>
        /^\S+@\S+\.\S+$/.test(value) ? null : 'Invalid email format',
      firstName: (value) =>
        value.trim().length > 0 ? null : 'First name is required',
      lastName: (value) =>
        value.trim().length > 0 ? null : 'Last name is required',
      password: (value) =>
        value.length >= 8 && /[0-9]/.test(value) && /[!@#$%^&*]/.test(value)
          ? null
          : 'Password must be at least 8 characters and include a number and special character',
      confirmPassword: (value, values) =>
        value === values.password ? null : 'Passwords do not match',
      terms: (value) => (value ? null : 'You must agree to the terms'),
    },
  });

  const handleSubmit = form.onSubmit(async (values) => {
    try {
      await handleRegister({
        email: values.username,
        username: values.username,
        first_name: values.firstName,
        last_name: values.lastName,
        password: values.password,
      });
      // work on what happens after user registration
    } catch (err) {
      const error = err as AxiosError<{ message?: string }>;
      if (error?.response?.status !== 500 && error?.response?.status !== 401) {
        showNotification({
          title: 'Registration Failed',
          message: error?.response?.data?.message || 'Something went wrong',
          color: 'red',
        });
      }
    }
  });

  const passwordStrength = useMemo(
    () => getPasswordStrength(form.values.password),
    [form.values.password]
  );
  return (
    <Container size={540}>
      <Title ta='center'> Odissys </Title>
      <Text c='dimmed' size='sm' ta='center' mt={5}>
        Enter your details to get an account &#128075;
      </Text>

      <Paper
        withBorder
        shadow='md'
        p={30}
        mt={30}
        radius='md'
        style={{ minWidth: 400 }}
      >
        <form onSubmit={handleSubmit}>
          <TextInput
            label='Email'
            placeholder='Email'
            required
            {...form.getInputProps('username')}
          />
          <TextInput
            label='First Name'
            placeholder='First Name'
            required
            mt='md'
            {...form.getInputProps('firstName')}
          />
          <TextInput
            label='Last Name'
            placeholder='Last Name'
            required
            mt='md'
            {...form.getInputProps('lastName')}
          />
          <PasswordInput
            label='Password'
            placeholder='Your password'
            required
            mt='md'
            {...form.getInputProps('password')}
          />

          {form.values.password.length > 0 && (
            <Progress
              value={passwordStrength}
              color={passwordStrengthColor(passwordStrength)}
              size='sm'
              mt={5}
              radius='xl'
            />
          )}
          <PasswordInput
            label='Confirm Password'
            placeholder='Confirm your password'
            required
            mt='md'
            {...form.getInputProps('confirmPassword')}
          />

          <Flex direction='column' justify='space-between' mt='lg'>
            <Checkbox
              label='I agree to privacy policy & terms'
              {...form.getInputProps('terms', { type: 'checkbox' })}
            />
          </Flex>
          <Button fullWidth mt='md' mb='md' type='submit'>
            Sign up
          </Button>
        </form>
        <Flex justify={'center'}>
          <Anchor onClick={() => goTo({ to: '/login' })} size='sm'>
            Sign in instead
          </Anchor>
        </Flex>
      </Paper>
    </Container>
  );
};

export default SignUp;
