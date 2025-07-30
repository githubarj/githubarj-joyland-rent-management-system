export const isAuthenticated = (): boolean => {
    const token: string | null = localStorage.getItem('token');
    return !!token;
}