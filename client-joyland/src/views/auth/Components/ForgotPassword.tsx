import {
  Paper,
  Title,
  Text,
  TextInput,
  Button,
  Container,
  Anchor,
  Center,
  Box,
  rem,
  Stack,
} from '@mantine/core';
import { IconArrowLeft } from '@tabler/icons-react';
import React from 'react';
import useCustomNavigation from '../../../hooks/useCustomNavigation';

const ForgotPassword: React.FC = () => {
  const { goTo } = useCustomNavigation()
  return (
    <Container size={460} my={30}>
      <Title ta={'center'} >
        Forgot your password?
      </Title>
      <Text c="dimmed" fz="sm" ta="center">
        Enter your email to get a reset link
      </Text>

      <Paper withBorder shadow="md" p={30} radius="md" mt="xl">
        <TextInput label="Your email" placeholder="Email" required />
        <Stack ta={'center'} mt="lg">
          <Button >Reset password</Button>
          <Anchor c="dimmed" onClick={() => goTo({ to: "/login" })} size="sm">
            <Center inline>
              <IconArrowLeft style={{ width: rem(12), height: rem(12) }} stroke={1.5} />
              <Box ml={5}>Back to the login page</Box>
            </Center>
          </Anchor>
        </Stack>
      </Paper>
    </Container>
  );
}

export default ForgotPassword 
