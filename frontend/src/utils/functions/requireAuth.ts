import { redirect } from "react-router-dom";


export async function requireAuth () {
    const token = localStorage.getItem('access_token');
    if (!token) {
        return redirect('/login')
    }

    return null
}