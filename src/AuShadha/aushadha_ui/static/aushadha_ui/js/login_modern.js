/**
 * AuShadha 2.0 - Modern Login with HTMX + Alpine.js
 *
 * This replaces the old Dojo-based login system
 */

// Alpine.js data for login form
document.addEventListener('alpine:init', () => {
    Alpine.data('loginForm', () => ({
        username: '',
        password: '',
        errors: {},
        loading: false,
        errorMessage: '',

        validateForm() {
            this.errors = {};

            if (!this.username) {
                this.errors.username = 'Username is required';
            }

            if (!this.password) {
                this.errors.password = 'Password is required';
            }

            return Object.keys(this.errors).length === 0;
        },

        async handleLogin(event) {
            event.preventDefault();

            if (!this.validateForm()) {
                return;
            }

            this.loading = true;
            this.errorMessage = '';

            const formData = new FormData(event.target);

            try {
                const response = await fetch('/AuShadha/authenticate/login/', {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });

                const data = await response.json();

                if (data.success) {
                    window.location.href = data.redirect_to || '/AuShadha/patients/';
                } else {
                    this.errorMessage = data.error_message || 'Login failed. Please try again.';
                }
            } catch (error) {
                console.error('Login error:', error);
                this.errorMessage = 'An error occurred. Please try again.';
            } finally {
                this.loading = false;
            }
        }
    }));
});

// HTMX configuration
document.addEventListener('DOMContentLoaded', () => {
    // Configure HTMX defaults
    if (typeof htmx !== 'undefined') {
        // Add CSRF token to all HTMX requests
        document.body.addEventListener('htmx:configRequest', (event) => {
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
            if (csrfToken) {
                event.detail.headers['X-CSRFToken'] = csrfToken;
            }
        });

        // Handle errors
        document.body.addEventListener('htmx:responseError', (event) => {
            console.error('HTMX error:', event.detail);
        });
    }
});
