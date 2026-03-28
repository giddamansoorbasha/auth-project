# 🔐 AuthKit — Production-Grade User Authentication API

![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supabase-336791?style=flat&logo=postgresql)
![JWT](https://img.shields.io/badge/Auth-JWT-000000?style=flat&logo=jsonwebtokens)

A production-grade authentication system built with FastAPI, PostgreSQL, and JWT.
Includes a clean frontend UI — fully connected end to end.

---

## 🚀 Live Demo
> Coming soon — deploying with Railway

---

## ✨ Features

- ✅ User Signup with bcrypt password hashing
- ✅ User Login with JWT Access Token
- ✅ Refresh Token (7 days) — silent re-auth
- ✅ Logout — wipes refresh token from DB
- ✅ Protected routes with `get_current_user` dependency
- ✅ Clean Frontend UI — Landing, Signup, Login, Dashboard
- ✅ Cloud PostgreSQL via Supabase
- ✅ Industry-standard project structure

---

## 🧱 Tech Stack

| Layer | Tech |
|---|---|
| Backend | FastAPI, Python 3.12 |
| Database | PostgreSQL (Supabase) |
| ORM | SQLAlchemy |
| Auth | JWT (python-jose), bcrypt (passlib) |
| Validation | Pydantic v2 |
| Frontend | HTML, CSS, Vanilla JS |

---

## 📁 Project Structure
```
auth_project/
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── config.py       ← ENV vars (pydantic-settings)
│   │   └── security.py     ← JWT + bcrypt logic
│   ├── db/
│   │   ├── database.py     ← SQLAlchemy engine + session
│   │   └── models.py       ← User model
│   ├── schemas/
│   │   └── auth.py         ← Pydantic schemas
│   ├── services/
│   │   └── auth_service.py ← Business logic
│   └── routers/
│       └── auth.py         ← API endpoints
├── index.html              ← Frontend UI
├── .env.example            ← ENV template
├── requirements.txt
└── README.md
```

---

## ⚙️ Local Setup
```bash
# 1. Clone
git clone https://github.com/YOUR_USERNAME/auth-project.git
cd auth-project

# 2. Create virtual env
python -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup .env
cp .env.example .env
# Fill in your values

# 5. Run
uvicorn app.main:app --reload
```

---

## 🔑 Environment Variables
```env
DATABASE_URL=postgresql://...
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

---

## 📡 API Endpoints

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/auth/signup` | Create account | ❌ |
| POST | `/auth/login` | Get tokens | ❌ |
| POST | `/auth/refresh` | New access token | ❌ |
| POST | `/auth/logout` | Wipe refresh token | ✅ |
| GET | `/auth/me` | Get current user | ✅ |
| GET | `/health` | Health check | ❌ |

---

## 👨‍💻 Author

**Gidda Mansoor Basha**
B.Tech CSE-AIML @ Jain University, Bangalore
[GitHub](https://github.com/YOUR_USERNAME) · [LinkedIn](https://linkedin.com/in/YOUR_USERNAME)