// ==================== UTILITAIRES GLOBAUX ====================

class AppUtils {
    static showAlert(message, type = 'error', duration = 5000) {
        const alertContainer = document.getElementById('alert-container');
        if (!alertContainer) return;

        const alertId = 'alert-' + Date.now();
        const alertClass = type === 'error' ? 'alert-error' : 'alert-success';
        
        const alertHTML = `
            <div id="${alertId}" class="alert ${alertClass} fade-in" role="alert">
                <div class="d-flex justify-content-between align-items-center">
                    <span>${message}</span>
                    <button type="button" class="btn-close" onclick="AppUtils.closeAlert('${alertId}')"></button>
                </div>
            </div>
        `;
        
        alertContainer.insertAdjacentHTML('beforeend', alertHTML);
        
        // Auto-fermeture
        setTimeout(() => {
            AppUtils.closeAlert(alertId);
        }, duration);
    }

    static closeAlert(alertId) {
        const alert = document.getElementById(alertId);
        if (alert) {
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.remove();
            }, 300);
        }
    }

    static async apiCall(url, options = {}) {
        try {
            const defaultOptions = {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            };

            const response = await fetch(url, { ...defaultOptions, ...options });
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Erreur réseau');
            }

            return data;
        } catch (error) {
            console.error('Erreur API:', error);
            AppUtils.showAlert(error.message || 'Erreur de communication avec le serveur');
            throw error;
        }
    }

    static formatNumber(num, precision = 10) {
        if (typeof num !== 'number') return num;
        
        // Éviter la notation scientifique pour les petits nombres
        if (Math.abs(num) < 1e-10 && num !== 0) {
            return num.toExponential(precision);
        }
        
        // Pour les grands nombres
        if (Math.abs(num) > 1e10) {
            return num.toExponential(precision);
        }
        
        // Pour les nombres normaux, supprimer les zéros inutiles
        const fixed = parseFloat(num.toFixed(precision));
        return fixed.toString();
    }

    static addButtonAnimation(button) {
        button.classList.add('pulse');
        setTimeout(() => {
            button.classList.remove('pulse');
        }, 300);
    }

    static formatTimestamp(timestamp) {
        const date = new Date(timestamp);
        return date.toLocaleString('fr-FR', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });
    }

    static copyToClipboard(text) {
        if (navigator.clipboard) {
            navigator.clipboard.writeText(text).then(() => {
                AppUtils.showAlert('Copié dans le presse-papier', 'success', 2000);
            });
        } else {
            // Fallback pour les navigateurs plus anciens
            const textArea = document.createElement('textarea');
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            AppUtils.showAlert('Copié dans le presse-papier', 'success', 2000);
        }
    }

    static debounce(func, wait, immediate) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                timeout = null;
                if (!immediate) func(...args);
            };
            const callNow = immediate && !timeout;
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
            if (callNow) func(...args);
        };
    }

    static validateNumberInput(input) {
        const value = parseFloat(input);
        return !isNaN(value) && isFinite(value);
    }

    static saveToLocalStorage(key, data) {
        try {
            localStorage.setItem(key, JSON.stringify(data));
        } catch (error) {
            console.warn('Impossible de sauvegarder dans localStorage:', error);
        }
    }

    static loadFromLocalStorage(key, defaultValue = null) {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : defaultValue;
        } catch (error) {
            console.warn('Impossible de charger depuis localStorage:', error);
            return defaultValue;
        }
    }
}

// ==================== HISTORIQUE GLOBAL ====================

class HistoryManager {
    constructor(type, maxItems = 50) {
        this.type = type;
        this.maxItems = maxItems;
        this.storageKey = `smartcalc_history_${type}`;
        this.history = AppUtils.loadFromLocalStorage(this.storageKey, []);
    }

    addItem(item) {
        item.timestamp = new Date().toISOString();
        item.id = Date.now();
        
        this.history.unshift(item);
        
        // Limiter le nombre d'éléments
        if (this.history.length > this.maxItems) {
            this.history = this.history.slice(0, this.maxItems);
        }
        
        this.saveHistory();
        this.renderHistory();
    }

    clear() {
        this.history = [];
        this.saveHistory();
        this.renderHistory();
    }

    saveHistory() {
        AppUtils.saveToLocalStorage(this.storageKey, this.history);
    }

    renderHistory() {
        // Cette méthode sera surchargée par les classes enfants
    }

    getHistory() {
        return this.history;
    }

    removeItem(id) {
        this.history = this.history.filter(item => item.id !== id);
        this.saveHistory();
        this.renderHistory();
    }
}

// ==================== GESTIONNAIRE DE RACCOURCIS CLAVIER ====================

class KeyboardManager {
    constructor() {
        this.shortcuts = new Map();
        this.setupGlobalShortcuts();
    }

    setupGlobalShortcuts() {
        document.addEventListener('keydown', (event) => {
            const key = this.getKeyString(event);
            const callback = this.shortcuts.get(key);
            
            if (callback) {
                event.preventDefault();
                callback(event);
            }
        });
    }

    getKeyString(event) {
        let key = event.key.toLowerCase();
        if (event.ctrlKey) key = 'ctrl+' + key;
        if (event.altKey) key = 'alt+' + key;
        if (event.shiftKey) key = 'shift+' + key;
        return key;
    }

    addShortcut(keyString, callback) {
        this.shortcuts.set(keyString.toLowerCase(), callback);
    }

    removeShortcut(keyString) {
        this.shortcuts.delete(keyString.toLowerCase());
    }
}

// ==================== GESTIONNAIRE DE THÈME ====================

class ThemeManager {
    constructor() {
        this.currentTheme = AppUtils.loadFromLocalStorage('smartcalc_theme', 'dark');
        this.applyTheme();
    }

    applyTheme() {
        document.body.setAttribute('data-theme', this.currentTheme);
        AppUtils.saveToLocalStorage('smartcalc_theme', this.currentTheme);
    }

    toggleTheme() {
        this.currentTheme = this.currentTheme === 'dark' ? 'light' : 'dark';
        this.applyTheme();
    }

    setTheme(theme) {
        this.currentTheme = theme;
        this.applyTheme();
    }
}

// ==================== INITIALISATION GLOBALE ====================

document.addEventListener('DOMContentLoaded', function() {
    // Initialiser les gestionnaires globaux
    window.appUtils = AppUtils;
    window.keyboardManager = new KeyboardManager();
    window.themeManager = new ThemeManager();

    // Ajouter des raccourcis globaux
    keyboardManager.addShortcut('ctrl+/', () => {
        AppUtils.showAlert('Raccourcis disponibles: Ctrl+C (copier), Ctrl+Z (annuler), F1 (aide)', 'info', 3000);
    });

    // Gestionnaire d'erreurs global
    window.addEventListener('error', function(event) {
        console.error('Erreur JavaScript:', event.error);
        AppUtils.showAlert('Une erreur inattendue s\'est produite. Consultez la console pour plus de détails.');
    });

    // Gestionnaire pour les promesses rejetées
    window.addEventListener('unhandledrejection', function(event) {
        console.error('Promise rejetée:', event.reason);
        AppUtils.showAlert('Erreur de traitement. Veuillez réessayer.');
    });

    // Améliorer l'accessibilité
    setupAccessibility();
});

// ==================== ACCESSIBILITÉ ====================

function setupAccessibility() {
    // Ajouter la navigation au clavier pour les boutons personnalisés
    document.querySelectorAll('.calc-btn, .func-btn, .insert-btn').forEach(button => {
        button.setAttribute('tabindex', '0');
        
        button.addEventListener('keydown', function(event) {
            if (event.key === 'Enter' || event.key === ' ') {
                event.preventDefault();
                button.click();
            }
        });
    });

    // Améliorer les labels pour les lecteurs d'écran
    document.querySelectorAll('input[type="number"], input[type="text"], textarea').forEach(input => {
        if (!input.getAttribute('aria-label') && !input.getAttribute('aria-labelledby')) {
            const label = input.closest('.form-group, .mb-3')?.querySelector('label');
            if (label) {
                input.setAttribute('aria-labelledby', label.id || 'label-' + Date.now());
            }
        }
    });
}

// ==================== GESTIONNAIRE DE PERFORMANCE ====================

class PerformanceManager {
    constructor() {
        this.measurements = new Map();
    }

    startMeasurement(name) {
        this.measurements.set(name, performance.now());
    }

    endMeasurement(name) {
        const startTime = this.measurements.get(name);
        if (startTime) {
            const duration = performance.now() - startTime;
            console.log(`${name} took ${duration.toFixed(2)}ms`);
            this.measurements.delete(name);
            return duration;
        }
        return null;
    }

    measureFunction(fn, name) {
        return (...args) => {
            this.startMeasurement(name);
            const result = fn.apply(this, args);
            this.endMeasurement(name);
            return result;
        };
    }
}

// Exporter pour utilisation globale
window.performanceManager = new PerformanceManager();