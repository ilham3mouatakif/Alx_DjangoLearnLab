# Social Media API

## Setup Instructions

1. **Install Dependencies:**
   ```bash
   pip install django djangorestframework
   ```

2. **Database Migrations:**
   ```bash
   python manage.py makemigrations accounts
   python manage.py migrate
   ```

3. **Run Server:**
   ```bash
   python manage.py runserver
   ```

## User Authentication

The API uses Token Authentication.

### Register
**Endpoint:** `POST /api/users/register/`

**Body:**
```json
{
    "username": "yourusername",
    "password": "yourpassword",
    "bio": "Bio content",
    "email": "user@example.com"
}
```

**Response:** Returns the created user object and an authentication token.

### Login
**Endpoint:** `POST /api/users/login/`

**Body:**
```json
{
    "username": "yourusername",
    "password": "yourpassword"
}
```

**Response:** Returns the authentication token.

### Profile
**Endpoint:** `GET /api/users/profile/`

**Headers:**
```
Authorization: Token <your_token>
```

## User Model
The `CustomUser` model extends Django's `AbstractUser` and includes:
- `bio`: Text field for user biography.
- `profile_picture`: Image field for profile avatar.
- `followers`: Many-to-Many relationship allowing users to follow each other.
