// Code-Switching Benchmark - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    initializeTooltips();

    // Add smooth scrolling to anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add fade-in animation to cards on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
            }
        });
    }, observerOptions);

    // Observe all cards
    document.querySelectorAll('.card, .feature-card, .stat-card, .variety-card, .step-card').forEach(card => {
        observer.observe(card);
    });

    // Add loading states to buttons
    document.querySelectorAll('button[type="submit"]').forEach(button => {
        button.addEventListener('click', function() {
            const originalText = this.innerHTML;
            this.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Loading...';
            this.disabled = true;
            
            // Re-enable after 3 seconds (fallback)
            setTimeout(() => {
                this.innerHTML = originalText;
                this.disabled = false;
            }, 3000);
        });
    });

    // Add copy functionality to code snippets
    document.querySelectorAll('code').forEach(code => {
        code.addEventListener('click', function() {
            navigator.clipboard.writeText(this.textContent).then(() => {
                // Show temporary success message
                const originalText = this.textContent;
                this.textContent = 'Copied!';
                this.style.color = '#10b981';
                
                setTimeout(() => {
                    this.textContent = originalText;
                    this.style.color = '';
                }, 1000);
            });
        });
    });

    // Add hover effects to interactive elements
    document.querySelectorAll('.btn, .card, .feature-card').forEach(element => {
        element.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });
        
        element.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Initialize progress bars animation
    animateProgressBars();
});

// Animate progress bars when they come into view
function animateProgressBars() {
    const progressBars = document.querySelectorAll('.progress-bar');
    
    const progressObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const progressBar = entry.target;
                const width = progressBar.getAttribute('aria-valuenow') || 
                             progressBar.style.width || '0%';
                
                progressBar.style.width = '0%';
                setTimeout(() => {
                    progressBar.style.width = width;
                }, 100);
            }
        });
    }, { threshold: 0.5 });

    progressBars.forEach(bar => {
        progressObserver.observe(bar);
    });
}

// Utility function to show notifications
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// Utility function to format numbers
function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
}

// Utility function to format percentages
function formatPercentage(num) {
    return (num * 100).toFixed(1) + '%';
}

// API utility functions
async function makeAPICall(url, options = {}) {
    try {
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API call failed:', error);
        showNotification('API call failed: ' + error.message, 'danger');
        throw error;
    }
}

// Chart utility functions
function createBarChart(containerId, data, layout = {}) {
    const defaultLayout = {
        template: 'plotly_white',
        margin: { t: 50, r: 50, b: 50, l: 50 },
        ...layout
    };
    
    Plotly.newPlot(containerId, data, defaultLayout, {responsive: true});
}

function createPieChart(containerId, labels, values, colors = null) {
    const data = [{
        labels: labels,
        values: values,
        type: 'pie',
        marker: {
            colors: colors || ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57']
        },
        textinfo: 'label+percent',
        textposition: 'outside'
    }];
    
    const layout = {
        template: 'plotly_white',
        margin: { t: 50, r: 50, b: 50, l: 50 }
    };
    
    Plotly.newPlot(containerId, data, layout, {responsive: true});
}

function createLineChart(containerId, x, y, name, color = '#6366f1') {
    const data = [{
        x: x,
        y: y,
        type: 'scatter',
        mode: 'lines+markers',
        name: name,
        line: { color: color, width: 3 },
        marker: { size: 8 }
    }];
    
    const layout = {
        template: 'plotly_white',
        margin: { t: 50, r: 50, b: 50, l: 50 }
    };
    
    Plotly.newPlot(containerId, data, layout, {responsive: true});
}

// Form validation utilities
function validateAPIKey(key, type) {
    if (!key || key.trim() === '') {
        return { valid: false, message: `${type} API key is required` };
    }
    
    // Basic validation patterns
    const patterns = {
        gemini: /^[A-Za-z0-9_-]{39}$/,
        mistral: /^[A-Za-z0-9]{32}$/,
        cohere: /^[A-Za-z0-9]{40}$/
    };
    
    if (patterns[type] && !patterns[type].test(key)) {
        return { valid: false, message: `Invalid ${type} API key format` };
    }
    
    return { valid: true, message: 'Valid API key' };
}

// Loading state management
function setLoadingState(element, loading = true) {
    if (loading) {
        element.disabled = true;
        element.dataset.originalText = element.innerHTML;
        element.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Loading...';
    } else {
        element.disabled = false;
        element.innerHTML = element.dataset.originalText || 'Submit';
    }
}

// Error handling
function handleError(error, context = '') {
    console.error(`Error in ${context}:`, error);
    
    let message = 'An unexpected error occurred';
    if (error.message) {
        message = error.message;
    } else if (typeof error === 'string') {
        message = error;
    }
    
    showNotification(message, 'danger');
}

// Success handling
function handleSuccess(message) {
    showNotification(message, 'success');
}

// Initialize tooltips function
function initializeTooltips() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Re-initialize tooltips for dynamically added content
function reinitializeTooltips() {
    // Destroy existing tooltips first
    var existingTooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    existingTooltips.forEach(function(element) {
        var tooltip = bootstrap.Tooltip.getInstance(element);
        if (tooltip) {
            tooltip.dispose();
        }
    });
    
    // Initialize new tooltips
    initializeTooltips();
}

// Export functions for use in other scripts
window.CodeSwitchingUtils = {
    showNotification,
    formatNumber,
    formatPercentage,
    makeAPICall,
    createBarChart,
    createPieChart,
    createLineChart,
    validateAPIKey,
    setLoadingState,
    handleError,
    handleSuccess,
    initializeTooltips,
    reinitializeTooltips
};
