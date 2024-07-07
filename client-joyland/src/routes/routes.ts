import React from 'react';
import { redirect, RouteObject } from 'react-router-dom';
import AppLayout from '../layout/Index';
import Dashboard from '../views/dashboard/Index';
import Admin from '../views/admin';
import Accounting from '../views/Accounting/Index';

export const routes: RouteObject[] = [
  {
    path: '/',
    element: React.createElement(AppLayout),
    children: [
      {
        index: true,
        loader: () => redirect('dashboard'),
      },
      {
        path: 'dashboard',
        element: React.createElement(Dashboard),
      },
      {
        path: 'admin',
        element: React.createElement(Admin),
      },
      {
        path: 'accounts',
        element: React.createElement(Accounting),
      },
    ],
  },
];
