import React from 'react';
import { RouteObject } from 'react-router-dom';
import AppLayout from '../layout/Index';

export const routes: RouteObject[] = [
  {
    path: '/',
    element: React.createElement(AppLayout),
    children: [],
  },
];
