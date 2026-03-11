import { Avatar, Indicator, Menu, Text } from '@mantine/core';
import {
  IconArrowsLeftRight,
  IconMessageCircle,
  IconPhoto,
  IconSearch,
  IconSettings,
} from '@tabler/icons-react';
import React from 'react';
import { MdLogout } from 'react-icons/md';
import { logout } from '../../../api/services/_auth.service';
import { showNotification } from '@mantine/notifications';
import { useUserStore } from '../../../store/useUserContext';
import useCustomNavigation from '../../../hooks/useCustomNavigation';

const UserMenu: React.FC = () => {
  const user = useUserStore((state) => state.user);
  const clearUser = useUserStore((state) => state.clearUser);

  const { goTo } = useCustomNavigation();

  const handleLogout = async () => {
    const refreshToken = localStorage.getItem('refresh_token') || undefined;
    await logout({ refresh: refreshToken });

    showNotification({
      title: 'Logout Successful',
      message: 'You have logged out successfully',
    });
    clearUser();
    goTo({ to: '/login' });
  };

  return (
    <Indicator offset={6} color="green" position="bottom-end" size={12} withBorder>
      <Menu trigger="hover" openDelay={100} closeDelay={400}>
        <Menu.Target>
          <Avatar style={{ cursor: 'pointer' }} color="cyan" radius="xl">
            RG
          </Avatar>
        </Menu.Target>
        <Menu.Dropdown>
          <Menu.Label>{user ? `Hello ${user.full_name}` : 'Hello'}</Menu.Label>
          <Menu.Item leftSection={<IconSettings size={14} />}>Settings</Menu.Item>
          <Menu.Item leftSection={<IconMessageCircle size={14} />}>Messages</Menu.Item>
          <Menu.Item leftSection={<IconPhoto size={14} />}>Gallery</Menu.Item>
          <Menu.Item
            leftSection={<IconSearch size={14} />}
            rightSection={
              <Text size="xs" c="dimmed">
                ⌘K
              </Text>
            }
          >
            Search
          </Menu.Item>

          <Menu.Divider />

          <Menu.Label>Danger zone</Menu.Label>
          <Menu.Item leftSection={<IconArrowsLeftRight size={14} />}>
            Transfer my data
          </Menu.Item>
          <Menu.Item
            onClick={handleLogout}
            color="red"
            leftSection={<MdLogout size={14} />}
          >
            Logout
          </Menu.Item>
        </Menu.Dropdown>
      </Menu>
    </Indicator>
  );
};

export default UserMenu;
