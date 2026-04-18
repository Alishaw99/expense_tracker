# Spec: Expense List

## Overview
Add a dedicated `/expenses` page that shows the logged-in user's full expense history in a sortable table. Users can filter by category using a dropdown. This is the first dedicated expense view, building on the summary already visible on the profile page and giving users a complete, browsable record of their spending.

## Depends on
- Step 01 — Database (expenses table must exist)
- Step 03 — Login/Logout (login_required decorator)
- Step 04 — Profile page (establishes the authenticated page pattern)

## Routes
- `GET /expenses` — display all expenses for the logged-in user, optional `?category=` query param filter — logged-in only

## Database changes
No database changes. Reads from the existing `expenses` table using `get_db()`.

## Templates
- **Create:** `templates/expenses.html` — full expense list page extending `base.html`
- **Modify:** `templates/base.html` — add a nav link to `/expenses` for logged-in users (alongside the existing Logout link)

## Files to change
- `app.py` — implement the `GET /expenses` route (currently a placeholder at `/expenses/add`)
- `templates/base.html` — add Expenses nav link for logged-in users

## Files to create
- `templates/expenses.html`

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only — never interpolate category into SQL strings
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- The category filter must use a whitelist from `CATEGORIES` in `database/db.py` — reject unknown values silently (treat as no filter)
- `@login_required` must be applied to the route
- Sort expenses by date DESC, then id DESC (most recent first)

## Definition of done
- [ ] `GET /expenses` renders the expense list for the logged-in demo user (8 rows visible)
- [ ] Selecting a category from the dropdown filters the list to only that category
- [ ] Selecting "All" (default) shows all expenses
- [ ] Visiting `/expenses` while logged out redirects to `/login`
- [ ] An account with zero expenses shows an empty-state message instead of a table
- [ ] The nav bar shows an "Expenses" link for logged-in users
- [ ] Category filter only accepts values from the fixed CATEGORIES list (unknown values ignored)
