import { ReactNode } from 'react';
import { IconType } from 'react-icons/lib';
import {
  MdOutlineAccountBalanceWallet,
  MdOutlineAdminPanelSettings,
  MdOutlineNotificationsNone,
  MdOutlineSpaceDashboard,
} from 'react-icons/md';
import { FcBusinessman, FcCalendar, FcMoneyTransfer } from 'react-icons/fc';
import { RiListSettingsLine } from 'react-icons/ri';
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
    icon: MdOutlineSpaceDashboard,
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
    label: 'Billing',
    icon: FcMoneyTransfer,
    to: 'billing',
    children: [
      {
        label: 'Water Bills',
        to: 'billing/water-bills',
      },
      {
        label: 'Monthly rent',
        to: 'billing/monthly-rent',
      },
      {
        label: 'Repairs',
        to: 'billing/repairs',
      },
      {
        label: 'Expenses',
        to: 'billing/expenses',
      },
      {
        label: 'Cancelled Bills',
        to: 'billing/cancelled-bills',
      },
    ],
  },
  {
    label: 'Accounting',
    icon: MdOutlineAccountBalanceWallet,
    to: 'accounting',
    children: [
      {
        label: 'Invoices',
        to: 'accounting/invoices',
      },
      {
        label: 'Receipts',
        to: 'accounting/receipts',
      },
      {
        label: 'Cancelled Payments',
        to: 'accounting/cancelled-payments',
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
    icon: MdOutlineAdminPanelSettings,
    to: 'admin',
  },
  {
    label: 'Settings',
    icon: RiListSettingsLine,
    to: 'settings',
  },
];

export { links };
