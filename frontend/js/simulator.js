/**
 * Policy Simulator UI Logic
 * Handles form interactions and simulation management
 */

class PolicySimulator {
    constructor() {
        this.scenarios = [];
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        // Policy form submission
        const policyForm = document.getElementById('policy-form');
        if (policyForm) {
            policyForm.addEventListener('submit', (e) => this.handleSimulation(e));
        }

        // Magnitude slider
        const magnitudeSlider = document.getElementById('magnitude');
        const magnitudeValue = document.getElementById('magnitude-value');
        if (magnitudeSlider && magnitudeValue) {
            magnitudeSlider.addEventListener('input', (e) => {
                const value = e.target.value;
                magnitudeValue.textContent = `${value}%`;
                
                // Color code based on value
                if (Math.abs(value) < 10) {
                    magnitudeValue.style.color = 'var(--accent-green)';
                } else if (Math.abs(value) < 25) {
                    magnitudeValue.style.color = 'var(--accent-yellow)';
                } else {
                    magnitudeValue.style.color = 'var(--accent-red)';
                }
            });
        }

        // Scenario management
        const addScenarioBtn = document.getElementById('add-scenario-btn');
        if (addScenarioBtn) {
            addScenarioBtn.addEventListener('click', () => this.addScenario());
        }

        const compareBtn = document.getElementById('compare-btn');
        if (compareBtn) {
            compareBtn.addEventListener('click', () => this.handleComparison());
        }
    }

    /**
     * Handle policy simulation
     */
    async handleSimulation(event) {
        event.preventDefault();

        const form = event.target;
        const formData = new FormData(form);

        // Collect affected sectors
        const affectedSectors = Array.from(
            form.querySelectorAll('input[name="sectors"]:checked')
        ).map(input => input.value);

        // Prepare policy data
        const policyData = {
            policy_type: formData.get('policy_type'),
            magnitude: parseFloat(formData.get('magnitude')),
            duration_months: parseInt(formData.get('duration_months')),
            affected_sectors: affectedSectors.length > 0 ? affectedSectors : null,
            description: formData.get('description') || ''
        };

        // Show loading
        this.showLoading(true);

        try {
            // Call API
            const result = await apiClient.simulatePolicy(policyData);

            // Display results
            this.displayResults(result);

            // Scroll to results
            document.getElementById('results-dashboard').scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        } catch (error) {
            console.error('Simulation error:', error);
            alert('Error running simulation: ' + error.message);
        } finally {
            this.showLoading(false);
        }
    }

    /**
     * Display simulation results
     */
    displayResults(result) {
        // Show results dashboard
        const dashboard = document.getElementById('results-dashboard');
        dashboard.classList.remove('hidden');

        // Update summary cards
        this.updateSummaryCards(result);

        // Create charts
        createInflationChart('inflation-chart', result.inflation_impact);
        createRiskChart('risk-chart', result.risk_assessment);
        createSectorChart('sector-chart', result.sector_impacts);
        createSentimentChart('sentiment-chart', result.sentiment_analysis);

        // Display recommendations
        this.displayRecommendations(result.recommendations);

        // Animate in
        dashboard.style.animation = 'fadeIn 0.5s ease';
    }

    /**
     * Update summary cards
     */
    updateSummaryCards(result) {
        // Inflation
        const inflationValue = document.getElementById('inflation-value');
        if (inflationValue) {
            const rate = result.inflation_impact.predicted_inflation_rate;
            inflationValue.textContent = `${rate}%`;
            inflationValue.style.color = getRiskColorByScore(rate * 10);
        }

        // Risk level
        const riskLevelValue = document.getElementById('risk-level-value');
        if (riskLevelValue) {
            const level = result.risk_assessment.risk_level;
            riskLevelValue.textContent = level;
            riskLevelValue.style.color = getRiskColor(level);
        }

        // Sentiment
        const sentimentValue = document.getElementById('sentiment-value');
        if (sentimentValue) {
            const category = result.sentiment_analysis.sentiment_category;
            sentimentValue.textContent = category;
            sentimentValue.style.color = 
                category === 'Positive' ? 'var(--accent-green)' :
                category === 'Negative' ? 'var(--accent-red)' :
                'var(--text-secondary)';
        }

        // Most affected sectors
        const affectedSectorsValue = document.getElementById('affected-sectors-value');
        if (affectedSectorsValue) {
            const mostAffected = result.sector_impacts.most_affected
                .slice(0, 3)
                .map(s => s.sector)
                .join(', ');
            affectedSectorsValue.textContent = mostAffected;
        }
    }

    /**
     * Display recommendations
     */
    displayRecommendations(recommendations) {
        const listContainer = document.getElementById('recommendations-list');
        if (!listContainer) return;

        listContainer.innerHTML = '';
        recommendations.forEach(rec => {
            const item = document.createElement('div');
            item.className = 'recommendation-item';
            item.textContent = rec;
            listContainer.appendChild(item);
        });
    }

    /**
     * Add a new scenario for comparison
     */
    addScenario() {
        const scenarioId = Date.now();
        const scenariosList = document.getElementById('scenarios-list');
        
        const scenarioHtml = `
            <div class="scenario-item" data-scenario-id="${scenarioId}">
                <div class="scenario-form">
                    <input type="text" placeholder="Scenario name" class="scenario-name" required>
                    <select class="scenario-policy-type" required>
                        <option value="">Select policy...</option>
                        <option value="Fuel Price Change">Fuel Price Change</option>
                        <option value="Tax Reform">Tax Reform</option>
                        <option value="Subsidy Change">Subsidy Change</option>
                        <option value="Minimum Wage Change">Minimum Wage Change</option>
                        <option value="Environmental Regulation">Environmental Regulation</option>
                        <option value="Import/Export Tariff">Import/Export Tariff</option>
                    </select>
                    <input type="number" placeholder="Magnitude (%)" class="scenario-magnitude" min="-50" max="50" step="0.5" required>
                    <input type="number" placeholder="Duration (months)" class="scenario-duration" min="1" max="60" value="12" required>
                </div>
                <button type="button" class="btn-secondary" onclick="simulator.removeScenario(${scenarioId})">
                    ❌ Remove
                </button>
            </div>
        `;
        
        scenariosList.insertAdjacentHTML('beforeend', scenarioHtml);
        this.scenarios.push(scenarioId);
        
        // Enable compare button if at least 2 scenarios
        const compareBtn = document.getElementById('compare-btn');
        if (this.scenarios.length >= 2) {
            compareBtn.disabled = false;
        }
    }

    /**
     * Remove a scenario
     */
    removeScenario(scenarioId) {
        const scenarioElement = document.querySelector(`[data-scenario-id="${scenarioId}"]`);
        if (scenarioElement) {
            scenarioElement.remove();
        }
        
        this.scenarios = this.scenarios.filter(id => id !== scenarioId);
        
        // Disable compare button if less than 2 scenarios
        const compareBtn = document.getElementById('compare-btn');
        if (this.scenarios.length < 2) {
            compareBtn.disabled = true;
        }
    }

    /**
     * Handle scenario comparison
     */
    async handleComparison() {
        const scenarioElements = document.querySelectorAll('.scenario-item');
        
        if (scenarioElements.length < 2) {
            alert('Please add at least 2 scenarios to compare');
            return;
        }

        // Collect scenario data
        const scenarios = [];
        for (const element of scenarioElements) {
            const name = element.querySelector('.scenario-name').value;
            const policyType = element.querySelector('.scenario-policy-type').value;
            const magnitude = parseFloat(element.querySelector('.scenario-magnitude').value);
            const duration = parseInt(element.querySelector('.scenario-duration').value);

            if (!name || !policyType || isNaN(magnitude) || isNaN(duration)) {
                alert('Please fill in all scenario fields');
                return;
            }

            scenarios.push({
                name,
                policy_type: policyType,
                magnitude,
                duration_months: duration
            });
        }

        // Show loading
        this.showLoading(true);

        try {
            // Call API
            const result = await apiClient.compareScenarios(scenarios);

            // Display comparison results
            this.displayComparisonResults(result);
        } catch (error) {
            console.error('Comparison error:', error);
            alert('Error comparing scenarios: ' + error.message);
        } finally {
            this.showLoading(false);
        }
    }

    /**
     * Display comparison results
     */
    displayComparisonResults(result) {
        const resultsContainer = document.getElementById('comparison-results');
        resultsContainer.classList.remove('hidden');

        // Display comparison table
        this.displayComparisonTable(result.comparison_table);

        // Display recommendation
        const recommendationDiv = document.getElementById('comparison-recommendation');
        recommendationDiv.innerHTML = `<h4>Recommendation</h4><p>${result.recommendation.replace(/\n/g, '<br>')}</p>`;

        // Create comparison chart
        createComparisonChart('comparison-chart', result.comparison_table);

        // Scroll to results
        resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    /**
     * Display comparison table
     */
    displayComparisonTable(comparisonData) {
        const container = document.getElementById('comparison-table-container');
        
        const tableHtml = `
            <table class="comparison-table">
                <thead>
                    <tr>
                        <th>Rank</th>
                        <th>Scenario</th>
                        <th>Inflation Rate</th>
                        <th>Risk Score</th>
                        <th>Risk Level</th>
                        <th>Sentiment</th>
                    </tr>
                </thead>
                <tbody>
                    ${comparisonData.map(row => `
                        <tr>
                            <td><span class="rank-badge rank-${row.rank}">${row.rank}</span></td>
                            <td>${row.name}</td>
                            <td>${row.inflation_rate}%</td>
                            <td>${row.risk_score}</td>
                            <td class="risk-${row.risk_level}">${row.risk_level}</td>
                            <td>${row.sentiment}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
        
        container.innerHTML = tableHtml;
    }

    /**
     * Show/hide loading overlay
     */
    showLoading(show) {
        const overlay = document.getElementById('loading-overlay');
        if (show) {
            overlay.classList.remove('hidden');
        } else {
            overlay.classList.add('hidden');
        }
    }
}

// Initialize simulator
const simulator = new PolicySimulator();
