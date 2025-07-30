import { LoaderFunction, redirect } from "react-router-dom";
import { isAuthenticated } from "./auth";

export const requireAuth: LoaderFunction = () => {
    if (!isAuthenticated()) {
        return redirect('/login');
    }
    return null;
}