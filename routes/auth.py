from flask import Blueprint, request, session, jsonify
from werkzeug.security import check_password_hash
from database.db import get_db

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'JSON body required'}), 400

    email = data.get('email', '').strip()
    password = data.get('password', '')

    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE email = ?", (email,)
    ).fetchone()
    conn.close()

    if not user or not check_password_hash(user['password_hash'], password):
        return jsonify({'error': 'Invalid credentials'}), 401

    session['user_id'] = user['id']
    return jsonify({
        'message': 'Logged in',
        'user': {'id': user['id'], 'name': user['name'], 'email': user['email']}
    })


@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out'})
