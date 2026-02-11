/**
 * Chart.js Fallback Implementation
 * Provides basic chart rendering using Canvas API when Chart.js CDN is unavailable
 */

// Constants for styling
const CHART_COLORS = {
    TEXT_PRIMARY: '#2c3e50',
    TEXT_SECONDARY: '#5a6c7d',
    GRID_COLOR: '#e8ecf1'
};

const CHART_CONFIG = {
    MAX_LABEL_LENGTH_BAR: 8,
    MAX_LABEL_LENGTH_LEGEND: 12
};

class Chart {
    constructor(ctx, config) {
        // Accept either a canvas element or element ID
        if (typeof ctx === 'string') {
            this.canvas = document.getElementById(ctx);
        } else {
            this.canvas = ctx;
        }
        
        if (this.canvas && this.canvas.getContext) {
            this.context = this.canvas.getContext('2d');
        }
        
        this.config = config;
        this.type = config.type;
        this.data = config.data;
        this.options = config.options || {};
        
        if (this.canvas && this.context) {
            this.render();
        }
    }
    
    render() {
        const canvas = this.canvas;
        const ctx = this.context;
        
        // Set canvas size
        const rect = canvas.getBoundingClientRect();
        canvas.width = rect.width * window.devicePixelRatio;
        canvas.height = rect.height * window.devicePixelRatio;
        ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
        
        const width = rect.width;
        const height = rect.height;
        
        // Clear canvas
        ctx.clearRect(0, 0, width, height);
        
        // Render based on chart type
        switch (this.type) {
            case 'doughnut':
            case 'pie':
                this.renderPieChart(ctx, width, height);
                break;
            case 'bar':
                this.renderBarChart(ctx, width, height);
                break;
            default:
                this.renderPlaceholder(ctx, width, height);
        }
    }
    
    renderPieChart(ctx, width, height) {
        const data = this.data.datasets[0].data;
        const labels = this.data.labels;
        const colors = this.data.datasets[0].backgroundColor;
        
        const centerX = width / 2;
        const centerY = height / 2;
        const radius = Math.min(width, height) / 3;
        const innerRadius = this.type === 'doughnut' ? radius * 0.6 : 0;
        
        let total = data.reduce((sum, val) => sum + val, 0);
        let currentAngle = -Math.PI / 2;
        
        // Draw slices
        data.forEach((value, index) => {
            const sliceAngle = (value / total) * 2 * Math.PI;
            
            ctx.beginPath();
            ctx.arc(centerX, centerY, radius, currentAngle, currentAngle + sliceAngle);
            if (innerRadius > 0) {
                ctx.arc(centerX, centerY, innerRadius, currentAngle + sliceAngle, currentAngle, true);
            } else {
                ctx.lineTo(centerX, centerY);
            }
            ctx.closePath();
            
            ctx.fillStyle = Array.isArray(colors) ? colors[index] : colors;
            ctx.fill();
            
            currentAngle += sliceAngle;
        });
        
        // Draw center value for doughnut
        if (this.type === 'doughnut') {
            ctx.fillStyle = CHART_COLORS.TEXT_PRIMARY;
            ctx.font = 'bold 24px Inter, sans-serif';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            const displayValue = data[0].toFixed(1);
            ctx.fillText(displayValue, centerX, centerY);
        }
        
        // Draw legend
        if (this.options.plugins && this.options.plugins.legend && this.options.plugins.legend.position === 'bottom') {
            this.drawLegend(ctx, labels, colors, width, height);
        }
    }
    
    renderBarChart(ctx, width, height) {
        const data = this.data.datasets[0].data;
        const labels = this.data.labels;
        const colors = this.data.datasets[0].backgroundColor;
        
        const padding = 40;
        const chartHeight = height - padding * 2;
        const chartWidth = width - padding * 2;
        const barWidth = chartWidth / labels.length * 0.7;
        const barSpacing = chartWidth / labels.length;
        
        // Find min and max
        let min = Math.min(...data, 0);
        let max = Math.max(...data, 0);
        const range = max - min;
        
        // Draw axes
        ctx.strokeStyle = '#e8ecf1';
        ctx.lineWidth = 1;
        
        // Y-axis
        ctx.beginPath();
        ctx.moveTo(padding, padding);
        ctx.lineTo(padding, height - padding);
        ctx.stroke();
        
        // X-axis
        ctx.beginPath();
        ctx.moveTo(padding, height - padding);
        ctx.lineTo(width - padding, height - padding);
        ctx.stroke();
        
        // Zero line if data crosses zero
        if (min < 0 && max > 0) {
            const zeroY = height - padding - ((0 - min) / range) * chartHeight;
            ctx.strokeStyle = '#5a6c7d';
            ctx.setLineDash([5, 5]);
            ctx.beginPath();
            ctx.moveTo(padding, zeroY);
            ctx.lineTo(width - padding, zeroY);
            ctx.stroke();
            ctx.setLineDash([]);
        }
        
        // Draw bars
        data.forEach((value, index) => {
            const barHeight = (Math.abs(value) / range) * chartHeight;
            const x = padding + index * barSpacing + (barSpacing - barWidth) / 2;
            const zeroY = height - padding - ((0 - min) / range) * chartHeight;
            const y = value >= 0 ? zeroY - barHeight : zeroY;
            
            ctx.fillStyle = Array.isArray(colors) ? colors[index] : colors;
            ctx.fillRect(x, y, barWidth, barHeight);
        });
        
        // Draw labels
        ctx.fillStyle = CHART_COLORS.TEXT_SECONDARY;
        ctx.font = '11px Inter, sans-serif';
        ctx.textAlign = 'center';
        labels.forEach((label, index) => {
            const x = padding + index * barSpacing + barSpacing / 2;
            const maxLabelWidth = barSpacing - 5;
            const truncatedLabel = label.length > CHART_CONFIG.MAX_LABEL_LENGTH_BAR 
                ? label.substring(0, CHART_CONFIG.MAX_LABEL_LENGTH_BAR) + '...' 
                : label;
            ctx.fillText(truncatedLabel, x, height - padding + 15);
        });
    }
    
    drawLegend(ctx, labels, colors, width, height) {
        const legendY = height - 30;
        const itemWidth = Math.min(width / labels.length, 150);
        const startX = (width - itemWidth * labels.length) / 2;
        
        ctx.font = '12px Inter, sans-serif';
        ctx.textAlign = 'left';
        
        labels.forEach((label, index) => {
            const x = startX + index * itemWidth;
            
            // Draw color box
            ctx.fillStyle = Array.isArray(colors) ? colors[index] : colors;
            ctx.fillRect(x, legendY, 12, 12);
            
            // Draw label
            ctx.fillStyle = CHART_COLORS.TEXT_SECONDARY;
            const truncatedLabel = label.length > CHART_CONFIG.MAX_LABEL_LENGTH_LEGEND 
                ? label.substring(0, CHART_CONFIG.MAX_LABEL_LENGTH_LEGEND) + '...' 
                : label;
            ctx.fillText(truncatedLabel, x + 16, legendY + 10);
        });
    }
    
    renderPlaceholder(ctx, width, height) {
        ctx.fillStyle = '#f5f7fa';
        ctx.fillRect(0, 0, width, height);
        
        ctx.fillStyle = CHART_COLORS.TEXT_SECONDARY;
        ctx.font = '14px Inter, sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('Chart rendered', width / 2, height / 2);
    }
    
    destroy() {
        if (this.canvas) {
            const ctx = this.canvas.getContext('2d');
            ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        }
    }
}

// Make Chart available globally
window.Chart = Chart;
