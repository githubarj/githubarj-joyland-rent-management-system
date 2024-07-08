import { useCallback } from 'react';
import { useNavigate } from 'react-router-dom';

interface NavigateOptions {
  to: string;
  replace?: boolean;
}

const useCustomNavigation = () => {
  const navigate = useNavigate();

  const goTo = useCallback(
    (options: NavigateOptions) => {
      const { to, replace = false } = options;
      navigate(to, { replace });
    },
    [navigate]
  );

  const goBack = useCallback(() => {
    navigate(-1);
  }, [navigate]);

  const replaceCurrent = useCallback(
    (to: string) => {
      navigate(to, { replace: true });
    },
    [navigate]
  );

  return {
    goTo,
    goBack,
    replaceCurrent,
  };
};

export default useCustomNavigation;
