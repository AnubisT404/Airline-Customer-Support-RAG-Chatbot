import axios from 'axios';

// const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://backend:8000';

// export const sendMessage = async (query: string) => {
//     try {
//         const response = await axios.post(`${API_URL}/query`, { query });
//         return response.data.message;
//     } catch (error) {
//         console.error('Error communicating with backend:', error);
//         throw error;
//     }
// };

// Create an axios instance with the base URL of your backend
const api = axios.create({
    baseURL: 'http://localhost:8000', // Make sure this URL is correct
});

// Function to send user messages to the backend and receive responses
export const sendMessage = async (message: string) => {
    try {
        console.log("Sending message to backend...", message);  // Debug message
        const response = await api.post('/query', { query: message });
        
        if (response.data.message) {
            console.log("Response from backend:", response.data.message);  // Log the response
            return response.data.message;
        } else {
            console.error("Unexpected response format from backend:", response.data);
            throw new Error("Invalid response format from backend.");
        }
    } catch (error) {
        console.error('Error communicating with backend:', error);
        throw new Error("Failed to communicate with the backend.");
    }

    // try {
    //     console.log("Sending message:", message);
    //     const response = await api.post('/query', { query: message });
    //     return response.data.message;
    // } catch (error) {
    //     console.error('Error communicating with backend:', error);
    //     return "Error communicating with the backend.";
    // }
};
