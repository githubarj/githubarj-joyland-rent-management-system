import React from 'react';
import { RouteObject } from 'react-router-dom';
import Login from './Pages/Login';
import ForgotPassword from './Pages/ForgotPassword';
import AuthLayout from './Pages/AuthLayout';
import ResetPassword from './Pages/ResetPassword';
import Register from './Pages/Register';
import VerifyEmail from './Pages/VerifyEmail';

export const authRoutes: RouteObject = {
  path: '/',
  element: React.createElement(AuthLayout),
  children: [
    {
      path: 'login',
      element: React.createElement(Login),
    },
    {
      path: 'register',
      element: React.createElement(Register),
    },
    {
      path: 'verify-email/:uid/:token',
      element: React.createElement(VerifyEmail),
    },
    {
      path: 'forgot-password',
      element: React.createElement(ForgotPassword),
    },
    {
      path: 'reset-password',
      element: React.createElement(ResetPassword),
    },
  ],
};
