import { redirect, RouteObject } from 'react-router-dom';
import TenantRegister from './Components/TenantRegister';
import React from 'react';

export const tentantRoutes: RouteObject = {
  path: 'tenants',
  children: [
    {
      index: true,
      loader: () => redirect('tenants-register'),
    },
    {
      path: 'tenants-register',
      element: React.createElement(TenantRegister),
    },
  ],
};
