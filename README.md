# GoatBot

**Multi-tenant AI chat platform** — spin up configurable OpenAI-powered chatbots on unique subdomains, with Auth0-backed admin access, a FastAPI backend, and a Streamlit chat UI behind Caddy.

This repository demonstrates end-to-end product thinking: API design, OAuth2 integration, prompt engineering for scoped assistants, reverse-proxy routing for tenant isolation, and containerized deployment.

**Live deployment:** [goatbot.com.pl](https://goatbot.com.pl)

---

## What it does

1. **Create a bot session** via the API (`POST /api/chat/start`) with a domain slug, title, mission, optional audience/tone, and a chat password.
2. **Route traffic by subdomain** — Caddy forwards `*.goatbot.localhost` to Streamlit and injects `X-Chat-Domain` so each tenant loads the right config from SQLite.
3. **Chat in the browser** — Streamlit streams responses from the OpenAI Chat Completions API; sessions are password-gated per bot.
4. **Secure the dashboard** — Auth0 login flow on the FastAPI app (`/api/auth/*`) for operator-facing flows.

---

## Tech stack

| Area | Choices |
|------|---------|
| **API** | FastAPI, Pydantic v2, Uvicorn |
| **Auth** | Auth0 (OAuth2), Authlib, `python-jose` (JWT), `httpx` |
| **AI** | OpenAI Python SDK, streaming completions |
| **UI** | Streamlit |
| **Data** | SQLite (`chat_sessions.db`) |
| **Edge / routing** | Caddy (wildcard hosts, custom headers) |
| **Ops** | Docker Compose, Grafana (optional in stack) |
| **Quality** | `uv`, Ruff, pytest, pre-commit, `ty` |

---

## Architecture (high level)

```text
Browser ──► Caddy :80/443
              ├── *.goatbot.localhost → Streamlit (+ X-Chat-Domain)
              └── goatbot.localhost /api/* → FastAPI
                        │
                        └── SQLite (per-tenant ChatConfig)
```

Shared Python modules under `shared/` keep Pydantic models and DB access consistent between the API and Streamlit.

---

## Quick start

**Prerequisites:** Docker & Docker Compose, an OpenAI API key, and (for full auth) an Auth0 application.

1. Clone the repo and add a `.env` (or export variables) for Streamlit/OpenAI — see `streamlit-chat` and backend env expectations in [`backend/README.md`](backend/README.md).

2. Map local hostnames. You need the apex host and **each tenant subdomain** you create via the API (replace `mybot` with the `domain` value you store):

   ```text
   127.0.0.1 goatbot.localhost
   127.0.0.1 mybot.goatbot.localhost
   ```

3. Start the stack:

   ```bash
   docker compose up --build
   ```

4. API docs: `http://goatbot.localhost/docs` (or your configured host). Grafana is exposed on port `3000` when enabled in Compose.

For **local development without Docker**, use Python 3.12+, install with `uv sync` (or `pip install -e .` from the project root), run the FastAPI app and Streamlit per [`backend/README.md`](backend/README.md) and your own process manager.

---

## Repository layout

```text
goatbot/
├── backend/           # FastAPI app (auth, chat API, health)
├── streamlit-chat/    # Tenant chat UI + prompts
├── shared/            # ChatConfig, DB, logging
├── infrastructure/    # Extra deployment notes
├── Caddyfile          # Subdomain → Streamlit, main host → API
├── docker-compose.yml
└── pyproject.toml     # Dependencies & tooling (uv)
```

---

## Why this project is useful on a resume

- **Full-stack Python** — REST API, typed models, and a real-time streaming UI.
- **Identity** — Industry-standard OAuth2/OIDC with Auth0, CSRF-style state on login, JWT handling.
- **Multi-tenancy** — Subdomain-based routing and per-tenant configuration without separate deployments.
- **LLM product patterns** — System prompts with scope rules, audience/tone, and streaming UX.
- **Production-shaped defaults** — CORS, reverse proxy, SQLite persistence, Compose-based environments.
