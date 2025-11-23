# Healthcare Subscription Management System

A Flask-based REST API for managing healthcare subscription plans with visit tracking. Users can signup, login, view available subscription plans, manage their subscriptions, and track healthcare visits with automatic billing.

## 🌟 Features

- **User Authentication** - JWT-based signup/login/logout
- **Subscription Plans** - Four pricing tiers from $25 to $120/month
- **Subscription Management** - Subscribe, view, and cancel subscriptions
- **Visit Tracking** - Record healthcare visits with automatic billing
- **Smart Billing** - Free visits within plan limits, automatic charges for extras
- **Monthly Usage Summary** - Track visits used and remaining balance
- **SQLite Database** - Easy setup, no external database required

## 💊 Subscription Plans

| Plan | Price/Month | Included Visits | Extra Visit Price | Services |
|------|------------|----------------|-------------------|----------|
| Lite Care Pack | $25 | 2 | $15 | Basic check-up |
| Standard Health Pack | $45 | 4 | $20 | Check-up, Blood analysis |
| Chronic Care Pack | $80 | 8 | $18 | Blood tests, X-ray, ECG |
| Unlimited Premium Pack | $120 | ∞ Unlimited | $0 | All diagnostics, X-ray, Ultrasound |

## 📦 Installation & Setup

### 1. Navigate to the project

```bash
cd module-6_fix
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

### 4. Configure environment (optional)

Edit `.env` file to customize settings:
```bash
HOST=0.0.0.0
PORT=5001
FLASK_ENV=development
JWT_SECRET=your-secret-key-here
```

### 5. Run the application

```bash
python app.py
```

The server will start on `http://localhost:5001`

---

## 🐳 Docker Installation (Alternative)

### Option 1: Using Docker Compose (Recommended)

```bash
# Build and start the container
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the container
docker-compose down
```

The API will be available at `http://localhost:5001`

### Option 2: Using Docker directly

```bash
# Build the image
docker build -t healthcare-api .

# Run the container
docker run -d \
  -p 5001:5001 \
  -e JWT_SECRET=your-secret-key \
  -v $(pwd)/instance:/app/instance \
  --name healthcare-api \
  healthcare-api

# View logs
docker logs -f healthcare-api

# Stop the container
docker stop healthcare-api
docker rm healthcare-api
```

**Note**: The `-v $(pwd)/instance:/app/instance` flag persists the database between container restarts.

---

## 📚 API Routes

### Quick Reference Table

| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| `POST` | `/api/auth/signup` | ❌ No | Create new user account |
| `POST` | `/api/auth/login` | ❌ No | Login and get JWT token |
| `POST` | `/api/auth/logout` | ❌ No | Logout and clear token |
| `GET` | `/api/auth/me` | ✅ Yes | Get current user info |
| `GET` | `/api/plans` | ✅ Yes | List all available plans |
| `GET` | `/api/subscriptions` | ✅ Yes | View your subscriptions |
| `POST` | `/api/subscriptions` | ✅ Yes | Subscribe to a plan |
| `DELETE` | `/api/subscriptions/<id>` | ✅ Yes | Cancel a subscription |
| `POST` | `/api/visits` | ✅ Yes | Record a healthcare visit |
| `GET` | `/api/visits` | ✅ Yes | Get your visit history |
| `GET` | `/api/visits/summary` | ✅ Yes | Get visit usage summary |

---

## 🔐 Authentication Endpoints

### 1. Signup - Create New Account

**`POST /api/auth/signup`**

Create a new user account.

**Request:**
```json
{
  "username": "john_doe",
  "password": "secure_password"
}
```

**Response (201 Created):**
```json
{
  "message": "User registered successfully"
}
```

**Errors:**
- `400` - Username or password missing
- `400` - User already exists

---

### 2. Login - Get Authentication Token

**`POST /api/auth/login`**

Authenticate and receive JWT token in HTTP-only cookie.

**Request:**
```json
{
  "username": "john_doe",
  "password": "secure_password"
}
```

**Response (200 OK):**
```json
{
  "message": "Login successful",
  "username": "john_doe"
}
```

**Errors:**
- `400` - Username or password missing
- `401` - Invalid credentials

---

### 3. Logout - Clear Session

**`POST /api/auth/logout`**

Logout by clearing the JWT cookie.

**Response (200 OK):**
```json
{
  "message": "Logged out successfully"
}
```

---

### 4. Get Current User

**`GET /api/auth/me`**

Get information about the currently authenticated user.

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "id": 1,
  "username": "john_doe"
}
```

**Errors:**
- `401` - Token invalid or missing
- `404` - User not found

---

## 💊 Plan & Subscription Endpoints

### 5. List All Plans

**`GET /api/plans`**

Get all available subscription plans.

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Lite Care Pack",
    "price": 25.0,
    "included_visits": 2,
    "extra_visit_price": 15.0,
    "services": ["Basic check-up"]
  },
  {
    "id": 2,
    "name": "Standard Health Pack",
    "price": 45.0,
    "included_visits": 4,
    "extra_visit_price": 20.0,
    "services": ["Check-up", "Blood analysis"]
  }
]
```

---

### 6. View My Subscriptions

**`GET /api/subscriptions`**

Get all your subscriptions (active and expired).

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "plan_name": "Standard Health Pack",
    "plan_id": 2,
    "start_date": "2025-11-23",
    "end_date": "2025-12-23",
    "active": true
  }
]
```

---

### 7. Subscribe to a Plan

**`POST /api/subscriptions`**

Subscribe to a healthcare plan.

**Headers:**
```
Authorization: Bearer <token>
```

**Request:**
```json
{
  "plan_id": 2,
  "duration_days": 30
}
```

**Response (201 Created):**
```json
{
  "message": "Subscription created successfully",
  "subscription_id": 1,
  "plan_name": "Standard Health Pack",
  "start_date": "2025-11-23",
  "end_date": "2025-12-23"
}
```

**Errors:**
- `400` - plan_id is required
- `404` - Plan not found
- `400` - Already have an active subscription

---

### 8. Cancel Subscription

**`DELETE /api/subscriptions/<subscription_id>`**

Cancel a subscription.

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "message": "Subscription cancelled successfully"
}
```

**Errors:**
- `404` - Subscription not found
- `403` - Unauthorized (not your subscription)

---

## 🏥 Visit Tracking Endpoints

### 9. Record a Visit

**`POST /api/visits`**

Record a healthcare visit. Automatically calculates billing based on your plan.

**Headers:**
```
Authorization: Bearer <token>
```

**Request:**
```json
{
  "subscription_id": 1,
  "notes": "Regular checkup"
}
```

**Response (201 Created):**
```json
{
  "message": "Visit recorded successfully",
  "visit_id": 1,
  "visit_date": "2025-11-24T10:30:00",
  "cost": 0,
  "charged": false,
  "visits_used_this_month": 1,
  "remaining_free_visits": 3,
  "plan_name": "Standard Health Pack"
}
```

**Billing Logic:**
- **Within limit**: `cost: 0` (free visit)
- **Exceeded limit**: `cost: 20` (charged extra visit price)
- **Unlimited plan**: Always `cost: 0`

**Errors:**
- `400` - subscription_id is required
- `404` - Subscription not found
- `403` - Unauthorized (not your subscription)
- `400` - Subscription has expired

---

### 10. Get Visit History

**`GET /api/visits`**

Get detailed history of all your healthcare visits.

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "visits": [
    {
      "visit_id": 5,
      "visit_date": "2025-11-24T10:30:00",
      "subscription_id": 1,
      "plan_name": "Standard Health Pack",
      "cost": 20.0,
      "was_charged": true,
      "notes": "Exceeded monthly limit"
    },
    {
      "visit_id": 4,
      "visit_date": "2025-11-23T14:20:00",
      "subscription_id": 1,
      "plan_name": "Standard Health Pack",
      "cost": 0,
      "was_charged": false,
      "notes": "Regular checkup"
    }
  ],
  "total_visits": 5
}
```

---

### 11. Get Visit Usage Summary

**`GET /api/visits/summary`**

Get summary of visit usage, remaining visits, and charges for all active subscriptions.

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "subscriptions": [
    {
      "subscription_id": 1,
      "plan_name": "Standard Health Pack",
      "plan_price": 45.0,
      "included_visits": 4,
      "visits_used_this_month": 5,
      "total_visits_all_time": 12,
      "remaining_free_visits": 0,
      "extra_visit_price": 20.0,
      "charges_this_month": 20.0,
      "status": "exceeded",
      "active_until": "2025-12-23"
    }
  ],
  "total_extra_charges": 20.0,
  "month": "November 2025"
}
```

**Status values:**
- `within_limit` - Still have free visits remaining
- `exceeded` - Used more than included visits (extra charges apply)
- `unlimited` - Unlimited plan (no charges)

---

## 💡 Usage Example

```bash
# 1. Signup
curl -X POST http://localhost:5001/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"username":"john","password":"pass123"}'

# 2. Login (save cookie)
curl -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"john","password":"pass123"}' \
  -c cookies.txt

# 3. View available plans
curl -X GET http://localhost:5001/api/plans \
  -b cookies.txt

# 4. Subscribe to Standard Health Pack (plan_id: 2)
curl -X POST http://localhost:5001/api/subscriptions \
  -H "Content-Type: application/json" \
  -d '{"plan_id":2,"duration_days":30}' \
  -b cookies.txt

# 5. Record a visit
curl -X POST http://localhost:5001/api/visits \
  -H "Content-Type: application/json" \
  -d '{"subscription_id":1,"notes":"Regular checkup"}' \
  -b cookies.txt

# 6. Check visit usage
curl -X GET http://localhost:5001/api/visits/summary \
  -b cookies.txt
```

---

## 📂 Project Structure

```
module-6_fix/
├── app.py                          # Main application entry point
├── .env                            # Environment variables
├── .env.example                    # Environment template
├── requirements.txt                # Python dependencies
├── README.md                       # This file
│
├── instance/                       # Database storage
│   └── subscriptions.db           # SQLite database
│
├── scripts/                        # Utility scripts
│   └── init_data.py               # Initialize default plans
│
└── src/                            # Source code
    ├── config/                     # Configuration
    │   ├── database.py            # DB instance
    │   └── settings.py            # Settings from .env
    │
    ├── controllers/                # API controllers
    │   ├── routes.py              # Blueprint registration
    │   ├── auth/                  # Authentication
    │   │   └── routes.py          # Auth endpoints
    │   ├── plans/                 # Plans & subscriptions
    │   │   └── routes.py          # Plans endpoints
    │   └── visits/                # Visit tracking
    │       └── routes.py          # Visit endpoints
    │
    └── models/                     # Database models
        ├── user.py                # User model
        ├── plan.py                # Plan model
        ├── subscription.py        # Subscription model
        └── visit.py               # Visit model
```

---

## 🗄️ Database Schema

The application uses SQLite with the following tables:

**User**
- `id` - Primary key
- `username` - Unique username
- `password` - Bcrypt hashed password

**Plan**
- `id` - Primary key
- `name` - Plan name
- `price` - Monthly price
- `included_visits` - Free visits per month (can be ∞)
- `extra_visit_price` - Cost per visit after limit
- `services_json` - JSON array of included services

**Subscription**
- `id` - Primary key
- `user_id` - Foreign key to User
- `plan_id` - Foreign key to Plan
- `start_date` - Subscription start date
- `end_date` - Subscription expiration date

**Visit** *(New)*
- `id` - Primary key
- `user_id` - Foreign key to User
- `subscription_id` - Foreign key to Subscription
- `visit_date` - Timestamp of visit
- `cost` - Amount charged (0 if within limit)
- `notes` - Optional visit notes

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
