// ==================== CONVERTISSEUR D'UNITÉS ====================

class UnitConverter {
    constructor() {
        this.currentCategory = '';
        this.fromUnit = '';
        this.toUnit = '';
        this.conversionHistory = [];
        
        this.initializeElements();
        this.attachEventListeners();
        this.loadInitialCategory();
        this.loadHistory();
        
        console.log('Convertisseur d\'unités initialisé');
    }

    initializeElements() {
        this.categorySelect = document.getElementById('category-select');
        this.fromUnitSelect = document.getElementById('from-unit');
        this.toUnitSelect = document.getElementById('to-unit');
        this.inputValue = document.getElementById('input-value');
        this.outputValue = document.getElementById('output-value');
        this.convertButton = document.getElementById('convert-btn');
        this.swapButton = document.getElementById('swap-units');
        this.historyContainer = document.getElementById('conversion-history');
        this.clearHistoryButton = document.getElementById('clear-conversion-history');
        this.conversionInfo = document.getElementById('conversion-info');
        this.unitsGuide = document.getElementById('units-guide');
        this.quickConversionTable = document.getElementById('quick-conversion-table');
        
        if (!this.categorySelect || !this.fromUnitSelect) {
            console.error('Éléments du convertisseur non trouvés');
            return;
        }
    }

    attachEventListeners() {
        // Changement de catégorie
        if (this.categorySelect) {
            this.categorySelect.addEventListener('change', (e) => {
                this.loadUnitsForCategory(e.target.value);
            });
        }
        
        // Bouton de conversion
        if (this.convertButton) {
            this.convertButton.addEventListener('click', () => this.performConversion());
        }
        
        // Bouton d'échange des unités
        if (this.swapButton) {
            this.swapButton.addEventListener('click', () => this.swapUnits());
        }
        
        // Conversion automatique lors de la saisie
        if (this.inputValue) {
            this.inputValue.addEventListener('input', AppUtils.debounce(() => {
                if (this.inputValue.value.trim() !== '') {
                    this.performConversion();
                }
            }, 500));
            
            this.inputValue.addEventListener('keydown', (e) => {
                if (e.key === 'Enter') {
                    this.performConversion();
                }
            });
        }
        
        // Changement d'unités
        if (this.fromUnitSelect) {
            this.fromUnitSelect.addEventListener('change', () => {
                if (this.inputValue.value.trim() !== '') {
                    this.performConversion();
                }
                this.updateQuickConversionTable();
            });
        }
        
        if (this.toUnitSelect) {
            this.toUnitSelect.addEventListener('change', () => {
                if (this.inputValue.value.trim() !== '') {
                    this.performConversion();
                }
                this.updateQuickConversionTable();
            });
        }
        
        // Effacer l'historique
        if (this.clearHistoryButton) {
            this.clearHistoryButton.addEventListener('click', () => this.clearHistory());
        }
    }

    async loadInitialCategory() {
        if (this.categorySelect && this.categorySelect.options.length > 0) {
            const firstCategory = this.categorySelect.options[0].value;
            await this.loadUnitsForCategory(firstCategory);
        }
    }

    async loadUnitsForCategory(category) {
        this.currentCategory = category;
        
        try {
            const response = await AppUtils.apiCall(`/api/convert/units/${encodeURIComponent(category)}`);
            
            if (response.success) {
                this.populateUnitSelects(response.units);
                this.updateUnitsGuide(response.units);
                this.updateQuickConversionTable();
            }
        } catch (error) {
            console.error('Erreur lors du chargement des unités:', error);
            AppUtils.showAlert('Erreur lors du chargement des unités');
        }
    }

    populateUnitSelects(units) {
        // Vider les selects
        this.fromUnitSelect.innerHTML = '';
        this.toUnitSelect.innerHTML = '';
        
        // Ajouter les options
        units.forEach(unit => {
            const fromOption = new Option(unit, unit);
            const toOption = new Option(unit, unit);
            
            this.fromUnitSelect.add(fromOption);
            this.toUnitSelect.add(toOption);
        });
        
        // Sélectionner différentes unités par défaut si possible
        if (units.length > 1) {
            this.fromUnitSelect.selectedIndex = 0;
            this.toUnitSelect.selectedIndex = 1;
        }
        
        // Sauvegarder les sélections
        this.fromUnit = this.fromUnitSelect.value;
        this.toUnit = this.toUnitSelect.value;
    }

    async performConversion() {
        const inputVal = this.inputValue.value.trim();
        if (!inputVal || !AppUtils.validateNumberInput(inputVal)) {
            this.outputValue.value = '';
            return;
        }

        const value = parseFloat(inputVal);
        const fromUnit = this.fromUnitSelect.value;
        const toUnit = this.toUnitSelect.value;
        
        if (!fromUnit || !toUnit) {
            AppUtils.showAlert('Veuillez sélectionner les unités de conversion');
            return;
        }

        try {
            // Afficher un indicateur de chargement
            this.outputValue.value = 'Conversion...';
            
            const response = await AppUtils.apiCall('/api/convert', {
                method: 'POST',
                body: JSON.stringify({
                    value: value,
                    from_unit: fromUnit,
                    to_unit: toUnit,
                    category: this.currentCategory
                })
            });

            if (response.success) {
                const formattedResult = AppUtils.formatNumber(response.result);
                this.outputValue.value = formattedResult;
                
                // Ajouter à l'historique
                this.addToHistory({
                    value: value,
                    fromUnit: fromUnit,
                    toUnit: toUnit,
                    result: formattedResult,
                    category: this.currentCategory
                });
                
                // Afficher les informations de conversion
                this.showConversionInfo(value, fromUnit, formattedResult, toUnit);
                
                this.updateHistoryDisplay();
            }
        } catch (error) {
            this.outputValue.value = 'Erreur';
            console.error('Erreur de conversion:', error);
        }
    }

    swapUnits() {
        if (!this.fromUnitSelect.value || !this.toUnitSelect.value) return;
        
        // Échanger les sélections d'unités
        const tempFromIndex = this.fromUnitSelect.selectedIndex;
        this.fromUnitSelect.selectedIndex = this.toUnitSelect.selectedIndex;
        this.toUnitSelect.selectedIndex = tempFromIndex;
        
        // Échanger les valeurs
        const tempValue = this.inputValue.value;
        this.inputValue.value = this.outputValue.value;
        this.outputValue.value = tempValue;
        
        // Effectuer la conversion si il y a une valeur
        if (this.inputValue.value.trim() !== '') {
            this.performConversion();
        }
        
        this.updateQuickConversionTable();
        AppUtils.showAlert('Unités échangées', 'success', 1500);
    }

    showConversionInfo(inputValue, fromUnit, outputValue, toUnit) {
        if (!this.conversionInfo) return;
        
        const formula = `${inputValue} ${fromUnit} = ${outputValue} ${toUnit}`;
        const formulaElement = document.getElementById('conversion-formula');
        
        if (formulaElement) {
            formulaElement.textContent = formula;
            this.conversionInfo.classList.remove('d-none');
            
            // Masquer après 5 secondes
            setTimeout(() => {
                this.conversionInfo.classList.add('d-none');
            }, 5000);
        }
    }

    updateUnitsGuide(units) {
        if (!this.unitsGuide) return;
        
        const descriptions = this.getUnitDescriptions(this.currentCategory);
        
        let guideHTML = `<h6 class="text-info">${this.currentCategory}</h6>`;
        guideHTML += '<div class="row">';
        
        units.forEach(unit => {
            const description = descriptions[unit] || unit;
            guideHTML += `
                <div class="col-6 mb-2">
                    <small><strong>${unit}</strong>: ${description}</small>
                </div>
            `;
        });
        
        guideHTML += '</div>';
        this.unitsGuide.innerHTML = guideHTML;
    }

    getUnitDescriptions(category) {
        const descriptions = {
            'Longueur': {
                'm': 'Mètre',
                'km': 'Kilomètre', 
                'cm': 'Centimètre',
                'mm': 'Millimètre',
                'in': 'Pouce',
                'ft': 'Pied',
                'yd': 'Yard',
                'mi': 'Mile'
            },
            'Masse': {
                'kg': 'Kilogramme',
                'g': 'Gramme',
                'mg': 'Milligramme',
                'lb': 'Livre',
                'oz': 'Once'
            },
            'Température': {
                'C': 'Celsius',
                'F': 'Fahrenheit',
                'K': 'Kelvin'
            },
            'Volume': {
                'L': 'Litre',
                'mL': 'Millilitre',
                'm³': 'Mètre cube',
                'ft³': 'Pied cube',
                'gal': 'Gallon',
                'pt': 'Pinte'
            },
            'Temps': {
                's': 'Seconde',
                'ms': 'Milliseconde',
                'min': 'Minute',
                'h': 'Heure',
                'd': 'Jour'
            }
        };
        
        return descriptions[category] || {};
    }

    updateQuickConversionTable() {
        if (!this.quickConversionTable || !this.fromUnitSelect.value || !this.toUnitSelect.value) return;
        
        const fromUnit = this.fromUnitSelect.value;
        const toUnit = this.toUnitSelect.value;
        const testValues = [1, 5, 10, 25, 50, 100];
        
        let tableHTML = `
            <h6>Conversion rapide: ${fromUnit} → ${toUnit}</h6>
            <div class="table-responsive">
                <table class="table table-dark table-sm">
                    <thead>
                        <tr>
                            <th>${fromUnit}</th>
                            <th>${toUnit}</th>
                        </tr>
                    </thead>
                    <tbody>
        `;
        
        testValues.forEach(value => {
            tableHTML += `
                <tr>
                    <td>${value}</td>
                    <td class="quick-conversion-result" data-value="${value}">Calcul...</td>
                </tr>
            `;
        });
        
        tableHTML += `
                    </tbody>
                </table>
            </div>
        `;
        
        this.quickConversionTable.innerHTML = tableHTML;
        
        // Calculer les conversions pour le tableau
        this.calculateQuickConversions(testValues, fromUnit, toUnit);
    }

    async calculateQuickConversions(values, fromUnit, toUnit) {
        for (const value of values) {
            try {
                const response = await AppUtils.apiCall('/api/convert', {
                    method: 'POST',
                    body: JSON.stringify({
                        value: value,
                        from_unit: fromUnit,
                        to_unit: toUnit,
                        category: this.currentCategory
                    })
                });

                if (response.success) {
                    const resultElement = document.querySelector(`[data-value="${value}"]`);
                    if (resultElement) {
                        resultElement.textContent = AppUtils.formatNumber(response.result);
                    }
                }
            } catch (error) {
                const resultElement = document.querySelector(`[data-value="${value}"]`);
                if (resultElement) {
                    resultElement.textContent = 'Erreur';
                }
            }
        }
    }

    addToHistory(conversion) {
        conversion.timestamp = new Date().toISOString();
        conversion.id = Date.now();
        
        this.conversionHistory.unshift(conversion);
        
        // Limiter l'historique
        if (this.conversionHistory.length > 30) {
            this.conversionHistory = this.conversionHistory.slice(0, 30);
        }
        
        this.saveHistory();
    }

    updateHistoryDisplay() {
        if (!this.historyContainer) return;
        
        if (this.conversionHistory.length === 0) {
            this.historyContainer.innerHTML = '<p class="text-muted">Aucune conversion dans l\'historique</p>';
            return;
        }
        
        const historyHTML = this.conversionHistory.slice(0, 10).map(item => `
            <div class="history-item" onclick="unitConverter.useHistoryItem(${item.value}, '${item.fromUnit}', '${item.toUnit}')">
                <div class="history-expression">
                    ${item.value} ${item.fromUnit} → ${item.toUnit}
                </div>
                <div class="history-result">${item.result} ${item.toUnit}</div>
                <div class="history-timestamp">
                    ${AppUtils.formatTimestamp(item.timestamp)} (${item.category})
                </div>
            </div>
        `).join('');
        
        this.historyContainer.innerHTML = historyHTML;
    }

    useHistoryItem(value, fromUnit, toUnit) {
        // Sélectionner la bonne catégorie si nécessaire
        const historyItem = this.conversionHistory.find(item => 
            item.value === value && item.fromUnit === fromUnit && item.toUnit === toUnit
        );
        
        if (historyItem && historyItem.category !== this.currentCategory) {
            this.categorySelect.value = historyItem.category;
            this.loadUnitsForCategory(historyItem.category).then(() => {
                this.setConversionValues(value, fromUnit, toUnit);
            });
        } else {
            this.setConversionValues(value, fromUnit, toUnit);
        }
    }

    setConversionValues(value, fromUnit, toUnit) {
        this.inputValue.value = value;
        this.fromUnitSelect.value = fromUnit;
        this.toUnitSelect.value = toUnit;
        this.performConversion();
        AppUtils.showAlert('Conversion chargée depuis l\'historique', 'success', 2000);
    }

    clearHistory() {
        this.conversionHistory = [];
        this.saveHistory();
        this.updateHistoryDisplay();
        AppUtils.showAlert('Historique des conversions effacé', 'success', 2000);
    }

    saveHistory() {
        AppUtils.saveToLocalStorage('conversion_history', this.conversionHistory);
    }

    loadHistory() {
        this.conversionHistory = AppUtils.loadFromLocalStorage('conversion_history', []);
        this.updateHistoryDisplay();
    }
}

// ==================== INITIALISATION ====================

document.addEventListener('DOMContentLoaded', function() {
    // Vérifier si nous sommes sur la page du convertisseur
    if (document.getElementById('category-select')) {
        window.unitConverter = new UnitConverter();
        console.log('Page convertisseur d\'unités chargée');
    }
});

// ==================== FONCTIONS D'EXPORT ====================

function exportConversionHistory() {
    if (!window.unitConverter) return;
    
    const data = {
        type: 'SmartCalc Conversion History',
        exported: new Date().toISOString(),
        history: window.unitConverter.conversionHistory
    };
    
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = `smartcalc-conversions-${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    
    URL.revokeObjectURL(url);
    AppUtils.showAlert('Historique des conversions exporté', 'success', 2000);
}