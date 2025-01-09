import axios from 'axios';
import { getCookie } from '../utils/cookies';

const API_URL = 'http://localhost:8080/users';
const GENERATE_URL = 'http://localhost:8080';

export const fetchProducts = async () => {
  const accessToken = getCookie('access_token');
  const idToken = getCookie('id_token');

  if (!accessToken || !idToken) {
    console.error('Access token or ID token is missing.');
    return [];
  }

  const headers = {
    Authorization: `Bearer ${accessToken}`,
    idToken: `Bearer ${idToken}`
  };

  try {
    const response = await axios.get(`${API_URL}/products`, { headers, withCredentials: true });
    return response.data;
  } catch (error) {
    console.error('Error fetching products:', error);
    return [];
  }
};

export const fetchAudiences = async () => {
  const accessToken = getCookie('access_token');
  const idToken = getCookie('id_token');

  if (!accessToken || !idToken) {
    console.error('Access token or ID token is missing.');
    return [];
  }

  const headers = {
    Authorization: `Bearer ${accessToken}`,
    idToken: `Bearer ${idToken}`
  };

  try {
    const response = await axios.get(`${API_URL}/audiences`, { headers, withCredentials: true });
    return response.data;
  } catch (error) {
    console.error('Error fetching audiences:', error);
    return [];
  }
};

export const fetchUserInfo = async () => {
    const accessToken = getCookie('access_token');
    const idToken = getCookie('id_token');
  
    if (!accessToken || !idToken) {
      console.error('Access token or ID token is missing.');
      return null;
    }
  
    const headers = {
      Authorization: `Bearer ${accessToken}`,
      idToken: `Bearer ${idToken}`
    };
  
    try {
      const response = await axios.get('http://localhost:8080/users/sub', { headers, withCredentials: true });
      return response.data;
    } catch (error) {
      console.error('Error fetching user info:', error);
      return null;
    }
  };
  
  export const fetchCompanyInfo = async () => {
    const accessToken = getCookie('access_token');
    const idToken = getCookie('id_token');
  
    if (!accessToken || !idToken) {
      console.error('Access token or ID token is missing.');
      return null;
    }
  
    const headers = {
      Authorization: `Bearer ${accessToken}`,
      idToken: `Bearer ${idToken}`
    };
  
    try {
      const response = await axios.get('http://localhost:8080/users/company', { headers, withCredentials: true });
      return response.data;
    } catch (error) {
      console.error('Error fetching company info:', error);
      return null;
    }
  };

export const generateContent = async (contentData) => {
  const accessToken = getCookie('access_token');
  const idToken = getCookie('id_token');

  if (!accessToken || !idToken) {
      console.error('Access token or ID token is missing.');
      return null;
  }

  const headers = {
      Authorization: `Bearer ${accessToken}`,
      idToken: `Bearer ${idToken}`,
      'Content-Type': 'application/json'
  };



  try {
      const response = await axios.post(`${GENERATE_URL}/contents/disperse`, contentData, { headers, withCredentials: true });
      return response.data;
  } catch (error) {
      console.error('Error generating content:', error);
      return null;
  }
};