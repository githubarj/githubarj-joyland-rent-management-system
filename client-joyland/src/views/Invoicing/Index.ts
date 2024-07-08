import React from 'react';
import { redirect, RouteObject } from 'react-router-dom';
import InvoiceList from './Components/InvoiceList'

export const invoiceRoutes: RouteObject = {
  path: 'Invoicing',
  children: [
    {
      index: true,
      loader: () => redirect('invoice-list'),
    },
    {
      path: 'invoice-list',
      element: React.createElement(InvoiceList),
    },
  ],
};
