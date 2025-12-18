from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Root endpoint that renders a simple form with Auth0 login/registration"""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>GoatBot Form</title>
    </head>
    <body>
        <div class="container">
            <div class="auth-section">
                <div id="authInfo" class="auth-info">
                    <!-- Auth info will be populated by JavaScript -->
                </div>
            </div>

            <h1>GoatBot Form</h1>

            <form id="dataForm">
                <label for="domain">Domain:</label>
                <input type="text" id="domain" name="domain" required>

                <label for="title">Title:</label>
                <input type="text" id="title" name="title" required>

                <label for="system_prompt">System Prompt:</label>
                <textarea id="system_prompt" name="system_prompt" required></textarea>

                <label for="password">Password:</label>
                <input type="password" id="password" name="password">

                <label for="password_confirm">Confirm Password:</label>
                <input type="password" id="password_confirm" name="password_confirm">

                <div id="passwordError" style="color: red; display: none; margin-bottom: 10px;"></div>

                <button type="submit" class="btn-primary">Submit</button>
            </form>
            <div id="response"></div>
        </div>

        <script>
            // Check authentication status on page load
            async function checkAuth() {
                try {
                    const response = await fetch('/api/auth/me');
                    if (response.ok) {
                        const user = await response.json();
                        displayAuthenticatedUser(user);
                    } else {
                        displayLoginPrompt();
                    }
                } catch (error) {
                    displayLoginPrompt();
                }
            }

            function displayAuthenticatedUser(user) {
                const authInfo = document.getElementById('authInfo');
                const initials = (user.name || user.email || 'U').substring(0, 2).toUpperCase();

                authInfo.innerHTML = `
                    <div class="user-info">
                        <div class="user-avatar">${initials}</div>
                        <div class="user-details">
                            <div class="user-name">${user.name || user.nickname || user.email || 'User'}</div>
                            <div class="user-email">${user.email || ''}</div>
                        </div>
                    </div>
                    <div class="auth-buttons">
                        <button class="btn-logout" onclick="logout()">Logout</button>
                    </div>
                `;
            }

            function displayLoginPrompt() {
                const authInfo = document.getElementById('authInfo');
                authInfo.innerHTML = `
                    <div class="login-prompt" style="width: 100%;">
                        <p>Please login or register to continue</p>
                        <button class="btn-primary" onclick="login()">Login / Register</button>
                    </div>
                `;
            }

            function login() {
                window.location.href = '/api/auth/login';
            }

            function logout() {
                window.location.href = '/api/auth/logout';
            }

            // Check auth status on page load
            checkAuth();

            // Form submission handler
            document.getElementById('dataForm').addEventListener('submit', async function(e) {
                e.preventDefault();

                const password = document.getElementById('password').value;
                const passwordConfirm = document.getElementById('password_confirm').value;
                const passwordError = document.getElementById('passwordError');

                // Check if passwords match (only if password is provided)
                if (password && password !== passwordConfirm) {
                    passwordError.textContent = 'Passwords do not match!';
                    passwordError.style.display = 'block';
                    return;
                }

                // Clear error if passwords match
                passwordError.style.display = 'none';

                const formData = {
                    domain: document.getElementById('domain').value,
                    title: document.getElementById('title').value,
                    system_prompt: document.getElementById('system_prompt').value,
                    password: password || null
                };

                const responseDiv = document.getElementById('response');
                responseDiv.style.display = 'block';
                responseDiv.textContent = 'Submitting...';
                responseDiv.className = '';

                try {
                    const response = await fetch('/api/chat/start', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(formData)
                    });

                    const data = await response.json();

                    if (response.ok) {
                        // Redirect immediately if redirect_url is present
                        if (data.redirect_url) {
                            window.location.href = data.redirect_url;
                            return; // Exit early to prevent further execution
                        }
                        // Fallback: show success message if no redirect_url
                        responseDiv.className = 'success';
                        responseDiv.textContent = 'Success! ' + (data.message || 'Chat created');
                        document.getElementById('dataForm').reset();
                    } else {
                        responseDiv.className = 'error';
                        responseDiv.textContent = 'Error: ' + (data.detail || 'Failed to submit data');
                    }
                } catch (error) {
                    responseDiv.className = 'error';
                    responseDiv.textContent = 'Error: ' + error.message;
                }
            });
        </script>
    </body>
    </html>
    """
    return html_content
