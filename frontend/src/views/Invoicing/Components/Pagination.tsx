import { Button, Center, Flex, Menu, Text } from '@mantine/core';
import React, { useState } from 'react';
import { IoMdArrowDropdown } from 'react-icons/io';
import { MdArrowBackIosNew, MdArrowForwardIos } from 'react-icons/md';

const CustomPagination: React.FC = () => {
  const [elements, setElements] = useState(10);
  const [pageNumber, setPageNumber] = useState(1);

  return (
    <Flex
      justify={'flex-end'}
      gap={'lg'}
      align={'center'}
      w={'100%'}
      px={15}
      pb={10}
    >
      <Center inline>
        Rows per page:{' '}
        <Menu shadow='md' width={200}>
          <Menu.Target>
            <Button c={'gray'} variant='transparent' size='xs' p={5}>
              <Text>{elements}</Text> <IoMdArrowDropdown />
            </Button>
          </Menu.Target>

          <Menu.Dropdown w={100}>
            <Menu.Item onClick={() => setElements(15)}>15</Menu.Item>
            <Menu.Item onClick={() => setElements(20)}>20</Menu.Item>
            <Menu.Item onClick={() => setElements(25)}>25</Menu.Item>
          </Menu.Dropdown>
        </Menu>
      </Center>
      <Text>1 - 5 of 13</Text>
      <Flex align={'center'} gap={'xs'}>
        <MdArrowBackIosNew />
        <MdArrowForwardIos />
      </Flex>
    </Flex>
  );
};

export default CustomPagination;
