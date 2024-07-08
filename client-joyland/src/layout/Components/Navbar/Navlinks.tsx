import { AppShell, NavLink, ScrollArea } from '@mantine/core';
import React, { ReactNode } from 'react';
import { links, navLinksProps } from '../../../helpers/navigation';
import { IconType } from 'react-icons/lib';
import { NavLink as RouterLink } from 'react-router-dom';

const Navlinks: React.FC = () => {
  const navIcon = (icon: IconType): ReactNode => {
    return React.createElement(icon);
  };

  const renderNavLink = (item: navLinksProps) => (
    <NavLink
      component={RouterLink}
      to={item.to}
      label={item.label}
      description={item.description}
      rightSection={item.rightSection}
      leftSection={item.icon && navIcon(item.icon)}
    >
      {item.children?.map((child) => renderNavLink(child))}
    </NavLink>
  );

  return (
    <AppShell.Section component={ScrollArea} type='hover' >
      {links.map(renderNavLink)}
    </AppShell.Section>
  );
};

export default Navlinks;
