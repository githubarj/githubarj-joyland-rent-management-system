import {
  Paper,
  Title,
  Text,
  Button,
  Container,
  Anchor,
  Center,
  Box,
  rem,
  PasswordInput,
  Stack,
} from '@mantine/core';
import { IconArrowLeft } from '@tabler/icons-react';
import React from 'react';
import useCustomNavigation from '../../../hooks/useCustomNavigation';

const ResetPassword: React.FC = () => {
  const { goTo } = useCustomNavigation()
  return (
    <Container size={460} my={30}>
      <Title ta={'center'} >
        Reset Password &#128274;
      </Title>
      <Text c="dimmed" fz="sm" ta="center">
        Your new password must be different  from <br />previously used passwords
      </Text>

      <Paper withBorder shadow="md" p={30} radius="md" mt="xl">
        <PasswordInput label="New Password" placeholder="New password" required mt="md" />
        <PasswordInput label="Confirm Password" placeholder="Confirm password" required mt="md" />
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

export default ResetPassword 
