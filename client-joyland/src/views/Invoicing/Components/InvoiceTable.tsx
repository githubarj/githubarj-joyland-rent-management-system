import React, { ReactNode, useEffect, useState } from 'react';
import dayjs from 'dayjs';
import advancedFormat from 'dayjs/plugin/advancedFormat';
import {
  Badge,
  Button,
  Flex,
  getOptionsLockup,
  Grid,
  Input,
  MultiSelect,
  Paper,
  Table,
  TableData,
  Text,
  Tooltip,
  UnstyledButton,
} from '@mantine/core';
import { InvoiceService } from '../../../services/_invoice.service';
import { invoices } from '../../../helpers/dataShapes';
import invoicingStyles from '../invoicingStyles.module.scss';
import CustomPagination from './Pagination';
import {
  MdDeleteOutline,
  MdOutlineModeEdit,
  MdOutlineRemoveRedEye,
} from 'react-icons/md';
import useCustomNavigation from '../../../hooks/useCustomNavigation';

const InvoiceTable: React.FC = () => {
  const [dataSource, setDataSource] = useState<ReactNode[][]>([]);
  const { goTo } = useCustomNavigation();

  useEffect(() => {
    fetchInvoices();
  }, []);

  const fetchInvoices = () => {
    InvoiceService.getInvoices()
      .then((res) => tableBody(res.data))
      .then((data) => setDataSource(data))
      .catch((err) => console.log(err));
  };

  const tableHeaders: string[] = [
    '#',
    'HOUSE NUMBER',
    'TENANT',
    'TOTAL',
    'ISSUE DATE',
    'BALANCE',
    'TYPE',
    'ACTION',
  ];

  dayjs.extend(advancedFormat);
  const tableBody = (items: invoices[]): ReactNode[][] => {
    return items.map((item) => [
      <Text c={'blue'}>{item.id}</Text>,
      <Text> {item.houseNumber} </Text>,
      <Text> {item.tenant} </Text>,
      <Text> {item.total} Ksh </Text>,
      <Text> {dayjs(item.issueDate).format('Do MMMM YYYY')} </Text>,
      <div>
        {item.balance <= 0 ? (
          <Badge color='green' variant='light'>
            Paid
          </Badge>
        ) : (
          `${parseFloat(item.balance.toFixed(2))} Ksh`
        )}
      </div>,
      <Text>{item.type} </Text>,
      <Flex gap={'xs'} align={'center'}>
        <Tooltip label={'view'}>
          <UnstyledButton onClick={() => goTo({ to: '/invoicing/invoice-details' })}>
            <MdOutlineRemoveRedEye color='green' />
          </UnstyledButton>
        </Tooltip>
        <Tooltip label={'edit'}>
          <UnstyledButton>
            <MdOutlineModeEdit color='blue' />
          </UnstyledButton>
        </Tooltip>
        <Tooltip label={'delete'}>
          <UnstyledButton>
            <MdDeleteOutline color='red' />
          </UnstyledButton>
        </Tooltip>
      </Flex>,
    ]);
  };

  const tableData: TableData = {
    head: tableHeaders,
    body: dataSource,
  };

  return (
    <Paper shadow='xs' radius={5} mb={20} >
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
      <Table.ScrollContainer minWidth={500}>
        <Table
          stickyHeader
          data={tableData}
          highlightOnHover
          striped={'even'}
          classNames={{
            thead: invoicingStyles.headers,
          }}
        />
      </Table.ScrollContainer>
      <CustomPagination />
    </Paper>
  );
};

export default InvoiceTable;
