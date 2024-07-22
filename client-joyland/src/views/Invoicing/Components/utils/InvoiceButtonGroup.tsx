import { Button, Paper } from '@mantine/core';
import React from 'react';
import { VscSend } from 'react-icons/vsc';
import { MdOutlineAttachMoney } from 'react-icons/md';

const InvoiceButtonGroup: React.FC = () => {
  return (
    <Paper
      shadow='xs'
      p={10}
      w={'fit-content'}
      display={'flex'}
      style={{ flexDirection: 'column', gap: 10 }}
    >
      <Button variant='filled' leftSection={<VscSend />}>
        SEND INVOICE
      </Button>
      <Button variant='default'>EDIT INVOICE</Button>
      <Button
        variant='filled'
        color='green'
        leftSection={<MdOutlineAttachMoney />}
      >
        ADD PAYMENT
      </Button>
    </Paper>
  );
};

export default InvoiceButtonGroup;
