import axios from "axios";

const API_BASE_URL = "http://localhost:8000/api/";

export const fetchMessages = async () => {
    const response = await axios.get(`${API_BASE_URL}messages/`);
    return response.data;
};

export const sendMessage = async (content: string) => {
    await axios.post(`${API_BASE_URL}messages/`, { content });
};