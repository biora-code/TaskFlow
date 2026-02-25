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

### 8. Task Domain Model

The Task model supports hierarchical relationships using a self-referencing foreign key.

Design:

- A task may optionally reference a parent task
- Root tasks (parent = null) represent top-level items
- Subtasks are linked via the parent relationship


### 9. Custom AI Integration Endpoint

A custom Django REST Framework action was implemented:

POST /api/tasks/{id}/generate-subtasks/


- Uses @action(detail=True) to remain REST-compliant
- Validates task ownership explicitly using get_object_or_404
- Makes a secure server-to-server request to OpenRouter
- Returns AI-generated suggestions without automatically persisting them
- AI-generated subtasks are returned as suggestions instead of being persisted immediately.

### 10. External API Security

AI integration follows secure design principles:

- OpenRouter API key is stored in environment variables
- No API keys are exposed to the frontend
- All AI calls are executed server-side


### 11. API Usage Examples

Obtain JWT Token
POST /api/token/

Request body:

{
  "username": "user",
  "password": "password"
}

Response:

{
  "access": "<jwt_access_token>",
  "refresh": "<jwt_refresh_token>"
}

Create Task
POST /api/tasks/
Authorization: Bearer <access_token>
{
  "title": "Build Portfolio Website",
  "description": "Create a personal website"
}

Generate AI Subtasks
POST /api/tasks/{id}/generate-subtasks/
Authorization: Bearer <access_token>

Response:

{
  "suggestions": ".............."
}

### 12. Separation of Concerns

The application follows layered responsibilities:

- Authentication: JWT (SimpleJWT)
- Business logic: ViewSets
- Serialization: Dedicated serializers
- Data validation: Model layer
- External services: Isolated in AI action
- State management (frontend): Pinia


### 13. Architectural Trade-Offs  !!!!!!

Given time constraints, priority was given to:

- Secure backend implementation
- Clean RESTful API design
- Automated tests for security and isolation
- Proper AI service integration


Frontend functionality was intentionally limited to focus on backend robustness and architectural clarity.
The API is fully functional and can be consumed by any SPA or mobile client.

### 14. If I Had More Time

### Planned improvements:

- Structured JSON schema validation for AI responses
- Background job processing for AI calls (Celery)
- PostgreSQL for production readiness
- Dockerized environment
- CI/CD pipeline (GitHub Actions)
- Role-based permissions
- Improved frontend task management UI
- Optimistic UI updates and improved state normalization

### 15. How to Run the Project


Backend
python -m venv venv
source venv/bin/activate   (or venv\Scripts\activate on Windows)
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

Create a .env file in the backend root:
OPENROUTER_API_KEY=your_openrouter_key_here

Frontend
npm install
npm run dev

Frontend runs on:

http://localhost:5173

Backend runs on:

http://127.0.0.1:8000

### 16. Final Notes

This project prioritizes:

- Security by default
- Clear architectural structure
- Deterministic behavior
- Proper separation of concerns
- Defensive programming when integrating external services
- The backend is production-structured and ready to scale beyond the current scope.
