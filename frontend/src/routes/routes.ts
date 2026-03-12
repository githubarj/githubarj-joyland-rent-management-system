import React from 'react';
import { RouteObject } from 'react-router-dom';
import AppLayout from '../layout/Index';
import ErrorPage from '../views/errors/Index';
import { invoiceRoutes } from '../views/Invoicing/Index';
import { authRoutes } from '../views/auth';
import { dashboardRoutes } from '../views/dashboard';
import { requireAuth } from '../utils/functions/requireAuth';
import { tenantRoutes } from '../views/tenants';

export const routes: RouteObject[] = [
  {
    path: '/',
    loader: requireAuth,
    element: React.createElement(AppLayout),
    children: [
      dashboardRoutes,
      invoiceRoutes,
      tenantRoutes,
      {
        path: '*',
        element: React.createElement(ErrorPage),
      },
    ],
  },
  authRoutes,
];
