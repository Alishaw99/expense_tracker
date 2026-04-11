# Spec: Login and Logout

## Overview
Implement session-based login and logout for Spendly. The GET `/login` route already renders the form; this step wires up the POST handler to validate credentials, verify the hashed password, and store the authenticated user's id in the Flask session. The `/logout` route clears the session and redirects to the landing page. A `login_required` helper is introduced so that future protected routes (profile, expenses) can guard access with a single decorator. This step is the authentication gateway — without it, no user-specific data can be safely served.

## Depends on
- Step 01 — Database setup (`users` table and `get_db()` must be working)
- Step 02 — Registration (a user must exist to log in)

## Routes
- `GET /login` — render login form — public *(already exists, no change needed)*
- `POST /login` — validate credentials, set session, redirect to `/profile` — public
- `GET /logout` — clear session, redirect to `/` — logged-in (safe to call even if not logged in)

## Database changes
No database changes. The `users` table already contains `email` and `password_hash`.

## Templates
- **Modify:** `templates/login.html` — add `value="{{ email }}"` to the email input so it repopulates on a failed login attempt. Password field must always be blank on re-render.
- **Modify:** `templates/base.html` — add conditional nav links: show "Logout" when `session.user_id` is set, show "Login" and "Register" when it is not.

## Files to change
- `app.py` — add `methods=['GET', 'POST']` to the `login` route; implement POST handler; implement `logout` route; add `login_required` decorator; import `session`, `check_password_hash`, `functools.wraps`

## Files to create
None.

## New dependencies
No new dependencies. `flask.session` and `werkzeug.security.check_password_hash` are already available.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only — never use string formatting in SQL
- Passwords hashed with werkzeug — use `check_password_hash` to verify, never compare plaintext
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Use `flask.session` (server-side cookie) to store `user_id` as an integer after successful login
- `app.secret_key` is already set — do not change it
- On failed login, re-render `templates/login.html` with `error=` and repopulated `email`; never reveal whether the email or password was wrong (use a generic message: "Invalid email or password.")
- On successful login, redirect to `url_for('profile')`
- `logout` must call `session.clear()` then redirect to `url_for('landing')`
- `login_required` decorator must redirect to `url_for('login')` if `session.get('user_id')` is falsy
- Do not apply `login_required` to the profile route yet — that belongs to Step 04

## Definition of done
- [ ] Submitting valid email and password sets `session['user_id']` and redirects to `/profile`
- [ ] Submitting an unknown email re-renders the login form with "Invalid email or password."
- [ ] Submitting a correct email but wrong password re-renders the login form with "Invalid email or password."
- [ ] Email field is repopulated after a failed login; password field is always empty
- [ ] Visiting `/logout` clears the session and redirects to `/`
- [ ] After logout, visiting `/logout` again still redirects safely to `/` (no error)
- [ ] `login_required` decorator exists and redirects unauthenticated requests to `/login`
- [ ] `base.html` nav shows "Logout" link when logged in and "Login"/"Register" links when logged out
- [ ] App starts and runs without errors after all changes
