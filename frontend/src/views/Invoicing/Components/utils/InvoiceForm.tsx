import { Divider, Paper } from '@mantine/core';
import React from 'react';
import FormHeader from './FormHeader';
import InvoiceTo from './InvoiceTo';
import InvoiceItem from './InvoiceItem';
import InvoiceFooter from './InvoiceFooter';
import Notes from './Notes';

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
        <InvoiceFooter />
        <Divider my={"xl"} />
        <Notes />
      </form>
    </Paper>
  )
};

export default InvoiceForm;
