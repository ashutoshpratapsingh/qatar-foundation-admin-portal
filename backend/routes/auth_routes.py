from flask import Blueprint, request, jsonify
from extensions import db, bcrypt
from models import Admin
from flask_jwt_extended import create_access_token
import datetime

auth_bp = Blueprint('auth', __name__)

reset_tokens = {}

# SIGNUP
@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json

    if not all([data.get('full_name'), data.get('email'),
                data.get('password'), data.get('confirm_password')]):
        return jsonify({"error": "All fields required"}), 400

    if data['password'] != data['confirm_password']:
        return jsonify({"error": "Passwords do not match"}), 400

    if len(data['password']) < 8:
        return jsonify({"error": "Password must be at least 8 chars"}), 400

    if Admin.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Account already exists"}), 400

    hashed = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    admin = Admin(
        full_name=data['full_name'],
        email=data['email'],
        password=hashed
    )

    db.session.add(admin)
    db.session.commit()

    return jsonify({"message": "Signup successful"}), 201


# LOGIN
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json

    admin = Admin.query.filter_by(email=data['email']).first()

    if not admin or not bcrypt.check_password_hash(admin.password, data['password']):
        return jsonify({"error": "Invalid email or password"}), 401

    remember = data.get("remember", False)

    expires = datetime.timedelta(days=7) if remember else None

    token = create_access_token(identity=str(admin.id), expires_delta=expires)

    return jsonify({
        "token": token,
        "admin_id": admin.id
    })


# FORGOT PASSWORD
@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.json
    email = data.get("email")

    admin = Admin.query.filter_by(email=email).first()

    if admin:
        token = f"reset-{admin.id}-{datetime.datetime.utcnow().timestamp()}"
        expiry = datetime.datetime.utcnow() + datetime.timedelta(hours=1)

        reset_tokens[token] = {
            "admin_id": admin.id,
            "expires": expiry
        }

        print("RESET LINK:", f"/reset-password/{token}")

    return jsonify({"message": "If email exists, reset link sent"})


# RESET PASSWORD
@auth_bp.route('/reset-password/<token>', methods=['POST'])
def reset_password(token):
    data = request.json

    if token not in reset_tokens:
        return jsonify({"error": "Invalid or expired link"}), 400

    record = reset_tokens[token]

    if datetime.datetime.utcnow() > record["expires"]:
        return jsonify({"error": "Link expired"}), 400

    admin = Admin.query.get(record["admin_id"])

    hashed = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    admin.password = hashed

    db.session.commit()

    del reset_tokens[token]

    return jsonify({"message": "Password reset successful"})