import { ReactNode } from 'react';
import { IconType } from 'react-icons/lib';
import { MdOutlineNotificationsNone } from 'react-icons/md';
import {
  FcAnswers,
  FcBarChart,
  FcBusinessman,
  FcCalendar,
  FcDataProtection,
  FcMoneyTransfer,
  FcSalesPerformance,
  FcServices,
} from 'react-icons/fc';
export interface navLinksProps {
  label: ReactNode;
  description?: ReactNode;
  rightSection?: ReactNode;
  leftSection?: ReactNode;
  children?: navLinksProps[];
  onChange?: (opened: boolean) => void;
  defaultOpened?: boolean;
  opened?: boolean;
  icon?: IconType;
  to: string;
}

const links: navLinksProps[] = [
  {
    label: 'Dashboard',
    icon: FcBarChart,
    to: 'dashboard',
  },
  {
    label: 'Notifications',
    icon: MdOutlineNotificationsNone,
    to: 'notifications',
  },
  {
    label: 'Users',
    to: 'users',
    icon: FcBusinessman,
    children: [
      {
        label: 'User Register',
        to: 'user-register',
      },
    ],
  },
  {
    label: 'Invoicing',
    icon: FcMoneyTransfer,
    to: 'invoicing',
    children: [
      {
        label: 'View invoices',
        to: 'invoicing/invoice-list',
      },
      {
        label: 'Create Invoice',
        to: 'invoicing/invoice-page',
      },
      {
        label: 'Repairs',
        to: 'invoicing/repairs',
      },
      {
        label: 'Expenses',
        to: 'invoicing/expenses',
      },
      {
        label: 'Cancelled Invoices',
        to: 'invoicing/cancelled-invoices',
      },
    ],
  },
  {
    label: 'Accounting',
    icon: FcSalesPerformance,
    to: 'accounting',
    children: [
      {
        label: 'Payments',
        to: 'accounting/payment-history',
      },
      {
        label: 'Record Payment',
        to: 'accounting/record-payment',
      },
      {
        label: 'Transaction Records',
        to: 'accounting/transaction-records',
      },
      {
        label: 'Cancelled Payments',
        to: 'accounting/cancelled-payments',
      },
    ],
  },
  {
    label: 'Reports',
    to: 'reports',
    icon: FcAnswers,
    children: [
      {
        label: 'Invoice Summary',
        to: 'reports/invoice-summary',
      },
      {
        label: 'Outstanding Payments',
        to: 'reports/oustanding-payments',
      },
      {
        label: 'Revenue Reports',
        to: 'reports/revenue-reports',
      },
    ],
  },
  {
    label: 'Calender',
    icon: FcCalendar,
    to: 'calendar',
  },

  {
    label: 'Admin',
    icon: FcDataProtection,
    to: 'admin',
  },
  {
    label: 'Settings',
    icon: FcServices,
    to: 'settings',
  },
];

export { links };
