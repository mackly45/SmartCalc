// ==================== CALCULATRICE SCIENTIFIQUE ====================

class ScientificCalculator {
    constructor() {
        this.angleMode = 'DEG';
        this.memory = 0;
        this.history = [];
        
        this.initializeElements();
        this.attachEventListeners();
        this.setupKeyboardShortcuts();
        this.loadAngleMode();
        
        console.log('Calculatrice scientifique initialisée');
    }

    initializeElements() {
        this.input = document.getElementById('scientific-input');
        this.result = document.getElementById('scientific-result');
        this.calcButton = document.getElementById('calc-scientific');
        this.clearButton = document.getElementById('clear-scientific');
        this.backspaceButton = document.getElementById('backspace-scientific');
        this.historyContainer = document.getElementById('scientific-history');
        this.clearHistoryButton = document.getElementById('clear-history');
        
        // Boutons de mode d'angle
        this.angleModeButtons = document.querySelectorAll('input[name="angle-mode"]');
        
        // Boutons de fonctions
        this.functionButtons = document.querySelectorAll('.func-btn');
        this.insertButtons = document.querySelectorAll('.insert-btn');
        
        if (!this.input || !this.result) {
            console.error('Éléments de la calculatrice scientifique non trouvés');
            return;
        }
    }

    attachEventListeners() {
        // Bouton de calcul
        if (this.calcButton) {
            this.calcButton.addEventListener('click', () => this.calculate());
        }
        
        // Bouton d'effacement
        if (this.clearButton) {
            this.clearButton.addEventListener('click', () => this.clearInput());
        }
        
        // Bouton de retour arrière
        if (this.backspaceButton) {
            this.backspaceButton.addEventListener('click', () => this.backspace());
        }
        
        // Boutons de mode d'angle
        this.angleModeButtons.forEach(button => {
            button.addEventListener('change', (e) => {
                if (e.target.checked) {
                    this.setAngleMode(e.target.value);
                }
            });
        });
        
        // Boutons de fonctions
        this.functionButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                this.insertFunction(e.target.dataset.function);
                AppUtils.addButtonAnimation(e.target);
            });
        });
        
        // Boutons d'insertion
        this.insertButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                this.insertText(e.target.dataset.value);
                AppUtils.addButtonAnimation(e.target);
            });
        });
        
        // Effacer l'historique
        if (this.clearHistoryButton) {
            this.clearHistoryButton.addEventListener('click', () => this.clearHistory());
        }
        
        // Calcul automatique lors de l'appui sur Entrée
        if (this.input) {
            this.input.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    this.calculate();
                }
            });
        }
    }

    setupKeyboardShortcuts() {
        const shortcuts = {
            'ctrl+enter': () => this.calculate(),
            'ctrl+l': () => this.clearInput(),
            'ctrl+h': () => this.clearHistory(),
            'ctrl+d': () => this.setAngleMode('DEG'),
            'ctrl+r': () => this.setAngleMode('RAD'),
            'ctrl+g': () => this.setAngleMode('GRAD')
        };

        Object.keys(shortcuts).forEach(key => {
            keyboardManager.addShortcut(key, shortcuts[key]);
        });
    }

    async calculate() {
        const expression = this.input.value.trim();
        if (!expression) {
            AppUtils.showAlert('Veuillez entrer une expression');
            return;
        }

        try {
            const response = await AppUtils.apiCall('/api/scientific/calculate', {
                method: 'POST',
                body: JSON.stringify({
                    expression: expression,
                    variables: this.getVariables()
                })
            });

            if (response.success) {
                const formattedResult = AppUtils.formatNumber(response.result);
                this.result.textContent = `= ${formattedResult}`;
                this.result.className = 'result-display text-success';
                
                // Ajouter à l'historique local
                this.addToHistory(expression, formattedResult);
                this.updateHistoryDisplay();
                
                // Copier le résultat dans le presse-papier (optionnel)
                // AppUtils.copyToClipboard(formattedResult);
            }
        } catch (error) {
            this.result.textContent = `Erreur: ${error.message}`;
            this.result.className = 'result-display text-danger';
        }
    }

    async setAngleMode(mode) {
        this.angleMode = mode;
        AppUtils.saveToLocalStorage('scientific_angle_mode', mode);
        
        try {
            await AppUtils.apiCall('/api/scientific/angle-mode', {
                method: 'POST',
                body: JSON.stringify({ mode: mode })
            });
            
            AppUtils.showAlert(`Mode d'angle changé en ${mode}`, 'success', 2000);
        } catch (error) {
            console.error('Erreur lors du changement de mode d\'angle:', error);
        }
    }

    loadAngleMode() {
        const savedMode = AppUtils.loadFromLocalStorage('scientific_angle_mode', 'DEG');
        this.angleMode = savedMode;
        
        // Cocher le bon bouton radio
        const modeButton = document.getElementById(savedMode.toLowerCase());
        if (modeButton) {
            modeButton.checked = true;
        }
    }

    insertFunction(functionName) {
        const cursorPos = this.input.selectionStart;
        const text = this.input.value;
        const newText = text.slice(0, cursorPos) + `${functionName}(` + text.slice(cursorPos);
        
        this.input.value = newText;
        this.input.focus();
        this.input.setSelectionRange(cursorPos + functionName.length + 1, cursorPos + functionName.length + 1);
    }

    insertText(text) {
        const cursorPos = this.input.selectionStart;
        const inputText = this.input.value;
        const newText = inputText.slice(0, cursorPos) + text + inputText.slice(cursorPos);
        
        this.input.value = newText;
        this.input.focus();
        this.input.setSelectionRange(cursorPos + text.length, cursorPos + text.length);
    }

    clearInput() {
        this.input.value = '';
        this.result.textContent = 'Résultat apparaîtra ici';
        this.result.className = 'result-display';
        this.input.focus();
    }

    backspace() {
        const cursorPos = this.input.selectionStart;
        if (cursorPos > 0) {
            const text = this.input.value;
            this.input.value = text.slice(0, cursorPos - 1) + text.slice(cursorPos);
            this.input.focus();
            this.input.setSelectionRange(cursorPos - 1, cursorPos - 1);
        }
    }

    getVariables() {
        // Pour l'instant, on retourne un objet vide
        // Peut être étendu pour permettre à l'utilisateur de définir des variables
        return {};
    }

    addToHistory(expression, result) {
        this.history.unshift({
            expression: expression,
            result: result,
            timestamp: new Date().toISOString(),
            angleMode: this.angleMode
        });
        
        // Limiter l'historique à 50 éléments
        if (this.history.length > 50) {
            this.history = this.history.slice(0, 50);
        }
        
        AppUtils.saveToLocalStorage('scientific_history', this.history);
    }

    updateHistoryDisplay() {
        if (!this.historyContainer) return;
        
        if (this.history.length === 0) {
            this.historyContainer.innerHTML = '<p class="text-muted">Aucun calcul dans l\'historique</p>';
            return;
        }
        
        const historyHTML = this.history.slice(0, 10).map(item => `
            <div class="history-item" onclick="scientificCalculator.useHistoryItem('${item.expression.replace(/'/g, "\\'")}')">
                <div class="history-expression text-monospace">${this.escapeHtml(item.expression)}</div>
                <div class="history-result">${item.result}</div>
                <div class="history-timestamp">
                    ${AppUtils.formatTimestamp(item.timestamp)} (${item.angleMode})
                </div>
            </div>
        `).join('');
        
        this.historyContainer.innerHTML = historyHTML;
    }

    useHistoryItem(expression) {
        this.input.value = expression;
        this.input.focus();
        AppUtils.showAlert('Expression chargée', 'success', 1500);
    }

    clearHistory() {
        this.history = [];
        AppUtils.saveToLocalStorage('scientific_history', this.history);
        this.updateHistoryDisplay();
        AppUtils.showAlert('Historique effacé', 'success', 2000);
    }

    loadHistory() {
        this.history = AppUtils.loadFromLocalStorage('scientific_history', []);
        this.updateHistoryDisplay();
    }

    escapeHtml(text) {
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return text.replace(/[&<>"']/g, function(m) { return map[m]; });
    }

    // Fonctions spéciales pour les boutons de fonction
    async executeSpecialFunction(functionName, value) {
        try {
            const response = await AppUtils.apiCall('/api/scientific/function', {
                method: 'POST',
                body: JSON.stringify({
                    function: functionName,
                    value: value
                })
            });

            if (response.success) {
                return AppUtils.formatNumber(response.result);
            }
        } catch (error) {
            throw new Error(`Erreur dans ${functionName}: ${error.message}`);
        }
    }
}

// ==================== EXEMPLES ET AIDE ====================

class ScientificExamples {
    static getExamples() {
        return [
            {
                category: 'Trigonométrie',
                examples: [
                    { expression: 'sin(30)', description: 'Sinus de 30 degrés' },
                    { expression: 'cos(pi/4)', description: 'Cosinus de π/4 radians' },
                    { expression: 'tan(45)', description: 'Tangente de 45 degrés' }
                ]
            },
            {
                category: 'Logarithmes',
                examples: [
                    { expression: 'log(100)', description: 'Logarithme base 10 de 100' },
                    { expression: 'ln(e)', description: 'Logarithme naturel de e' },
                    { expression: 'exp(1)', description: 'Exponentielle de 1' }
                ]
            },
            {
                category: 'Puissances et racines',
                examples: [
                    { expression: 'sqrt(16)', description: 'Racine carrée de 16' },
                    { expression: '2**8', description: '2 puissance 8' },
                    { expression: '3^4', description: '3 puissance 4' }
                ]
            }
        ];
    }

    static showHelp() {
        const examples = this.getExamples();
        let helpText = 'Exemples d\'expressions:\n\n';
        
        examples.forEach(category => {
            helpText += `${category.category}:\n`;
            category.examples.forEach(example => {
                helpText += `  ${example.expression} - ${example.description}\n`;
            });
            helpText += '\n';
        });
        
        helpText += 'Constantes disponibles: pi, e\n';
        helpText += 'Fonctions: sin, cos, tan, asin, acos, atan, log, ln, exp, sqrt, abs\n';
        helpText += 'Opérateurs: +, -, *, /, ^, **, %, (, )';
        
        AppUtils.showAlert(helpText, 'info', 10000);
    }
}

// ==================== INITIALISATION ====================

document.addEventListener('DOMContentLoaded', function() {
    // Vérifier si nous sommes sur la page scientifique
    if (document.getElementById('scientific-input')) {
        window.scientificCalculator = new ScientificCalculator();
        window.scientificCalculator.loadHistory();
        
        // Ajouter un bouton d'aide
        const helpButton = document.createElement('button');
        helpButton.className = 'btn btn-outline-info btn-sm float-end';
        helpButton.innerHTML = '<i class="fas fa-question-circle"></i> Aide';
        helpButton.onclick = () => ScientificExamples.showHelp();
        
        const cardHeader = document.querySelector('.card-header h3');
        if (cardHeader && cardHeader.parentNode) {
            cardHeader.parentNode.style.display = 'flex';
            cardHeader.parentNode.style.justifyContent = 'space-between';
            cardHeader.parentNode.style.alignItems = 'center';
            cardHeader.parentNode.appendChild(helpButton);
        }
        
        console.log('Page calculatrice scientifique chargée');
    }
});

// ==================== FONCTIONS D'EXPORT ====================

function exportScientificHistory() {
    if (!window.scientificCalculator) return;
    
    const data = {
        type: 'SmartCalc Scientific History',
        exported: new Date().toISOString(),
        history: window.scientificCalculator.history,
        settings: {
            angleMode: window.scientificCalculator.angleMode
        }
    };
    
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = `smartcalc-scientific-${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    
    URL.revokeObjectURL(url);
    AppUtils.showAlert('Historique scientifique exporté', 'success', 2000);
}