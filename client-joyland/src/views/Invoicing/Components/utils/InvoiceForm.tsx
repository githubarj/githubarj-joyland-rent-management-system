import { Divider, Paper } from '@mantine/core';
import React from 'react';
import FormHeader from './FormHeader';
import InvoiceTo from './InvoiceTo';
import InvoiceItem from './InvoiceItem';

const InvoiceForm: React.FC = () => {
  return (
    <Paper shadow='xs' className='flex-1  p-4'>
      <form action=''>
        <FormHeader />
        <Divider my={'xl'} />
        <InvoiceTo />
        <Divider my={'xl'} />
        <InvoiceItem />
        <Divider my={"xl"} />
      </form>
    </Paper>
  )
};

export default InvoiceForm;
