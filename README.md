# TaskFlow

## Tech Stack

Backend:
- Django
- Django REST Framework
- JWT (SimpleJWT)

Frontend:
- Vue 3 (Composition API)
- PrimeVue 4
- Pinia
- Vue Router

Database:
- SQLite

---

## Architectural Decisions

### 1. Project Structure

The Django project uses an `apps/` modular structure to improve scalability and separation of concerns.

Reason:
- Encourages clean architecture
- Allows adding more domains later
- Avoids clutter in root

### 2. Authentication Strategy

JWT-based authentication was chosen for:

- Stateless backend
- Scalability
- Compatibility with SPA frontend

Access tokens are short-lived.
Refresh tokens are used to obtain new access tokens.

All endpoints require authentication by default.