# Spec: Registration

## Overview
Implement the user registration feature for Spendly. The GET `/register` route already renders the form; this step wires up the POST handler to validate input, check for duplicate emails, hash the password, and insert the new user into the `users` table. On success the user is redirected to the login page. On failure the form is re-rendered with a clear error message and pre-populated fields. This is the first user-facing write operation and the gateway to all authenticated features.

## Depends on
- Step 01 — Database setup (`users` table must exist, `get_db()` must be working)

## Routes
- `GET /register` — render registration form — public *(already exists, no change needed)*
- `POST /register` — validate input, insert user, redirect to login — public

## Database changes
No database changes. The `users` table (id, name, email, password_hash, created_at) is already created by `init_db()`.

## Templates
- **Modify:** `templates/register.html` — already renders `{{ error }}`; add `value="{{ name }}"` and `value="{{ email }}"` to the name and email inputs so fields repopulate on validation errors

## Files to change
- `app.py` — add `methods=['GET', 'POST']` to the `register` route; implement POST handler with validation, hashing, and DB insert

## Files to create
None.

## New dependencies
No new dependencies. `werkzeug.security.generate_password_hash` is already installed.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only — never use string formatting in SQL
- Passwords hashed with `werkzeug.security.generate_password_hash`
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Catch `sqlite3.IntegrityError` to handle duplicate email — do not pre-check with a SELECT
- Redirect to `url_for('login')` on successful registration
- Re-render `templates/register.html` with `error=` and repopulated `name`/`email` on failure
- Validate server-side: name not empty, email not empty, password ≥ 8 characters
- Do not auto-login after registration — that belongs to Step 03 (Login)
- Password field must always be cleared on re-render (never repopulate it)

## Definition of done
- [ ] Submitting valid name, email, and password creates a new row in the `users` table with a hashed password
- [ ] Successful registration redirects to `/login`
- [ ] Submitting a duplicate email re-renders the form with the message "An account with that email already exists"
- [ ] Submitting an empty name, email, or password re-renders the form with a descriptive error
- [ ] Submitting a password shorter than 8 characters shows an error
- [ ] Name and email fields are repopulated after a validation error
- [ ] Password field is always empty after any error
- [ ] App starts and runs without errors after changes to `app.py`
