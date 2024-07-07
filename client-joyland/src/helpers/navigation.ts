import { ReactNode } from 'react';
import { IconType } from 'react-icons/lib';
import { MdOutlineSpaceDashboard } from 'react-icons/md';

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
}

const links: navLinksProps[] = [
  {
    label: 'Dashboard',
    icon: MdOutlineSpaceDashboard,
  },
  {
    label: 'Notifications',
  },
  {
    label: 'Billing',
    children: [
      {
        label: 'Water Bills',
      },
      {
        label: 'Monthly rent',
      },
      {
        label: 'Repairs',
      },
      {
        label: 'Expenses',
      },
      {
        label: 'Cancelled Bills',
      },
    ],
  },
  {
    label: 'Accounting',
    children: [
      {
        label: 'Invoices',
      },
      {
        label: 'Receipts',
      },
      {
        label: 'Cancelled Payments',
      },
    ],
  },
  {
    label: 'Admin',
  },
  {
    label: 'Settings',
  },
];

export { links };
