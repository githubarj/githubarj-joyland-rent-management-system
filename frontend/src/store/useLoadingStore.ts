import { create } from 'zustand';

interface LoadingState {
  loading: Record<string, boolean>;
  setLoading: (key: string, value: boolean) => void;
}

export const useLoadingStore = create<LoadingState>((set) => ({
  loading: { user: true },
  setLoading: (key, value) =>
    set((state) => ({
      loading: { ...state.loading, [key]: value },
    })),
}));
