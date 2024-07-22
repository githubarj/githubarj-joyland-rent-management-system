import React from 'react';
import { redirect, RouteObject } from 'react-router-dom';
import InvoiceList from './Components/InvoiceList';
import DetailsInvoice from './Components/DetailsInvoice';

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
    {
      path: 'invoice-details',
      element: React.createElement(DetailsInvoice),
    },
  ],
};
