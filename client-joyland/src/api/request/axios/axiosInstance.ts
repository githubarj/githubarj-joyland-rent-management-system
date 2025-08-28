import axios from "axios";

const  baseUrl  = import.meta.env.VITE_SERVER_BASE_URL;

export const query = axios.create({
  baseURL: baseUrl,
  timeout: 10000,
});
