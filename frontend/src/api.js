import axios from 'axios';

export const baseURL = "http://127.0.0.1:8000";

export const api = axios.create({
  baseURL: baseURL,
});

export default api;