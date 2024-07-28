import { Flex, Image, Text, Title } from '@mantine/core';
import React from 'react';
import freelance from '../../../../../public/assets/freeLance.png';
import { DatePickerInput } from '@mantine/dates';

const FormHeader: React.FC = () => {
  return (
    <Flex className='justify-between'>
      <div className='flex gap-2'>
        <Image src={freelance} fit='contain' h={'xl'} />
        <Title order={2}>Joyland</Title>
      </div>

      <div>
        <Title order={2}>Invoice #2345</Title>
        <DatePickerInput label={'Date Issued'} variant='filled' />
        <DatePickerInput label={'Date Due'} variant='filled' />
      </div>
    </Flex>
  );
};

export default FormHeader;
