import {
  Combobox,
  Flex,
  Input,
  InputBase,
  Paper,
  Text,
  useCombobox,
} from '@mantine/core';
import React, { useState } from 'react';
import SearchTenant from '../../../../utils/components/SearchTenant';

const InvoiceTo: React.FC = () => {
  return (
    <Flex className='justify-between'>
      <SearchTenant />
      <div className='flex flex-col'>
        <Text>House No: a1</Text>
        <Text>John Doe</Text>

        <Text> 07234786</Text>
        <Text>john.doe@gmail.com</Text>
      </div>
    </Flex>
  );
};

export default InvoiceTo;
