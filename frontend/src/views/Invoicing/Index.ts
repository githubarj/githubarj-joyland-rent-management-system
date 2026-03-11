import React from 'react';
import { redirect, RouteObject } from 'react-router-dom';
import InvoiceList from './Components/InvoiceList';
import InvoicePage from './Components/DetailsInvoice';

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
      path: 'invoice-page',
      element: React.createElement(InvoicePage),
    },
  ],
};
