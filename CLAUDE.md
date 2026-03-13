# CLAUDE.md — Project Rules & Architecture Guidelines

These rules must be followed in every session, for every change.

---

## 1. Project Structure

Always use a modular structure:
- `app/` folder for all source code
- `.env` file for secrets (never commit this)
- `requirements.txt` for dependencies

---

## 2. Python Compatibility

- Target Python 3.9+
- **CRITICAL:** Do NOT use the `|` operator for type unions (e.g., `str | None`).
- Always use `from typing import Optional` and write `Optional[str]` instead.

---

## 3. Database

- Use **SQLAlchemy 2.0 style** and **Pydantic v2**
- Use **Alembic** for database migrations
- **CRITICAL — Auto-create database on startup:**
  1. Connect to the PostgreSQL server (not a specific database) and check if the target database exists.
  2. If it does NOT exist, CREATE it automatically.
  3. Then connect to the target database.
  4. Auto-create all tables.
  5. Auto-seed dummy data if tables are empty.
- Use `sqlalchemy_utils` (`database_exists`, `create_database`) or raw SQL via `psycopg2` to create the database.
- Add `sqlalchemy-utils` to `requirements.txt`.
- The app must work **out-of-the-box with ZERO manual setup** — no need to manually create a database.

---

## 4. Dependencies (`requirements.txt`)

- **NEVER pin version numbers.**
- Write ONLY the package name, one per line.
- Example: `fastapi` NOT `fastapi==0.100.0`
- No `==`, `>=`, or `~=` version specifiers at all.

---

## 5. Deployment-Ready

- Include a **Dockerfile** for containerized deployment.
- Include a **render.yaml** for Render deployment.
- Use environment variables for all secrets.
- When creating a PostgreSQL database on Render, set Access Control to allow ALL inbound traffic (`0.0.0.0/0`) so it is accessible from anywhere.

---

## 6. GitHub Integration (CRITICAL)

- At the very start of every new project, before generating any code, ask ONLY for the GitHub repository URL.
- Do NOT ask anything else.
- Initialize git and set the remote origin to that URL immediately.

---

## 7. Git Commits (MANDATORY)

- After EVERY change, new feature, or fix: automatically `git add`, commit with a descriptive message, and push to GitHub.
- Never skip this step.
- Commit message format:
  - `feat: add database connection setup`
  - `fix: resolve seed script error`

---

## 8. Password Hashing (CRITICAL — Avoid bcrypt bugs)

- **Do NOT use `passlib`** — it has compatibility issues with newer versions of bcrypt (`AttributeError on __about__`).
- Instead, use `bcrypt` directly:

```python
import bcrypt
hashed = bcrypt.hashpw(
    password.encode('utf-8')[:72],
    bcrypt.gensalt()
)
```

- **ALWAYS truncate passwords to 72 bytes BEFORE hashing:** `password.encode('utf-8')[:72]`
- Add `bcrypt` to `requirements.txt` (NOT `passlib`).

---

## 9. Startup Scripts (CRITICAL)

- Create a `start.sh` script (macOS/Linux) that:
  1. Installs dependencies: `pip install -r requirements.txt`
  2. Runs `python seed.py` to seed the database
  3. Starts the server: `uvicorn main:app --reload`

- Create a `start.bat` script (Windows) that:
  1. Installs dependencies: `pip install -r requirements.txt`
  2. Runs `python seed.py` to seed the database
  3. Starts the server: `uvicorn main:app --reload`

- The scripts must run `seed.py` FIRST, then start the server.
- Make `start.sh` executable: `chmod +x start.sh`
- Users should ONLY need to run `./start.sh` or `start.bat` to get the full app running.
