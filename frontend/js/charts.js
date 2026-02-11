/**
 * Chart.js visualization functions
 * Creates various charts for displaying simulation results
 */

// Color utilities
const COLORS = {
    low: '#00c851',
    moderate: '#f39c12',
    high: '#e67e22',
    critical: '#e74c3c',
    positive: '#0095da',
    negative: '#e74c3c',
    neutral: '#7f8c8d'
};

/**
 * Get risk color based on level
 */
function getRiskColor(level) {
    const levelLower = level.toLowerCase();
    return COLORS[levelLower] || COLORS.neutral;
}

/**
 * Get risk color based on score
 */
function getRiskColorByScore(score) {
    if (score < 25) return COLORS.low;
    if (score < 50) return COLORS.moderate;
    if (score < 75) return COLORS.high;
    return COLORS.critical;
}

/**
 * Create inflation gauge chart
 */
function createInflationChart(canvasId, inflationData) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) {
        console.warn(`Canvas element ${canvasId} not found`);
        return;
    }

    const inflationRate = inflationData.predicted_inflation_rate;
    const baseline = inflationData.baseline_inflation;
    
    // Destroy existing chart
    if (ctx.chart) {
        ctx.chart.destroy();
        ctx.chart = null;
    }

    try {
        ctx.chart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Predicted', 'Safe Zone'],
                datasets: [{
                    data: [inflationRate, Math.max(0, 10 - inflationRate)],
                    backgroundColor: [
                        getRiskColorByScore(inflationRate * 10),
                        'rgba(0, 0, 0, 0.05)'
                    ],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                cutout: '75%',
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `${context.label}: ${context.parsed.toFixed(1)}%`;
                            }
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error creating inflation chart:', error);
    }

    // Update details
    const detailsDiv = document.getElementById('inflation-details');
    if (detailsDiv) {
        detailsDiv.innerHTML = `
            <p><strong>Predicted:</strong> ${inflationRate}%</p>
            <p><strong>Baseline:</strong> ${baseline}%</p>
            <p><strong>Change:</strong> ${inflationData.change_from_baseline > 0 ? '+' : ''}${inflationData.change_from_baseline}%</p>
            <p><strong>Confidence:</strong> ${inflationData.confidence}%</p>
        `;
    }
}

/**
 * Create risk assessment gauge chart
 */
function createRiskChart(canvasId, riskData) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) {
        console.warn(`Canvas element ${canvasId} not found`);
        return;
    }

    const riskScore = riskData.composite_risk_score;
    
    // Destroy existing chart
    if (ctx.chart) {
        ctx.chart.destroy();
        ctx.chart = null;
    }

    try {
        ctx.chart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Risk Score', 'Safe Zone'],
                datasets: [{
                    data: [riskScore, Math.max(0, 100 - riskScore)],
                    backgroundColor: [
                        getRiskColor(riskData.risk_level),
                        'rgba(0, 0, 0, 0.05)'
                    ],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                cutout: '75%',
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `${context.label}: ${context.parsed.toFixed(1)}`;
                            }
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error creating risk chart:', error);
    }

    // Update details
    const detailsDiv = document.getElementById('risk-details');
    if (detailsDiv) {
        const components = riskData.components;
        detailsDiv.innerHTML = `
            <p><strong>Economic Risk:</strong> ${components.economic_risk}</p>
            <p><strong>Sector Disruption:</strong> ${components.sector_disruption_risk}</p>
            <p><strong>Social Unrest:</strong> ${components.social_unrest_risk}</p>
            <p><strong>Inequality Impact:</strong> ${components.income_inequality_risk}</p>
        `;
    }
}

/**
 * Create sector impact radar/bar chart
 */
function createSectorChart(canvasId, sectorData) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) {
        console.warn(`Canvas element ${canvasId} not found`);
        return;
    }

    const sectors = Object.keys(sectorData.sector_impacts);
    const impacts = Object.values(sectorData.sector_impacts);

    // Destroy existing chart
    if (ctx.chart) {
        ctx.chart.destroy();
        ctx.chart = null;
    }

    // Color code bars based on positive/negative impact
    const backgroundColors = impacts.map(impact => 
        impact > 0 ? COLORS.positive : COLORS.negative
    );

    try {
        ctx.chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: sectors,
                datasets: [{
                    label: 'Impact Score',
                    data: impacts,
                    backgroundColor: backgroundColors,
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        min: -1,
                        max: 1,
                        ticks: {
                            color: '#5a6c7d'
                        },
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        }
                    },
                    x: {
                        ticks: {
                            color: '#5a6c7d'
                        },
                        grid: {
                            display: false
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const impact = context.parsed.y;
                                const sentiment = impact > 0 ? 'Positive' : 'Negative';
                                return `${sentiment} Impact: ${Math.abs(impact).toFixed(3)}`;
                            }
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error creating sector chart:', error);
    }
}

/**
 * Create sentiment pie chart
 */
function createSentimentChart(canvasId, sentimentData) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) {
        console.warn(`Canvas element ${canvasId} not found`);
        return;
    }

    // Destroy existing chart
    if (ctx.chart) {
        ctx.chart.destroy();
        ctx.chart = null;
    }

    try {
        ctx.chart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: ['Positive', 'Negative', 'Neutral'],
                datasets: [{
                    data: [
                        sentimentData.positive_ratio,
                        sentimentData.negative_ratio,
                        sentimentData.neutral_ratio
                    ],
                    backgroundColor: [
                        COLORS.positive,
                        COLORS.negative,
                        COLORS.neutral
                    ],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: '#5a6c7d',
                            padding: 15
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `${context.label}: ${context.parsed.toFixed(1)}%`;
                            }
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error creating sentiment chart:', error);
    }

    // Update details
    const detailsDiv = document.getElementById('sentiment-details');
    if (detailsDiv) {
        detailsDiv.innerHTML = `
            <p><strong>Overall Score:</strong> ${sentimentData.overall_sentiment_score}</p>
            <p><strong>Category:</strong> ${sentimentData.sentiment_category}</p>
            <p><strong>Unrest Probability:</strong> ${(sentimentData.social_unrest_probability * 100).toFixed(1)}%</p>
            <p><strong>Key Concerns:</strong> ${sentimentData.key_concerns.join(', ')}</p>
        `;
    }
}

/**
 * Create comparison bar chart
 */
function createComparisonChart(canvasId, comparisonData) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) {
        console.warn(`Canvas element ${canvasId} not found`);
        return;
    }

    const scenarioNames = comparisonData.map(s => s.name);
    const riskScores = comparisonData.map(s => s.risk_score);
    const inflationRates = comparisonData.map(s => s.inflation_rate);

    // Destroy existing chart
    if (ctx.chart) {
        ctx.chart.destroy();
        ctx.chart = null;
    }

    try {
        ctx.chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: scenarioNames,
                datasets: [
                    {
                        label: 'Risk Score',
                        data: riskScores,
                        backgroundColor: COLORS.negative,
                        yAxisID: 'y'
                    },
                    {
                        label: 'Inflation Rate (%)',
                        data: inflationRates,
                        backgroundColor: COLORS.positive,
                        yAxisID: 'y1'
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                scales: {
                    y: {
                        type: 'linear',
                        position: 'left',
                        title: {
                            display: true,
                            text: 'Risk Score',
                            color: '#5a6c7d'
                        },
                        ticks: {
                            color: '#5a6c7d'
                        },
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        }
                    },
                    y1: {
                        type: 'linear',
                        position: 'right',
                        title: {
                            display: true,
                            text: 'Inflation Rate (%)',
                            color: '#5a6c7d'
                        },
                        ticks: {
                            color: '#5a6c7d'
                        },
                        grid: {
                            display: false
                        }
                    },
                    x: {
                        ticks: {
                            color: '#5a6c7d'
                        },
                        grid: {
                            display: false
                        }
                    }
                },
                plugins: {
                    legend: {
                        labels: {
                            color: '#5a6c7d'
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error creating comparison chart:', error);
    }
}
