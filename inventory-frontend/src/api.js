// TODO: Replace with your actual Render URL
export const API_URL = "https://inventory-backend-api-fbt4.onrender.com";

export const apiCall = async (endpoint, method = "GET", body = null) => {
    const options = {
        method,
        headers: { "Content-Type": "application/json" },
    };
    if (body) options.body = JSON.stringify(body);

    const response = await fetch(`${API_URL}${endpoint}`, options);

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "An error occurred");
    }

    if (response.status === 204) return null; // Handle DELETE requests
    return response.json();
};