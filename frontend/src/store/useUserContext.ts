import { create } from 'zustand';

interface User {
  id: number;
  email: string;
  full_name: string;
  roles: string;
  date_joined: string;
  is_active: boolean;
}

interface UserStore {
    user: User | null;
    setUser: (user: User) => void;
    clearUser: () => void;
}


export const useUserStore = create<UserStore>((set) => ({
  user: null,
  setUser: (user) => set({ user }),
  clearUser: () => set({ user: null }),
}));