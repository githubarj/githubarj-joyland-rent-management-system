import { Button, Paper } from '@mantine/core';
import React from 'react';
import { VscSend } from 'react-icons/vsc';
import { MdOutlineAttachMoney } from 'react-icons/md';
import { IoIosPrint } from 'react-icons/io';

const InvoiceButtonGroup: React.FC = () => {
  return (
    <Paper shadow='xs' p={10} w={'fit-content'} className='flex flex-row md:flex-col gap-2 flex-wrap '>
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
      <Button
        variant='filled'
        color='red'
        leftSection={<IoIosPrint />}
      >
        PRINT
      </Button>
    </Paper>
  );
};

export default InvoiceButtonGroup;
