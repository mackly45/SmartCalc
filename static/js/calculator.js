// ==================== CALCULATRICE STANDARD ====================

class StandardCalculator {
    constructor() {
        this.currentValue = '0';
        this.expression = '';
        this.isWaitingForOperand = true;
        
        this.initializeElements();
        this.attachEventListeners();
        this.setupKeyboardShortcuts();
        
        console.log('Calculatrice standard initialisée');
    }

    initializeElements() {
        this.expressionDisplay = document.getElementById('expression-display');
        this.resultDisplay = document.getElementById('result-display');
        this.buttons = document.querySelectorAll('.calc-btn');
        
        if (!this.resultDisplay) {
            console.error('Éléments de la calculatrice non trouvés');
            return;
        }
        
        this.updateDisplay();
    }

    attachEventListeners() {
        this.buttons.forEach(button => {
            button.addEventListener('click', (event) => {
                this.handleButtonClick(event.target);
            });
        });
    }

    setupKeyboardShortcuts() {
        // Raccourcis clavier pour la calculatrice
        const shortcuts = {
            '0': () => this.appendNumber('0'),
            '1': () => this.appendNumber('1'),
            '2': () => this.appendNumber('2'),
            '3': () => this.appendNumber('3'),
            '4': () => this.appendNumber('4'),
            '5': () => this.appendNumber('5'),
            '6': () => this.appendNumber('6'),
            '7': () => this.appendNumber('7'),
            '8': () => this.appendNumber('8'),
            '9': () => this.appendNumber('9'),
            '+': () => this.addOperator('+'),
            '-': () => this.addOperator('-'),
            '*': () => this.addOperator('×'),
            '/': () => this.addOperator('÷'),
            'enter': () => this.calculate(),
            '=': () => this.calculate(),
            '.': () => this.addDecimal(),
            'escape': () => this.clear(),
            'c': () => this.clear(),
            'backspace': () => this.backspace(),
            '%': () => this.percentage()
        };

        Object.keys(shortcuts).forEach(key => {
            keyboardManager.addShortcut(key, shortcuts[key]);
        });
    }

    handleButtonClick(button) {
        AppUtils.addButtonAnimation(button);
        
        const action = button.dataset.action;
        const value = button.dataset.value;
        
        switch (action) {
            case 'clear':
                this.clear();
                break;
            case 'number':
                this.appendNumber(value);
                break;
            case 'operator':
                this.addOperator(value);
                break;
            case 'equals':
                this.calculate();
                break;
            case 'decimal':
                this.addDecimal();
                break;
            case 'percentage':
                this.percentage();
                break;
            case 'toggle_sign':
                this.toggleSign();
                break;
        }
    }

    async performCalculation(action, value = '') {
        try {
            const response = await AppUtils.apiCall('/api/calculate', {
                method: 'POST',
                body: JSON.stringify({
                    action: action,
                    value: value
                })
            });

            if (response.success) {
                this.currentValue = response.current_value;
                this.expression = response.expression;
                this.updateDisplay();
                
                // Si c'est un calcul complet, ajouter à l'historique
                if (action === 'equals' && response.current_value !== 'Error') {
                    this.addToHistory(this.expression, this.currentValue);
                }
            }
        } catch (error) {
            this.currentValue = 'Error';
            this.updateDisplay();
        }
    }

    appendNumber(number) {
        this.performCalculation('number', number);
    }

    addOperator(operator) {
        this.performCalculation('operator', operator);
    }

    calculate() {
        this.performCalculation('equals');
    }

    addDecimal() {
        this.performCalculation('decimal');
    }

    percentage() {
        this.performCalculation('percentage');
    }

    toggleSign() {
        this.performCalculation('toggle_sign');
    }

    clear() {
        this.performCalculation('clear');
    }

    backspace() {
        // Fonction pour supprimer le dernier caractère
        if (this.currentValue.length > 1) {
            this.currentValue = this.currentValue.slice(0, -1);
        } else {
            this.currentValue = '0';
        }
        this.updateDisplay();
    }

    updateDisplay() {
        if (this.resultDisplay) {
            this.resultDisplay.textContent = this.currentValue;
        }
        
        if (this.expressionDisplay) {
            this.expressionDisplay.textContent = this.expression;
        }
    }

    addToHistory(expression, result) {
        if (typeof addToCalculatorHistory === 'function') {
            addToCalculatorHistory({
                expression: expression,
                result: result,
                type: 'standard'
            });
        }
    }
}

// ==================== HISTORIQUE CALCULATRICE ====================

class CalculatorHistory extends HistoryManager {
    constructor() {
        super('calculator', 20);
        this.historyContainer = document.getElementById('calculator-history');
        this.renderHistory();
    }

    renderHistory() {
        if (!this.historyContainer) return;

        if (this.history.length === 0) {
            this.historyContainer.innerHTML = '<p class="text-muted">Aucun calcul dans l\'historique</p>';
            return;
        }

        const historyHTML = this.history.map(item => `
            <div class="history-item" onclick="calculatorHistory.useHistoryItem('${item.result}')">
                <div class="history-expression">${item.expression || 'Calcul direct'}</div>
                <div class="history-result">${item.result}</div>
                <div class="history-timestamp">${AppUtils.formatTimestamp(item.timestamp)}</div>
            </div>
        `).join('');

        this.historyContainer.innerHTML = historyHTML;
    }

    useHistoryItem(result) {
        // Utiliser le résultat dans la calculatrice
        if (window.calculator) {
            window.calculator.currentValue = result;
            window.calculator.expression = '';
            window.calculator.updateDisplay();
            AppUtils.showAlert('Résultat utilisé dans la calculatrice', 'success', 2000);
        }
    }
}

// ==================== FONCTIONS GLOBALES ====================

function addToCalculatorHistory(item) {
    if (window.calculatorHistory) {
        window.calculatorHistory.addItem(item);
    }
}

function clearCalculatorHistory() {
    if (window.calculatorHistory) {
        window.calculatorHistory.clear();
        AppUtils.showAlert('Historique effacé', 'success', 2000);
    }
}

// ==================== INITIALISATION ====================

document.addEventListener('DOMContentLoaded', function() {
    // Vérifier si nous sommes sur la page de la calculatrice
    if (document.querySelector('.calculator-display')) {
        window.calculator = new StandardCalculator();
        
        // Initialiser l'historique si le conteneur existe
        if (document.getElementById('calculator-history')) {
            window.calculatorHistory = new CalculatorHistory();
            
            // Bouton pour effacer l'historique
            const clearHistoryBtn = document.getElementById('clear-calc-history');
            if (clearHistoryBtn) {
                clearHistoryBtn.addEventListener('click', clearCalculatorHistory);
            }
        }
        
        console.log('Page calculatrice standard chargée');
    }
});

// ==================== FONCTIONS D'EXPORT ====================

// Fonction pour exporter l'historique
function exportCalculatorHistory() {
    if (!window.calculatorHistory) return;
    
    const data = {
        type: 'SmartCalc Calculator History',
        exported: new Date().toISOString(),
        history: window.calculatorHistory.getHistory()
    };
    
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = `smartcalc-history-${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    
    URL.revokeObjectURL(url);
    AppUtils.showAlert('Historique exporté', 'success', 2000);
}

// Fonction pour importer l'historique
function importCalculatorHistory(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    const reader = new FileReader();
    reader.onload = function(e) {
        try {
            const data = JSON.parse(e.target.result);
            if (data.type === 'SmartCalc Calculator History' && data.history) {
                window.calculatorHistory.history = data.history;
                window.calculatorHistory.saveHistory();
                window.calculatorHistory.renderHistory();
                AppUtils.showAlert('Historique importé avec succès', 'success', 3000);
            } else {
                throw new Error('Format de fichier invalide');
            }
        } catch (error) {
            AppUtils.showAlert('Erreur lors de l\'importation: ' + error.message);
        }
    };
    reader.readAsText(file);
}