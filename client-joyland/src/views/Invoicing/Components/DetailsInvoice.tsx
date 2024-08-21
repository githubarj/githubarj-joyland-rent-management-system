import { Button, Container, Group } from '@mantine/core';
import React from 'react';
import InvoiceButtonGroup from './utils/InvoiceButtonGroup';
import InvoiceForm from './utils/InvoiceForm';
import { IoArrowBackOutline } from 'react-icons/io5';
import useCustomNavigation from '../../../hooks/useCustomNavigation';

const InvoicePage: React.FC = () => {
  const { goBack } = useCustomNavigation()
  return (
    <Container fluid className=' p-3  ' >
      <Group className='mb-2'>
        <Button variant='light' color={"red"} rightSection={<IoArrowBackOutline />} onClick={goBack} >
          Back
        </Button>
      </Group>
      <div className='w-full flex flex-col-reverse  sm:flex-row gap-4'>
        <InvoiceForm />
        <InvoiceButtonGroup />
      </div>
    </Container>
  );
};

export default InvoicePage;
