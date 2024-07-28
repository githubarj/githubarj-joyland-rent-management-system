import { Container } from '@mantine/core';
import React from 'react';
import InvoiceButtonGroup from './utils/InvoiceButtonGroup';
import InvoiceForm from './utils/InvoiceForm';

const DetailsInvoice: React.FC = () => {
  return (
    <Container fluid className='flex flex-col-reverse  sm:flex-row gap-4'>
      <InvoiceForm />
      <InvoiceButtonGroup />
    </Container>
  );
};

export default DetailsInvoice;