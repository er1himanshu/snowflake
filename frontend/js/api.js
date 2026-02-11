/**
 * API Client for Snowflake Policy Impact Simulator
 * Handles all communication with the backend API
 */

const API_BASE_URL = window.location.origin + '/api';

class APIClient {
    /**
     * Make a GET request
     */
    async get(endpoint) {
        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('API GET error:', error);
            throw error;
        }
    }

    /**
     * Make a POST request
     */
    async post(endpoint, data) {
        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('API POST error:', error);
            throw error;
        }
    }

    /**
     * Simulate a policy
     */
    async simulatePolicy(policyData) {
        return await this.post('/simulate', policyData);
    }

    /**
     * Compare multiple scenarios
     */
    async compareScenarios(scenarios) {
        return await this.post('/compare', { scenarios });
    }

    /**
     * Get list of available sectors
     */
    async getSectors() {
        return await this.get('/sectors');
    }

    /**
     * Get policy types
     */
    async getPolicyTypes() {
        return await this.get('/policy-types');
    }

    /**
     * Get simulation history
     */
    async getHistory(limit = 10) {
        return await this.get(`/history?limit=${limit}`);
    }

    /**
     * Get current economic indicators
     */
    async getEconomicIndicators() {
        return await this.get('/economic-indicators');
    }

    /**
     * Check API health
     */
    async healthCheck() {
        return await this.get('/health');
    }
}

// Create singleton instance
const apiClient = new APIClient();
