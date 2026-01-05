# Phase II Full-Stack Todo Application

A production-ready, multi-user todo application with JWT-based authentication and strict user isolation.

## Features

- ✅ User registration and authentication
- ✅ Create tasks with title and description
- ✅ View task list (newest first)
- ✅ Mark tasks as complete/incomplete
- ✅ Edit task details
- ✅ Delete tasks with confirmation
- ✅ Session persistence (7 days)
- ✅ Strict user isolation
- ✅ Responsive design

## Quick Start

See `specs/001-fullstack-todo-app/quickstart.md` for detailed setup instructions.

### Prerequisites
- Python 3.11+
- Node.js 18+
- Neon PostgreSQL account

### Setup
1. Generate JWT secret: `openssl rand -base64 32`
2. Configure `.env` files with BETTER_AUTH_SECRET and DATABASE_URL
3. Run backend: `cd backend && pip install -r requirements.txt && uvicorn src.main:app --reload`
4. Run frontend: `cd frontend && npm install && npm run dev`
5. Visit: http://localhost:3000

## Documentation
- Specification: `specs/001-fullstack-todo-app/spec.md`
- Implementation Plan: `specs/001-fullstack-todo-app/plan.md`
- API Contract: `specs/001-fullstack-todo-app/contracts/api-spec.yaml`
- Quickstart Guide: `specs/001-fullstack-todo-app/quickstart.md`
