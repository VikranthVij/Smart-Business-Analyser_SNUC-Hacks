const API_BASE_URL = "http://localhost:8000"; // Your FastAPI URL

export const fetchTrends = async (keywords: string[]) => {
  try {
    const response = await fetch(`${API_BASE_URL}/trends`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ keywords }),
    });
    if (!response.ok) throw new Error("Failed to fetch trends");
    return await response.json();
  } catch (error) {
    console.error("Error fetching trends:", error);
    return { trends: [] };
  }
};