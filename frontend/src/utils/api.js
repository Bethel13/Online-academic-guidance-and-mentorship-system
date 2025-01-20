// frontend/src/utils/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5000'
});

export const testConnection = async () => {
  try {
    const response = await api.get('/');
    console.log('Backend Connection:', response.data);
    return response.data;
  } catch (error) {
    console.error('Connection Error:', error);
    throw error;
  }
};

export const testRegistration = async (userData) => {
  try {
    const response = await api.post('/register', userData);
    console.log('Registration Response:', response.data);
    return response.data;
  } catch (error) {
    console.error('Registration Error:', error);
    throw error;
  }
};

export const testLogin = async (credentials) => {
  try {
    const response = await api.post('/login', credentials);
    console.log('Login Response:', response.data);
    return response.data;
  } catch (error) {
    console.error('Login Error:', error);
    throw error;
  }
};