import { Container } from '@mantine/core';
import SearchInvoices from './SearchInvoices';
import InvoiceTable from '../Components/InvoiceTable'
import React from 'react';

const InvoiceList: React.FC = () => {
  return (
    <Container fluid>
      <SearchInvoices />
      <InvoiceTable />
    </Container>
  );
};

export default InvoiceList;
