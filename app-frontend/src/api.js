import axios from 'axios'

// Create an axios instance with the base URL of the backend API
const api = axios.create({
    baseURL: process.env.REACT_APP_BACKEND_URL,
})

export default api;
