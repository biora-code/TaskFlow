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

### 3. UI Framework Choice

PrimeVue 4 was selected as the sole UI library to ensure visual consistency and reduce custom CSS.

The Aura preset theme was chosen for its clean and professional aesthetic, which fits a productivity application context.

### 4. Access Control & Data Isolation

All API endpoints are protected globally using IsAuthenticated as the default permission class.

Reason:

- Security by default
- Prevents accidental exposure of new endpoints
- Ensures consistent protection across the API
- User data isolation is enforced at the queryset level because it:
    - Guarantees that users can only access their own tasks
    - Prevents cross-user data leakage even if request parameters are manipulated
    - Keeps security logic centralized in the backend

### 5. Token Lifecycle Management (Frontend)

The frontend implements automatic token management using Axios interceptors.

Reason:

- Access tokens are automatically attached to every request
- Expired access tokens trigger a refresh flow transparently
- If refresh fails, the user is logged out and redirected to login

This approach:

- Improves user experience by avoiding unexpected session drops
- Keeps authentication logic centralized
- Ensures consistent behavior across all API calls

### 6. Automated Security Tests

Automated backend tests were implemented to validate authentication and data isolation.

The test suite covers:

- Unauthorized access to protected endpoints
- Data isolation between different users
- Prevents regressions during future development:
    - Ensures authentication and isolation logic behaves as expected
    - Demonstrates backend reliability and correctness

### 7. Pagination & Stable Ordering

Pagination was enabled globally using PageNumberPagination.

Reason:

- Prepares the API for scalability
- Required for Level 3 filtering and URL synchronization
- Ensures consistent response structure

A default ordering (-created_at) was added to the Task model.

Reason:

- Prevents unstable pagination results
- Ensures deterministic API responses
- Eliminates pagination warnings

