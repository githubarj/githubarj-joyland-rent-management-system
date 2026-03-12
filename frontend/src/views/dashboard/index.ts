import React from 'react';
import { redirect, RouteObject } from 'react-router-dom';
import Dashboard from './Index';

export const dashboardRoutes: RouteObject = {
  path: 'Dashboard',
  children: [
    {
      index: true,
      loader: () => redirect('dashboard'),
    },
    {
      path: 'invoice-list',
      element: React.createElement(Dashboard),
    },
  ],
};
