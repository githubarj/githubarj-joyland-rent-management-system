import { Divider, Flex, Image, Paper } from '@mantine/core';
import React from 'react';
import FormHeader from './FormHeader';

const InvoiceForm: React.FC = () => {
  return (
    <Paper shadow='xs' className='flex-1  p-4'>
      <form action=''>
        <FormHeader />

        <Divider my={'xl'} />
      </form>
    </Paper>
  );
};

export default InvoiceForm;
