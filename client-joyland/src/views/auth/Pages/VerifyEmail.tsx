import { Button, Container, Loader, Text, Title } from '@mantine/core';
import React, { useEffect } from 'react';
import useCustomNavigation from '../../../hooks/useCustomNavigation';
import { MdMarkEmailRead } from 'react-icons/md';
import { useParams } from 'react-router-dom';
import { verifyEmail } from '../../../api/services/_auth.service';
import { showNotification } from '@mantine/notifications';
import { useLoadingStore } from '../../../store/useLoadingStore';

const VerifyEmail: React.FC = () => {
  const { goTo } = useCustomNavigation();
  const { uid, token } = useParams();
  const { loading } = useLoadingStore();

  useEffect(() => {
    if (!uid || !token) {
      showNotification({
        title: 'An Error Occurred',
        message: 'Missing UID or verification token',
      });
    }

    const verify = async () => {
      const res = await verifyEmail(uid, token);
      if (!res) {
        console.error('Verification failed');
        // Optional: show UI feedback or redirect
      }
    };

    verify();
  }, [uid, token]);
  return (
    <Container
      miw={400}
      maw={500}
      style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}
    >
      {loading['verify-email'] ? (
        <Loader />
      ) : (
        <>
          
          <Title ta='center'>Email address verified</Title>
          <MdMarkEmailRead size={48} />
          <Text c='dimmed' size='sm' ta='center' mt={5}>
            Your email address has being confirmed and your account has been
            successfully created, you can now log in with your user details
          </Text>
          <Button mt={'md'} onClick={() => goTo({ to: '/login' })}>
            Back to login
          </Button>
        </>
      )}
    </Container>
  );
};

export default VerifyEmail;
