# Blog API

A production-ready FastAPI blog application with PostgreSQL, JWT authentication, and auto-seeding.

---

## Quick Start

### macOS / Linux
```bash
./start.sh
```

### Windows
```bat
start.bat
```

These scripts will:
1. Install all dependencies
2. Seed the database with dummy data (skipped if data already exists)
3. Start the development server at `http://localhost:8000`

---

## Manual Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure environment
Create a `.env` file in the root folder:
```
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### 3. Seed the database
```bash
python seed.py
```

### 4. Start the server
```bash
uvicorn main:app --reload
```

API docs available at: `http://localhost:8000/docs`

---

## API Endpoints

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/login` | Login and receive JWT token |

### Users
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/users/` | Register a new user |
| GET | `/users/` | List all users |
| GET | `/users/me` | Get current logged-in user |
| GET | `/users/{id}` | Get user by ID |
| PUT | `/users/{id}` | Update user (auth required) |
| DELETE | `/users/{id}` | Delete user (auth required) |

### Blogs
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/blogs/` | Create a blog post (auth required) |
| GET | `/blogs/` | List all blog posts |
| GET | `/blogs/{id}` | Get blog post by ID |
| PUT | `/blogs/{id}` | Update blog post (owner only) |
| DELETE | `/blogs/{id}` | Delete blog post (owner only) |

### Utility
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/seed` | Manually trigger seeding |

---

## Deploy to Render

1. Push your code to GitHub.
2. Go to [render.com](https://render.com) and create a new **Web Service**.
3. Connect your GitHub repository.
4. Set environment variables:
   - `DATABASE_URL` — your Render PostgreSQL connection string
   - `SECRET_KEY` — a long random secret string
5. Render will use the `render.yaml` config automatically.
6. After deploy, visit `https://your-app.onrender.com/docs` to test.

---

## Docker

```bash
docker build -t blog-api .
docker run -p 10000:10000 --env-file .env blog-api
```
