import { Image } from '@mantine/core';
import React from 'react';
import Image404 from '../assets/cuate.png';

const Error404: React.FC = () => {
  return <Image src={Image404} fit='contain'  mah={400} />;
};

export default Error404;