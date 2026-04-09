from functools import wraps
from flask import Blueprint, request, session, jsonify
from database.db import get_db, CATEGORIES

expenses_bp = Blueprint('expenses', __name__, url_prefix='/api')


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated


@expenses_bp.route('/expenses/summary', methods=['GET'])
@login_required
def summary():
    user_id = session['user_id']
    conn = get_db()
    by_category = conn.execute(
        """
        SELECT category, SUM(amount) AS total, COUNT(*) AS count
        FROM expenses
        WHERE user_id = ?
        GROUP BY category
        ORDER BY total DESC
        """,
        (user_id,)
    ).fetchall()
    total_row = conn.execute(
        "SELECT SUM(amount) AS total FROM expenses WHERE user_id = ?", (user_id,)
    ).fetchone()
    conn.close()
    return jsonify({
        'by_category': [dict(r) for r in by_category],
        'total': total_row['total'] or 0
    })


@expenses_bp.route('/expenses', methods=['GET'])
@login_required
def list_expenses():
    user_id = session['user_id']
    category = request.args.get('category')
    conn = get_db()
    if category:
        rows = conn.execute(
            "SELECT * FROM expenses WHERE user_id = ? AND category = ? ORDER BY date DESC",
            (user_id, category)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM expenses WHERE user_id = ? ORDER BY date DESC",
            (user_id,)
        ).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@expenses_bp.route('/expenses', methods=['POST'])
@login_required
def create_expense():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'JSON body required'}), 400

    amount = data.get('amount')
    category = data.get('category')
    date = data.get('date')
    description = data.get('description', '')

    if not amount or not category or not date:
        return jsonify({'error': 'amount, category, and date are required'}), 400
    if category not in CATEGORIES:
        return jsonify({'error': f'category must be one of: {CATEGORIES}'}), 400

    user_id = session['user_id']
    conn = get_db()
    cur = conn.execute(
        "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
        (user_id, amount, category, date, description)
    )
    conn.commit()
    row = conn.execute("SELECT * FROM expenses WHERE id = ?", (cur.lastrowid,)).fetchone()
    conn.close()
    return jsonify(dict(row)), 201


@expenses_bp.route('/expenses/<int:expense_id>', methods=['PUT'])
@login_required
def update_expense(expense_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'JSON body required'}), 400

    user_id = session['user_id']
    conn = get_db()
    existing = conn.execute(
        "SELECT * FROM expenses WHERE id = ? AND user_id = ?", (expense_id, user_id)
    ).fetchone()
    if not existing:
        conn.close()
        return jsonify({'error': 'Expense not found'}), 404

    amount = data.get('amount', existing['amount'])
    category = data.get('category', existing['category'])
    date = data.get('date', existing['date'])
    description = data.get('description', existing['description'])

    if category not in CATEGORIES:
        conn.close()
        return jsonify({'error': f'category must be one of: {CATEGORIES}'}), 400

    conn.execute(
        "UPDATE expenses SET amount = ?, category = ?, date = ?, description = ? WHERE id = ?",
        (amount, category, date, description, expense_id)
    )
    conn.commit()
    row = conn.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,)).fetchone()
    conn.close()
    return jsonify(dict(row))


@expenses_bp.route('/expenses/<int:expense_id>', methods=['DELETE'])
@login_required
def delete_expense(expense_id):
    user_id = session['user_id']
    conn = get_db()
    existing = conn.execute(
        "SELECT * FROM expenses WHERE id = ? AND user_id = ?", (expense_id, user_id)
    ).fetchone()
    if not existing:
        conn.close()
        return jsonify({'error': 'Expense not found'}), 404

    conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Deleted'})
