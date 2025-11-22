# Healthcare Subscription Management System

A Flask-based REST API for managing healthcare subscription plans. Users can signup, login, view available subscription plans, and manage their subscriptions.

## Features

- User authentication (signup/login/logout) with JWT tokens
- Four subscription plans with different pricing tiers
- Subscription management (create, view, cancel)
- SQLite database for easy setup

## Subscription Plans

| Plan | Price | Included Visits | Extra Visit Price | Services |
|------|-------|----------------|-------------------|----------|
| Lite Care Pack | $25/month | 2 | $15 | Basic check-up |
| Standard Health Pack | $45/month | 4 | $20 | Check-up, Blood analysis |
| Chronic Care Pack | $80/month | 8 | $18 | Blood tests, X-ray, ECG |
| Unlimited Premium Pack | $120/month | Unlimited | $0 | All diagnostics, X-ray, Ultrasound |

## Installation

### 1. Clone/Navigate to the project

```bash
cd fixed_module-6
```

### 2. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set JWT secret (optional for development)

```bash
export JWT_SECRET='your-super-secret-key-here'
```

If not set, a development default will be used (with a warning).

### 5. Run the application

```bash
python app.py
```

The server will start on `http://localhost:5000`

## API Endpoints

### Authentication

#### Signup
```http
POST /api/auth/signup
Content-Type: application/json

{
  "username": "john_doe",
  "password": "secure_password"
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "john_doe",
  "password": "secure_password"
}
```

Returns a JWT token in a cookie.

#### Logout
```http
POST /api/auth/logout
```

#### Get Current User
```http
GET /api/auth/me
Authorization: Bearer <token>
```

### Subscription Plans

#### List All Plans
```http
GET /api/plans
Authorization: Bearer <token>
```

#### View My Subscriptions
```http
GET /api/subscriptions
Authorization: Bearer <token>
```

#### Subscribe to a Plan
```http
POST /api/subscriptions
Authorization: Bearer <token>
Content-Type: application/json

{
  "plan_id": 1,
  "duration_days": 30
}
```

#### Cancel Subscription
```http
DELETE /api/subscriptions/<subscription_id>
Authorization: Bearer <token>
```

## Usage Example

```bash
# 1. Signup
curl -X POST http://localhost:5000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"username":"test_user","password":"test123"}'

# 2. Login (save the cookie)
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test_user","password":"test123"}' \
  -c cookies.txt

# 3. View plans
curl -X GET http://localhost:5000/api/plans \
  -b cookies.txt

# 4. Subscribe to plan ID 2
curl -X POST http://localhost:5000/api/subscriptions \
  -H "Content-Type: application/json" \
  -d '{"plan_id":2,"duration_days":30}' \
  -b cookies.txt

# 5. View my subscriptions
curl -X GET http://localhost:5000/api/subscriptions \
  -b cookies.txt
```

## Project Structure

```
fixed_module-6/
├── app.py              # Main application file
├── config.py           # Configuration settings
├── models.py           # Database models (User, Plan, Subscription)
├── auth.py             # Authentication blueprint and helpers
├── routes.py           # Main routes (plans, subscriptions)
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Database

The application uses SQLite with the following schema:

- **User**: id, username, password (hashed)
- **Plan**: id, name, price, included_visits, extra_visit_price, services_json
- **Subscription**: id, user_id, plan_id, start_date, end_date

## Security Notes

- Passwords are hashed using bcrypt
- JWT tokens are used for authentication
- Tokens expire after 6 hours
- In production, set a strong `JWT_SECRET` environment variable
- In production, enable HTTPS and add `secure=True` to cookies

## Troubleshooting

**Import errors**: Make sure you're in the virtual environment
```bash
source venv/bin/activate
```

**Database not found**: The database is created automatically on first run

**JWT errors**: Set the JWT_SECRET environment variable

## Development

To run in development mode with debug enabled:
```bash
python app.py
```

The application will automatically reload on code changes.

## License

Educational project - free to use and modify.
