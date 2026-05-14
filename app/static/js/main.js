// Main JavaScript utilities for POS System

// Toast notification
function showToast(message, type = 'success') {
    const alertClass = `alert-${type === 'error' ? 'danger' : type}`;
    const alertHtml = `
        <div class="alert ${alertClass} alert-dismissible fade show position-fixed top-0 end-0 m-3" role="alert" style="z-index: 9999;">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    const div = document.createElement('div');
    div.innerHTML = alertHtml;
    document.body.appendChild(div.firstElementChild);
    
    setTimeout(() => {
        document.querySelectorAll('.alert-dismissible').forEach(el => el.remove());
    }, 4000);
}

// Format currency - Ghana Cedis
function formatCurrency(amount) {
    try {
        const numAmount = parseFloat(amount) || 0;
        return new Intl.NumberFormat('en-GH', {
            style: 'currency',
            currency: 'GHS',
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        }).format(numAmount);
    } catch (error) {
        return 'GHS 0.00';
    }
}

// Clean and parse price from various formats
// Converts "GHC120", "₵120", "120 GHC", "GHS 120.00", etc. to number
function cleanPrice(price) {
    if (typeof price === 'number') {
        return isNaN(price) ? 0 : price;
    }
    
    if (!price) return 0;
    
    // Convert to string and remove currency symbols and text
    let cleaned = String(price)
        .replace(/,/g, '')             // Remove thousands separators
        .replace(/[^\d.-]/g, '')       // Keep only numeric characters, decimal point, and minus sign
        .trim();
    
    const num = parseFloat(cleaned) || 0;
    return isNaN(num) ? 0 : num;
}

// Parse currency (legacy support)
function parseCurrency(value) {
    return cleanPrice(value);
}

// Format date
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-US', options);
}

// Format time
function formatTime(dateString) {
    const options = { hour: '2-digit', minute: '2-digit', second: '2-digit' };
    return new Date(dateString).toLocaleTimeString('en-US', options);
}

// Debounce function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Throttle function
function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Initialize tooltips
function initializeTooltips() {
    document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(el => {
        new bootstrap.Tooltip(el);
    });
}

// Initialize popovers
function initializePopovers() {
    document.querySelectorAll('[data-bs-toggle="popover"]').forEach(el => {
        new bootstrap.Popover(el);
    });
}

// API call helper
async function apiCall(method, url, data = null) {
    try {
        const options = {
            method: method.toUpperCase(),
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            }
        };
        
        if (data) {
            options.body = JSON.stringify(data);
        }
        
        const response = await fetch(url, options);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Form validation
function validateForm(formElement) {
    let isValid = true;
    
    formElement.querySelectorAll('[required]').forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

// Clear form
function clearForm(formElement) {
    formElement.reset();
    formElement.querySelectorAll('.is-invalid').forEach(el => {
        el.classList.remove('is-invalid');
    });
}

// Initialize document
document.addEventListener('DOMContentLoaded', function() {
    initializeTooltips();
    initializePopovers();
    
    // Remove alerts after 4 seconds
    document.querySelectorAll('.alert').forEach(alert => {
        if (!alert.classList.contains('position-fixed')) {
            setTimeout(() => {
                alert.remove();
            }, 4000);
        }
    });
});
