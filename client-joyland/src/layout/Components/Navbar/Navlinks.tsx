import { NavLink, ScrollArea } from '@mantine/core';
import React, { ReactNode } from 'react';
import { links, navLinksProps } from '../../../helpers/navigation';
import { IconType } from 'react-icons/lib';

const Navlinks: React.FC = () => {
  const navIcon = (icon: IconType): ReactNode => {
    return React.createElement(icon);
  };

  const renderNavLink = (item: navLinksProps) => (
    <NavLink
      label={item.label}
      description={item.description}
      rightSection={item.rightSection}
      leftSection={item.icon && navIcon(item.icon)}
      // onClick={item.onClick}
    >
      {item.children?.map((child, index) => renderNavLink(child))}
    </NavLink>
  );

  return <ScrollArea>{links.map(renderNavLink)}</ScrollArea>;
};

export default Navlinks;
