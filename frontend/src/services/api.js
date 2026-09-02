import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export const getDashboardStats = async () => {
    const response = await axios.get(`${API_URL}/dashboard/stats`);
    return response.data;
};

export const getCandidates = async () => {
    const response = await axios.get(`${API_URL}/candidates`);
    return response.data;
};

export const getCandidate = async (id) => {
    const response = await axios.get(`${API_URL}/candidates/${id}`);
    return response.data;
};

export const getTimeline = async (id) => {
    const response = await axios.get(`${API_URL}/candidates/${id}/timeline`);
    return response.data;
};

export const sendOutreach = async (id) => {
    const response = await axios.post(`${API_URL}/candidates/${id}/outreach`);
    return response.data;
};

export const simulateReply = async (id, message) => {
    const response = await axios.post(`${API_URL}/candidates/${id}/reply`, { message });
    return response.data;
};

export const scheduleInterview = async (id) => {
    const response = await axios.post(`${API_URL}/candidates/${id}/schedule`);
    return response.data;
};
