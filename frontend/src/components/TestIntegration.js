// frontend/src/components/TestIntegration.js
import React from 'react';
import { testConnection, testRegistration, testLogin } from '../utils/api';

const TestIntegration = () => {
  const handleTestConnection = async () => {
    try {
      await testConnection();
    } catch (error) {
      console.error('Test failed:', error);
    }
  };

  const handleTestRegistration = async () => {
    const testUser = {
      username: 'testuser',
      email: 'test@example.com',
      password: 'password123',
      role: 'Student'
    };
    try {
      await testRegistration(testUser);
    } catch (error) {
      console.error('Registration test failed:', error);
    }
  };

  const handleTestLogin = async () => {
    const credentials = {
      email: 'test@example.com',
      password: 'password123'
    };
    try {
      await testLogin(credentials);
    } catch (error) {
      console.error('Login test failed:', error);
    }
  };

  return (
    <div>
      <h2>Integration Tests</h2>
      <button onClick={handleTestConnection}>Test Backend Connection</button>
      <button onClick={handleTestRegistration}>Test Registration</button>
      <button onClick={handleTestLogin}>Test Login</button>
    </div>
  );
};

export default TestIntegration;