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
        <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
        <title>GoatBot Form</title>
        <link href="https://fonts.googleapis.com/css?family=Roboto:100,300,100italic,300italic" rel="stylesheet">
        <style>
            * {
                box-sizing: border-box;
            }

            html {
                scroll-behavior: smooth;
            }

            html, body {
                margin: 0;
                padding: 0;
                background: #1c1d26;
                color: rgba(255, 255, 255, 0.75);
                font-family: "Roboto", Helvetica, sans-serif;
                font-size: 17pt;
                font-weight: 100;
                line-height: 1.75em;
            }

            #page-wrapper {
                min-height: 100vh;
                position: relative;
                overflow-x: hidden;
            }

            /* Subtle background parallax effect */
            #parallax-bg {
                position: fixed;
                top: -20%;
                left: 0;
                width: 100%;
                height: 140%;
                background: radial-gradient(circle at 20% 50%, rgba(228, 76, 101, 0.1) 0%, transparent 50%),
                            radial-gradient(circle at 80% 80%, rgba(228, 76, 101, 0.05) 0%, transparent 50%);
                pointer-events: none;
                z-index: -1;
                will-change: transform;
            }

            /* Header */
            #header {
                background: rgba(28, 29, 38, 0.95);
                box-shadow: 0 0 0.25em 0 rgba(0, 0, 0, 0.15);
                cursor: default;
                height: 3.5em;
                left: 0;
                line-height: 3.5em;
                position: fixed;
                top: 0;
                width: 100%;
                z-index: 10000;
                -moz-transition: background-color 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
                -webkit-transition: background-color 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
                -ms-transition: background-color 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
                transition: background-color 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
            }

            #header.scrolled {
                background: rgba(28, 29, 38, 0.98);
                box-shadow: 0 0 0.5em 0 rgba(0, 0, 0, 0.3);
            }

            #header h1 {
                color: #ffffff;
                font-weight: 300;
                height: inherit;
                left: 1.25em;
                line-height: inherit;
                margin: 0;
                padding: 0;
                position: absolute;
                top: 0;
            }

            #header h1 a {
                border: 0;
                color: inherit;
                text-decoration: none;
            }

            #nav {
                position: absolute;
                right: 1em;
                top: 0;
            }

            #nav ul {
                list-style: none;
                margin: 0;
                padding: 0;
            }

            #nav ul li {
                display: inline-block;
                margin-left: 1.5em;
            }

            #nav ul li a {
                border: 0;
                color: inherit;
                display: inline-block;
                font-size: 0.9em;
                font-weight: 300;
                letter-spacing: 0.25em;
                text-decoration: none;
                text-transform: uppercase;
            }

            #nav ul li a:hover {
                color: #e44c65;
            }

            /* Main Content */
            .wrapper {
                padding: 6em 0 4em 0;
                margin-top: 3.5em;
            }

            /* Scroll Animation Classes */
            .fade-in {
                opacity: 0;
                -moz-transform: translateY(30px);
                -webkit-transform: translateY(30px);
                -ms-transform: translateY(30px);
                transform: translateY(30px);
                -moz-transition: opacity 0.6s ease-out, transform 0.6s ease-out;
                -webkit-transition: opacity 0.6s ease-out, transform 0.6s ease-out;
                -ms-transition: opacity 0.6s ease-out, transform 0.6s ease-out;
                transition: opacity 0.6s ease-out, transform 0.6s ease-out;
            }

            .fade-in.visible {
                opacity: 1;
                -moz-transform: translateY(0);
                -webkit-transform: translateY(0);
                -ms-transform: translateY(0);
                transform: translateY(0);
            }

            .fade-in-left {
                opacity: 0;
                -moz-transform: translateX(-30px);
                -webkit-transform: translateX(-30px);
                -ms-transform: translateX(-30px);
                transform: translateX(-30px);
                -moz-transition: opacity 0.6s ease-out, transform 0.6s ease-out;
                -webkit-transition: opacity 0.6s ease-out, transform 0.6s ease-out;
                -ms-transition: opacity 0.6s ease-out, transform 0.6s ease-out;
                transition: opacity 0.6s ease-out, transform 0.6s ease-out;
            }

            .fade-in-left.visible {
                opacity: 1;
                -moz-transform: translateX(0);
                -webkit-transform: translateX(0);
                -ms-transform: translateX(0);
                transform: translateX(0);
            }

            .fade-in-right {
                opacity: 0;
                -moz-transform: translateX(30px);
                -webkit-transform: translateX(30px);
                -ms-transform: translateX(30px);
                transform: translateX(30px);
                -moz-transition: opacity 0.6s ease-out, transform 0.6s ease-out;
                -webkit-transition: opacity 0.6s ease-out, transform 0.6s ease-out;
                -ms-transition: opacity 0.6s ease-out, transform 0.6s ease-out;
                transition: opacity 0.6s ease-out, transform 0.6s ease-out;
            }

            .fade-in-right.visible {
                opacity: 1;
                -moz-transform: translateX(0);
                -webkit-transform: translateX(0);
                -ms-transform: translateX(0);
                transform: translateX(0);
            }

            .scale-in {
                opacity: 0;
                -moz-transform: scale(0.9);
                -webkit-transform: scale(0.9);
                -ms-transform: scale(0.9);
                transform: scale(0.9);
                -moz-transition: opacity 0.6s ease-out, transform 0.6s ease-out;
                -webkit-transition: opacity 0.6s ease-out, transform 0.6s ease-out;
                -ms-transition: opacity 0.6s ease-out, transform 0.6s ease-out;
                transition: opacity 0.6s ease-out, transform 0.6s ease-out;
            }

            .scale-in.visible {
                opacity: 1;
                -moz-transform: scale(1);
                -webkit-transform: scale(1);
                -ms-transform: scale(1);
                transform: scale(1);
            }

            .container {
                margin: 0 auto;
                max-width: 1000px;
                width: calc(100% - 4em);
            }

            /* Auth Section */
            .auth-section {
                margin-bottom: 3em;
                padding-top: 1em;
            }

            .auth-info {
                display: flex;
                justify-content: space-between;
                align-items: center;
                flex-wrap: wrap;
                gap: 1em;
            }

            .user-info {
                display: flex;
                align-items: center;
                gap: 1em;
            }

            .user-avatar {
                width: 3em;
                height: 3em;
                border-radius: 50%;
                background: #e44c65;
                color: #ffffff;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: 300;
                font-size: 1em;
            }

            .user-details {
                display: flex;
                flex-direction: column;
            }

            .user-name {
                color: #ffffff;
                font-weight: 300;
            }

            .user-email {
                color: rgba(255, 255, 255, 0.5);
                font-size: 1em;
            }

            .login-prompt {
                text-align: center;
            }

            .login-prompt p {
                margin-bottom: 1em;
            }

            /* Form */
            form {
                margin: 0 0 2em 0;
            }

            .form-field {
                margin-bottom: 2em;
                -moz-transition-delay: 0s;
                -webkit-transition-delay: 0s;
                -ms-transition-delay: 0s;
                transition-delay: 0s;
            }

            .form-field:nth-child(1) { transition-delay: 0.1s; }
            .form-field:nth-child(2) { transition-delay: 0.2s; }
            .form-field:nth-child(3) { transition-delay: 0.3s; }
            .form-field:nth-child(4) { transition-delay: 0.4s; }
            .form-field:nth-child(5) { transition-delay: 0.5s; }
            .form-field:nth-child(6) { transition-delay: 0.6s; }
            .form-field:nth-child(7) { transition-delay: 0.7s; }
            .form-field:nth-child(8) { transition-delay: 0.8s; }

            label {
                color: #ffffff;
                display: block;
                font-size: 1em;
                font-weight: 300;
                margin: 0 0 1em 0;
            }

            .field-description {
                color: rgba(255, 255, 255, 0.5);
                font-size: 0.85em;
                font-weight: 100;
                margin: -0.75em 0 0.75em 0;
                font-style: italic;
                line-height: 1.5em;
            }

            input[type="text"],
            input[type="password"],
            input[type="email"],
            textarea {
                -moz-appearance: none;
                -webkit-appearance: none;
                -ms-appearance: none;
                appearance: none;
                -moz-transition: border-color 0.2s ease-in-out;
                -webkit-transition: border-color 0.2s ease-in-out;
                -ms-transition: border-color 0.2s ease-in-out;
                transition: border-color 0.2s ease-in-out;
                background: transparent;
                border-radius: 4px;
                border: solid 1px rgba(255, 255, 255, 0.3);
                color: inherit;
                display: block;
                outline: 0;
                padding: 0 1em;
                text-decoration: none;
                width: 100%;
            }

            input[type="text"],
            input[type="password"],
            input[type="email"] {
                height: 3em;
            }

            textarea {
                padding: 0.75em 1em;
                min-height: 120px;
                resize: vertical;
            }

            input[type="text"]:focus,
            input[type="password"]:focus,
            input[type="email"]:focus,
            textarea:focus {
                border-color: #e44c65;
            }

            ::-webkit-input-placeholder {
                color: rgba(255, 255, 255, 0.5) !important;
                opacity: 1.0;
            }

            :-moz-placeholder {
                color: rgba(255, 255, 255, 0.5) !important;
                opacity: 1.0;
            }

            ::-moz-placeholder {
                color: rgba(255, 255, 255, 0.5) !important;
                opacity: 1.0;
            }

            :-ms-input-placeholder {
                color: rgba(255, 255, 255, 0.5) !important;
                opacity: 1.0;
            }

            /* Buttons */
            button,
            .button {
                -moz-appearance: none;
                -webkit-appearance: none;
                -ms-appearance: none;
                appearance: none;
                -moz-transition: background-color 0.2s ease-in-out, color 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
                -webkit-transition: background-color 0.2s ease-in-out, color 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
                -ms-transition: background-color 0.2s ease-in-out, color 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
                transition: background-color 0.2s ease-in-out, color 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
                background-color: transparent;
                border-radius: 4px;
                border: 0;
                box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.3);
                color: #ffffff !important;
                cursor: pointer;
                display: inline-block;
                font-size: 0.9em;
                font-weight: 300;
                height: 3em;
                letter-spacing: 0.25em;
                line-height: 3em;
                padding: 0 2em;
                text-align: center;
                text-decoration: none;
                text-transform: uppercase;
                white-space: nowrap;
            }

            button:hover,
            .button:hover {
                box-shadow: inset 0 0 0 1px #e44c65;
                color: #e44c65 !important;
            }

            button.primary,
            .button.primary,
            .btn-primary {
                background-color: #e44c65;
                box-shadow: none;
                color: #ffffff !important;
            }

            button.primary:hover,
            .button.primary:hover,
            .btn-primary:hover {
                background-color: #e76278;
            }

            .btn-logout {
                background-color: transparent;
            }

            /* Headings */
            h1, h2, h3, h4, h5, h6 {
                color: #ffffff;
                font-weight: 300;
                line-height: 1.75em;
                margin: 0 0 1em 0;
            }

            h1 {
                font-size: 2.2em;
                margin-bottom: 1.5em;
            }

            /* Response Messages */
            #response {
                margin-top: 2em;
                padding: 1em;
                border-radius: 4px;
                display: none;
            }

            #response.success {
                background-color: rgba(76, 175, 80, 0.2);
                border: 1px solid rgba(76, 175, 80, 0.5);
                color: #4caf50;
                display: block;
            }

            #response.error {
                background-color: rgba(244, 67, 54, 0.2);
                border: 1px solid rgba(244, 67, 54, 0.5);
                color: #f44336;
                display: block;
            }

            #passwordError {
                color: #f44336;
                display: none;
                margin-bottom: 1em;
                padding: 0.5em;
                background-color: rgba(244, 67, 54, 0.1);
                border-radius: 4px;
                border: 1px solid rgba(244, 67, 54, 0.3);
            }

            /* Scroll Progress Indicator */
            #scroll-progress {
                position: fixed;
                top: 0;
                left: 0;
                width: 0%;
                height: 3px;
                background: linear-gradient(90deg, #e44c65, #e76278);
                z-index: 10001;
                -moz-transition: width 0.1s ease-out;
                -webkit-transition: width 0.1s ease-out;
                -ms-transition: width 0.1s ease-out;
                transition: width 0.1s ease-out;
                box-shadow: 0 2px 4px rgba(228, 76, 101, 0.3);
            }

            /* Responsive */
            @media screen and (max-width: 736px) {
                body {
                    font-size: 15pt;
                }

                .container {
                    width: calc(100% - 2em);
                }

                .wrapper {
                    padding: 3em 0 2em 0;
                    margin-top: 2.75em;
                }

                #header {
                    height: 2.75em;
                    line-height: 2.75em;
                }

                #header h1 {
                    left: 1em;
                    font-size: 1em;
                }

                #nav {
                    right: 0.5em;
                }

                #nav ul li {
                    margin-left: 0.5em;
                }

                #nav ul li a {
                    font-size: 0.8em;
                }

                .auth-info {
                    flex-direction: column;
                    align-items: flex-start;
                }
            }
        </style>
    </head>
    <body>
        <div id="scroll-progress"></div>
        <div id="parallax-bg"></div>
        <div id="page-wrapper">
            <!-- Header -->
            <header id="header">
                <h1 id="logo"><a href="/">GoatBot</a></h1>
                <nav id="nav">
                    <ul>
                        <li><a href="/">Home</a></li>
                    </ul>
                </nav>
            </header>

            <!-- Main Content -->
            <div class="wrapper">
                <div class="container">
                    <div class="auth-section fade-in">
                        <div id="authInfo" class="auth-info">
                            <!-- Auth info will be populated by JavaScript -->
                        </div>
                    </div>

                    <header class="major fade-in">
                        <h1>GoatBot Form</h1>
                    </header>

                    <form id="dataForm" class="fade-in">
                        <div class="form-field fade-in">
                            <label for="domain">Domain:</label>
                            <div class="field-description">The subdomain where your bot will be deployed and accessible e.g. youtbot.goatbot.io</div>
                            <input type="text" id="domain" name="domain" required>
                        </div>

                        <div class="form-field fade-in">
                            <label for="title">Title:</label>
                            <div class="field-description">A descriptive title or name for your bot that will be displayed to users.</div>
                            <input type="text" id="title" name="title" required>
                        </div>

                        <div class="form-field fade-in">
                            <label for="bot_audience">For whom the bot is addressed:</label>
                            <div class="field-description">Describe the target audience or user group this bot is designed to serve (e.g., the name of your friend, close ones etc"</div>
                            <textarea id="bot_audience" name="bot_audience" required></textarea>
                        </div>

                        <div class="form-field fade-in">
                            <label for="bot_aim">What is bot's aim / What should it do:</label>
                            <textarea id="bot_aim" name="bot_aim" required></textarea>
                        </div>

                        <div class="form-field fade-in">
                            <label for="bot_tone">What should be bot's general tone:</label>
                            <textarea id="bot_tone" name="bot_tone" required></textarea>
                        </div>

                        <div class="form-field fade-in">
                            <label for="password">Password:</label>
                            <div class="field-description">Password to guard access to the bot</div>
                            <input type="password" id="password" name="password">
                        </div>


                        <div class="form-field fade-in">
                            <label for="password_confirm">Confirm Password:</label>
                            <input type="password" id="password_confirm" name="password_confirm">
                        </div>

                        <div id="passwordError" class="fade-in"></div>

                        <div class="form-field fade-in">
                            <button type="submit" class="button primary">Submit</button>
                        </div>
                    </form>
                    <div id="response" class="fade-in"></div>
                </div>
            </div>
        </div>

        <script>
            // Smooth scrolling and scroll animations
            (function() {
                // Header scroll effect and scroll progress
                const header = document.getElementById('header');
                const scrollProgress = document.getElementById('scroll-progress');
                let lastScroll = 0;

                function handleScroll() {
                    const currentScroll = window.pageYOffset || document.documentElement.scrollTop;
                    const documentHeight = document.documentElement.scrollHeight - window.innerHeight;
                    const scrollPercent = (currentScroll / documentHeight) * 100;

                    // Update scroll progress bar
                    if (scrollProgress) {
                        scrollProgress.style.width = scrollPercent + '%';
                    }

                    // Update header
                    if (currentScroll > 50) {
                        header.classList.add('scrolled');
                    } else {
                        header.classList.remove('scrolled');
                    }

                    lastScroll = currentScroll;
                }

                window.addEventListener('scroll', handleScroll, { passive: true });
                handleScroll(); // Initial check

                // Intersection Observer for fade-in animations
                const observerOptions = {
                    threshold: 0.1,
                    rootMargin: '0px 0px -50px 0px'
                };

                const observer = new IntersectionObserver(function(entries) {
                    entries.forEach(function(entry) {
                        if (entry.isIntersecting) {
                            entry.target.classList.add('visible');
                            // Optionally stop observing after animation
                            // observer.unobserve(entry.target);
                        }
                    });
                }, observerOptions);

                // Observe all elements with fade-in classes
                document.addEventListener('DOMContentLoaded', function() {
                    const animatedElements = document.querySelectorAll('.fade-in, .fade-in-left, .fade-in-right, .scale-in');
                    animatedElements.forEach(function(el) {
                        observer.observe(el);
                    });

                    // Trigger initial animations for elements already in view
                    setTimeout(function() {
                        animatedElements.forEach(function(el) {
                            const rect = el.getBoundingClientRect();
                            const isVisible = rect.top < window.innerHeight && rect.bottom > 0;
                            if (isVisible) {
                                el.classList.add('visible');
                            }
                        });
                    }, 100);
                });

                // Staggered animation delays for form fields
                document.addEventListener('DOMContentLoaded', function() {
                    const formFields = document.querySelectorAll('.form-field.fade-in');
                    formFields.forEach(function(field, index) {
                        field.style.transitionDelay = (index * 0.1) + 's';
                    });
                });

                // Subtle background parallax effect
                let parallaxTicking = false;
                function updateBackgroundParallax() {
                    const scrolled = window.pageYOffset;
                    const parallaxBg = document.getElementById('parallax-bg');
                    if (parallaxBg && window.innerWidth > 736) {
                        const rate = scrolled * 0.3;
                        parallaxBg.style.transform = 'translateY(' + rate + 'px)';
                    }
                    parallaxTicking = false;
                }

                function requestBackgroundParallax() {
                    if (!parallaxTicking) {
                        window.requestAnimationFrame(updateBackgroundParallax);
                        parallaxTicking = true;
                    }
                }

                window.addEventListener('scroll', requestBackgroundParallax, { passive: true });
                window.addEventListener('resize', function() {
                    const parallaxBg = document.getElementById('parallax-bg');
                    if (parallaxBg && window.innerWidth <= 736) {
                        parallaxBg.style.transform = 'translateY(0px)';
                    }
                });
            })();

            // Store current user info
            let currentUser = null;

            // Check authentication status on page load
            async function checkAuth() {
                try {
                    const response = await fetch('/api/auth/me');
                    if (response.ok) {
                        const user = await response.json();
                        currentUser = user;
                        displayAuthenticatedUser(user);
                    } else {
                        currentUser = null;
                        displayLoginPrompt();
                    }
                } catch (error) {
                    currentUser = null;
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
                        <button class="button btn-logout" onclick="logout()">Logout</button>
                    </div>
                `;
            }

            function displayLoginPrompt() {
                const authInfo = document.getElementById('authInfo');
                authInfo.innerHTML = `
                    <div class="login-prompt" style="width: 100%;">
                        <p>Please login or register to continue</p>
                        <button class="button primary" onclick="login()">Login / Register</button>
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
                    user: currentUser ? currentUser.email : null,
                    domain: document.getElementById('domain').value,
                    title: document.getElementById('title').value,
                    bot_audience: document.getElementById('bot_audience').value,
                    bot_aim: document.getElementById('bot_aim').value,
                    bot_tone: document.getElementById('bot_tone').value,
                    password: password || ''
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
