// Mobile App State
const state = {
    currentPage: 'moderate',
    darkMode: false,
    logsOffset: 0,
    userId: 'mobile_user_' + Date.now(),
    isProcessing: false
};

// Initialize the app
document.addEventListener('DOMContentLoaded', function() {
    checkAPIStatus();
    setupInputListeners();
    loadLogs();
    loadSettings();
    registerServiceWorker();
});

// Page Navigation
function showPage(page) {
    // Hide all pages
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
    
    // Show selected page
    const pageElement = document.getElementById(page + '-page');
    if (pageElement) {
        pageElement.classList.add('active');
    }
    
    const navBtn = document.querySelector(`.nav-btn[data-page="${page}"]`);
    if (navBtn) {
        navBtn.classList.add('active');
    }
    
    state.currentPage = page;
    
    // Load data if needed
    if (page === 'logs') {
        loadLogs();
    }
}

// Moderation Functions
async function moderateComment() {
    if (state.isProcessing) return;
    
    const textarea = document.getElementById('commentInput');
    const comment = textarea.value.trim();
    
    if (!comment) {
        showToast('Please enter a comment to moderate');
        textarea.focus();
        return;
    }
    
    // Start loading
    state.isProcessing = true;
    const btn = document.querySelector('#moderate-page .btn-primary');
    const btnText = document.getElementById('moderateBtnText');
    const spinner = document.getElementById('moderateSpinner');
    
    btnText.textContent = 'Analyzing...';
    spinner.style.display = 'inline-block';
    btn.disabled = true;
    
    try {
        const response = await fetch('/api/moderate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Device-Type': 'mobile'
            },
            body: JSON.stringify({
                comment: comment,
                user_id: state.userId,
                device_type: 'mobile'
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayModerationResult(data);
        } else {
            showToast(data.error || 'Moderation failed');
        }
    } catch (error) {
        showToast('Network error. Please check your connection.');
        console.error('Moderation error:', error);
    } finally {
        state.isProcessing = false;
        btnText.textContent = 'Analyze Comment';
        spinner.style.display = 'none';
        btn.disabled = false;
    }
}

function displayModerationResult(data) {
    const resultCard = document.getElementById('resultCard');
    const decision = document.getElementById('resultDecision');
    const confidence = document.getElementById('resultConfidence');
    const reasoning = document.getElementById('resultReasoning');
    const appealBtn = document.getElementById('appealBtn');
    
    resultCard.style.display = 'block';
    resultCard.className = 'card result-card ' + data.decision;
    
    decision.textContent = data.decision.toUpperCase();
    decision.className = 'result-decision ' + data.decision;
    
    confidence.textContent = Math.round(data.confidence * 100) + '%';
    reasoning.textContent = data.reasoning;
    
    // Show appeal button if eligible
    if (data.appeal_eligible) {
        appealBtn.style.display = 'inline-block';
        // Store comment for appeal
        appealBtn.dataset.comment = document.getElementById('commentInput').value;
    } else {
        appealBtn.style.display = 'none';
    }
    
    // Refresh logs
    loadLogs();
}

function resetModeration() {
    document.getElementById('commentInput').value = '';
    document.getElementById('resultCard').style.display = 'none';
    document.getElementById('commentInput').focus();
}

// Appeal Functions
function showAppealFromResult() {
    const comment = document.getElementById('appealBtn').dataset.comment;
    if (comment) {
        document.getElementById('appealComment').value = comment;
        showPage('appeal');
        document.getElementById('appealContext').focus();
    }
}

async function submitAppeal() {
    if (state.isProcessing) return;
    
    const comment = document.getElementById('appealComment').value.trim();
    const context = document.getElementById('appealContext').value.trim();
    
    if (!comment) {
        showToast('Please enter the original comment');
        document.getElementById('appealComment').focus();
        return;
    }
    
    if (!context) {
        showToast('Please provide appeal context');
        document.getElementById('appealContext').focus();
        return;
    }
    
    // Start loading
    state.isProcessing = true;
    const btn = document.querySelector('#appeal-page .btn-primary');
    const btnText = document.getElementById('appealBtnText');
    const spinner = document.getElementById('appealSpinner');
    
    btnText.textContent = 'Processing Appeal...';
    spinner.style.display = 'inline-block';
    btn.disabled = true;
    
    try {
        const response = await fetch('/api/appeal', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Device-Type': 'mobile'
            },
            body: JSON.stringify({
                comment: comment,
                appeal_context: context,
                user_id: state.userId
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayAppealResult(data);
        } else {
            showToast(data.error || 'Appeal failed');
        }
    } catch (error) {
        showToast('Network error. Please check your connection.');
        console.error('Appeal error:', error);
    } finally {
        state.isProcessing = false;
        btnText.textContent = 'Submit Appeal';
        spinner.style.display = 'none';
        btn.disabled = false;
    }
}

function displayAppealResult(data) {
    const resultCard = document.getElementById('appealResultCard');
    const decision = document.getElementById('appealDecision');
    const confidence = document.getElementById('appealConfidence');
    const reasoning = document.getElementById('appealReasoning');
    
    resultCard.style.display = 'block';
    resultCard.className = 'card result-card ' + data.decision;
    
    decision.textContent = data.decision.toUpperCase();
    decision.className = 'result-decision ' + data.decision;
    
    confidence.textContent = Math.round(data.confidence * 100) + '%';
    reasoning.textContent = data.reasoning;
    
    // Refresh logs
    loadLogs();
}

function resetAppeal() {
    document.getElementById('appealComment').value = '';
    document.getElementById('appealContext').value = '';
    document.getElementById('appealResultCard').style.display = 'none';
    document.getElementById('appealComment').focus();
}

// Logs Functions
async function loadLogs() {
    try {
        const response = await fetch('/api/log?limit=20');
        const data = await response.json();
        
        if (data.success) {
            displayLogs(data.logs);
        }
    } catch (error) {
        console.error('Error loading logs:', error);
    }
}

function displayLogs(logs) {
    const logList = document.getElementById('logList');
    
    if (!logs || logs.length === 0) {
        logList.innerHTML = '<div class="log-empty">No moderation logs available</div>';
        return;
    }
    
    let html = '';
    logs.forEach(log => {
        const decisionClass = log.decision;
        const confidencePercent = Math.round(log.confidence * 100);
        
        html += `
            <div class="log-item">
                <div class="log-info">
                    <div class="log-comment">${escapeHtml(log.comment_preview)}</div>
                    <div class="log-meta">
                        <span>${log.timestamp}</span>
                        <span>•</span>
                        <span class="log-badge ${decisionClass}">${log.decision}</span>
                        <span>•</span>
                        <span>${confidencePercent}%</span>
                    </div>
                </div>
            </div>
        `;
    });
    
    logList.innerHTML = html;
}

function refreshLogs() {
    loadLogs();
    showToast('Logs refreshed');
}

function loadMoreLogs() {
    state.logsOffset += 20;
    loadLogs();
}

// Settings Functions
async function loadSettings() {
    try {
        const response = await fetch('/api/health');
        const data = await response.json();
        
        if (data.status === 'healthy') {
            document.getElementById('apiStatusBadge').textContent = 'Online';
            document.getElementById('apiStatusBadge').className = 'status-badge online';
            document.getElementById('modelDisplay').textContent = data.model || 'GPT-4';
            document.getElementById('maxLengthDisplay').textContent = data.max_comment_length || 5000;
        } else {
            document.getElementById('apiStatusBadge').textContent = 'Offline';
            document.getElementById('apiStatusBadge').className = 'status-badge offline';
        }
    } catch (error) {
        document.getElementById('apiStatusBadge').textContent = 'Offline';
        document.getElementById('apiStatusBadge').className = 'status-badge offline';
        console.error('Error loading settings:', error);
    }
}

function toggleDarkMode() {
    const isChecked = document.getElementById('darkModeToggle').checked;
    document.body.classList.toggle('dark-mode', isChecked);
    localStorage.setItem('darkMode', isChecked);
}

function clearCache() {
    if (confirm('Clear local cache?')) {
        localStorage.clear();
        showToast('Cache cleared');
        location.reload();
    }
}

// API Status Check
async function checkAPIStatus() {
    const dot = document.getElementById('statusDot');
    const text = document.getElementById('statusText');
    
    try {
        const response = await fetch('/api/health');
        const data = await response.json();
        
        if (data.status === 'healthy') {
            dot.className = 'status-dot online';
            text.textContent = 'Online';
        } else {
            dot.className = 'status-dot offline';
            text.textContent = 'Offline';
        }
    } catch (error) {
        dot.className = 'status-dot offline';
        text.textContent = 'Offline';
    }
}

// Input Listeners
function setupInputListeners() {
    // Character counter for moderation
    const commentInput = document.getElementById('commentInput');
    commentInput.addEventListener('input', function() {
        const count = this.value.length;
        document.getElementById('charCount').textContent = count;
        if (count > 5000) {
            this.style.borderColor = '#F44336';
        } else {
            this.style.borderColor = '';
        }
    });
    
    // Character counter for appeal
    const appealContext = document.getElementById('appealContext');
    appealContext.addEventListener('input', function() {
        const count = this.value.length;
        document.getElementById('appealCharCount').textContent = count;
        if (count > 5000) {
            this.style.borderColor = '#F44336';
        } else {
            this.style.borderColor = '';
        }
    });
    
    // Enter key support (Shift+Enter for new line)
    document.querySelectorAll('textarea').forEach(textarea => {
        textarea.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                const page = this.closest('.page').id;
                if (page === 'moderate-page') {
                    moderateComment();
                } else if (page === 'appeal-page') {
                    submitAppeal();
                }
            }
        });
    });
}

// Service Worker Registration (for PWA)
function registerServiceWorker() {
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/sw.js')
            .then(() => console.log('Service Worker registered'))
            .catch(err => console.log('Service Worker registration failed:', err));
    }
}

// Toast Notification
function showToast(message) {
    const toast = document.getElementById('toast');
    const toastMessage = document.getElementById('toastMessage');
    
    toastMessage.textContent = message;
    toast.style.display = 'flex';
    
    // Auto hide after 3 seconds
    clearTimeout(toast.timeout);
    toast.timeout = setTimeout(() => {
        hideToast();
    }, 3000);
}

function hideToast() {
    document.getElementById('toast').style.display = 'none';
}

// Utility Functions
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Handle offline/online events
window.addEventListener('online', function() {
    showToast('Back online');
    checkAPIStatus();
});

window.addEventListener('offline', function() {
    showToast('You are offline. Some features may not work.');
});

// Load dark mode preference
if (localStorage.getItem('darkMode') === 'true') {
    document.getElementById('darkModeToggle').checked = true;
    document.body.classList.add('dark-mode');
}

// Service Worker for offline support (optional)
// Create a simple sw.js file in the static directory