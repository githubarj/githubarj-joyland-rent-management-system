import React from 'react';
import { redirect, RouteObject } from 'react-router-dom';
import AppLayout from '../layout/Index';
import Dashboard from '../views/dashboard/Index';
import Admin from '../views/admin';
import Accounting from '../views/Accounting/Index';
import Notifications from '../views/notifications/Index';
import Settings from '../views/settings/Index';
import ErrorPage from '../views/errors/Index';
import { invoiceRoutes } from '../views/Invoicing/Index';

export const routes: RouteObject[] = [
  {
    path: '/',
    element: React.createElement(AppLayout),
    children: [
      {
        index: true,
        loader: () => redirect('dashboard'),
      },
      invoiceRoutes,
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
      {
        path: 'notifications',
        element: React.createElement(Notifications),
      },
      {
        path: 'settings',
        element: React.createElement(Settings),
      },
      {
        path: '*',
        element: React.createElement(ErrorPage),
      },
    ],
  },
];
