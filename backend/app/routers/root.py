from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint that renders a simple form"""
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

                <button type="submit">Submit</button>
            </form>
            <div id="response"></div>
        </div>

        <script>
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
