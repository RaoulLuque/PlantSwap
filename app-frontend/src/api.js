import axios from 'axios'

// Create an axios instance with the base URL of the backend API
const api = axios.create({
    baseURL: 'http://localhost:8000',
})

export default api;
