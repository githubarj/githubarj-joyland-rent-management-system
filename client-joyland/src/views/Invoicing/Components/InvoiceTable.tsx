import React from 'react';
import { Button, Flex, Grid, Input, MultiSelect, Paper, Table, TableData } from '@mantine/core';

const InvoiceTable: React.FC = () => {

  const tableHeaders = [
    'Id',
    'House Number',
    'Tenant',
    'Total',
    'Issue Date',
    'Balance',
  ];

  const tableDatas = [

  ]

  const tableData: TableData = {
    caption: 'Some elements from periodic table',
    head: ['Element position', 'Atomic mass', 'Symbol', 'Element name'],
    body: [
      [6, 12.011, 'C', 'Carbon'],
      [7, 14.007, 'N', 'Nitrogen'],
      [39, 88.906, 'Y', 'Yttrium'],
      [56, 137.33, 'Ba', 'Barium'],
      [58, 140.12, 'Ce', 'Cerium'],
    ],
  };
  return (
    <Paper>
      <Grid px={15} py={20} display={'flex'} justify='space-between'>
        <Grid.Col span={'content'}>
          <MultiSelect placeholder='Action' data={['Pending', 'paid']} />
        </Grid.Col>
        <Grid.Col span={'content'}>
          <Flex gap={'md'}>
            <Input placeholder='Search  Invoice' />
            <Button>Create invoice </Button>
          </Flex>
        </Grid.Col>
      </Grid>
      <Table data={tableData} highlightOnHover />
    </Paper>
  );
};

export default InvoiceTable;
