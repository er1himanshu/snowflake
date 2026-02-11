/**
 * Main Application Logic
 * Handles initialization and tab navigation
 */

class SnowflakeApp {
    constructor() {
        this.currentTab = 'simulate';
        this.initialize();
    }

    initialize() {
        console.log('🚀 Initializing Snowflake AI Policy Impact Simulator...');
        
        // Setup tab navigation
        this.setupTabNavigation();
        
        // Check API health
        this.checkAPIHealth();
        
        // Load initial data
        this.loadInitialData();
        
        console.log('✅ Application initialized');
    }

    /**
     * Setup tab navigation
     */
    setupTabNavigation() {
        const tabButtons = document.querySelectorAll('.tab-button');
        const tabContents = document.querySelectorAll('.tab-content');

        tabButtons.forEach(button => {
            button.addEventListener('click', () => {
                const tabName = button.getAttribute('data-tab');
                
                // Remove active class from all
                tabButtons.forEach(btn => btn.classList.remove('active'));
                tabContents.forEach(content => content.classList.remove('active'));
                
                // Add active class to current
                button.classList.add('active');
                const tabContent = document.getElementById(`${tabName}-tab`);
                if (tabContent) {
                    tabContent.classList.add('active');
                }
                
                this.currentTab = tabName;
            });
        });
    }

    /**
     * Check API health
     */
    async checkAPIHealth() {
        try {
            const health = await apiClient.healthCheck();
            console.log('✅ API Health:', health);
            
            if (health.status !== 'healthy') {
                this.showNotification('Warning: API may not be fully operational', 'warning');
            }
        } catch (error) {
            console.error('❌ API Health Check Failed:', error);
            this.showNotification('Warning: Cannot connect to backend API', 'error');
        }
    }

    /**
     * Load initial data
     */
    async loadInitialData() {
        try {
            // Load economic indicators (optional, for display)
            const indicators = await apiClient.getEconomicIndicators();
            console.log('📊 Latest Economic Indicators:', indicators);
        } catch (error) {
            console.error('Error loading initial data:', error);
        }
    }

    /**
     * Show notification to user
     */
    showNotification(message, type = 'info') {
        // Simple console notification for now
        // Could be enhanced with a toast notification system
        const emoji = type === 'error' ? '❌' : type === 'warning' ? '⚠️' : 'ℹ️';
        console.log(`${emoji} ${message}`);
        
        // Optionally show alert for errors
        if (type === 'error') {
            // Only show alert for critical errors, not connection issues
            if (!message.includes('Cannot connect')) {
                alert(message);
            }
        }
    }

    /**
     * Format number with commas
     */
    static formatNumber(num, decimals = 2) {
        return num.toFixed(decimals).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    }

    /**
     * Format percentage
     */
    static formatPercentage(num, decimals = 1) {
        return `${num.toFixed(decimals)}%`;
    }

    /**
     * Get risk emoji based on level
     */
    static getRiskEmoji(level) {
        const levelLower = level.toLowerCase();
        switch (levelLower) {
            case 'low': return '✅';
            case 'moderate': return '⚠️';
            case 'high': return '🔴';
            case 'critical': return '🚨';
            default: return '❓';
        }
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.snowflakeApp = new SnowflakeApp();
});

// Add global error handler
window.addEventListener('error', (event) => {
    console.error('Global error:', event.error);
});

// Add unhandled promise rejection handler
window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason);
});
