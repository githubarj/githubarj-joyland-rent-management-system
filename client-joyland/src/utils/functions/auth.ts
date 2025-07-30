export const isAuthenticated = (): boolean => {
    const token: string | null = localStorage.getItem('token');
    return !!token;
}

/**
 * Calculate password strength as a percentage.
 * @param password - The password string to evaluate.
 * @returns A number between 0 and 100 representing strength.
 */


export const getPasswordStrength = (password: string): number => {
  let multiplier = password.length > 7 ? 0 : 1;
  if (/[A-Z]/.test(password)) multiplier += 1;
  if (/[0-9]/.test(password)) multiplier += 1;
  if (/[!@#$%^&*]/.test(password)) multiplier += 1;
  if (password.length >= 8) multiplier += 1;

  return (multiplier / 4) * 100;
};

/**
 * Returns a color string based on password strength.
 * @param strength - Password strength as a number between 0 and 100.
 * @returns A string representing a color.
 */


export const passwordStrengthColor = (strength: number): string => {
  if (strength === 100) return 'teal';
  if (strength >= 50) return 'yellow';
  return 'red';
};