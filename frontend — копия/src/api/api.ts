import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/';

export const fetchMessages = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}messages/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching messages:', error);
    throw error;
  }
};

export const sendMessage = async (content: string) => {
  try {
    await axios.post(`${API_BASE_URL}messages/`, { content });
  } catch (error) {
    console.error('Error sending message:', error);
    throw error;
  }
};