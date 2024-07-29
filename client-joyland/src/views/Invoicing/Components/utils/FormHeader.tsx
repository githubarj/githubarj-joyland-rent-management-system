import { Flex, Image, Text, Title } from '@mantine/core';
import React from 'react';
import freelance from '../../../../../public/assets/freeLance.png';
import { DatePickerInput } from '@mantine/dates';

const FormHeader: React.FC = () => {
  return (
    <Flex className='justify-between'>
      <div className='flex flex-col gap-2'>
        <div className='flex gap-2'>
          <Image src={freelance} fit='contain' h={'xl'} />
          <Title order={2}>Joyland</Title>
        </div>
        <div className='flex flex-col'>
          <Text>Kasarani, Nairobi</Text>
          <Text>Paybill : 55543</Text>
          <Text>Account Number: #house-number</Text>
        </div>
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
