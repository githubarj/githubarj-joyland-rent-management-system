import React from 'react';
import { Grid, MultiSelect, Paper, Title } from '@mantine/core';
import { DateTimePicker } from '@mantine/dates';

const SearchInvoices: React.FC = () => {
  return (
    <Paper py={'lg'} px={'md'} mb={20}>
      <Title order={2} mb={10}>
        Filters
      </Title>
      <Grid>
        <Grid.Col span={6}>
          <MultiSelect placeholder='Pick value' data={['Pending', 'paid']} />
        </Grid.Col>
        <Grid.Col span={6}>
          <DateTimePicker placeholder='Pick date and time' />
        </Grid.Col>
      </Grid>
    </Paper>
  );
};

export default SearchInvoices;
