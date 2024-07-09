import React, { useEffect, useState } from 'react';
import {
  Button,
  Flex,
  Grid,
  Input,
  MultiSelect,
  Paper,
  Table,
  TableData,
} from '@mantine/core';
import { InvoiceService } from '../../../services/_invoice.service';

const InvoiceTable: React.FC = () => {
  const [dataSource, setDataSource] = useState<{
    keys: string[];
    values: any[][];
  }>({
    keys: [], // Initial empty array
    values: [],
  });

  useEffect(() => {
    fetchInvoices();
  }, []);

  const fetchInvoices = () => {
    InvoiceService.getInvoices()
      .then((res) => processData(res.data))
      .then((data) => setDataSource(data))
      .catch((err) => console.log(err));
  };

  interface MyObject {
    [key: string]: any;
  }

  function processData(data: MyObject[]): { keys: string[]; values: any[][] } {
    if (data.length === 0) {
      return { keys: [], values: [] };
    }

    const keys = Object.keys(data[0]);
    const values = data.map((obj) => keys.map((key) => obj[key]));

    return { keys, values };
  }

  const tableData: TableData = {
    caption: 'Some elements from periodic table',
    head: dataSource.keys,
    body: dataSource.values,
  };

  return (
    <Paper shadow='0 4px 8px rgba(0, 0, 0, 0.1)' radius={5}>
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
      <Table
        data={tableData}
        highlightOnHover
        styles={{
          thead: { backgroundColor: '#f4f5fa' },
        }}
      />
    </Paper>
  );
};

export default InvoiceTable;
