import { Container } from '@mantine/core';
import React from 'react';
import InvoiceButtonGroup from './utils/InvoiceButtonGroup';

const DetailsInvoice: React.FC = () => {
  return (
    <Container fluid>
      <InvoiceButtonGroup />
    </Container>
  );
};

export default DetailsInvoice;
