
import React from 'react';
import { RouteObject } from 'react-router-dom';
import Login from './Components/Login';
import ForgotPassword from './Components/ForgotPassword';
import AuthLayout from './Components/AuthLayout';
import ResetPassword from './Components/ResetPassword';

export const authRoutes: RouteObject = {
  path: '/',
  element: React.createElement(AuthLayout),
  children: [
    {
      path: 'login',
      element: React.createElement(Login),
    },
    {
      path: 'forgot-password',
      element: React.createElement(ForgotPassword),
    },
    {
      path: 'reset-password',
      element: React.createElement(ResetPassword)
    }
  ]
}
