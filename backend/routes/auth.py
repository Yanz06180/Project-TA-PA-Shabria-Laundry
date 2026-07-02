from flask import Blueprint, request, jsonify, session
from db import query

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data     = request.get_json() or {}
    email    = (data.get("email") or "").strip()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"error": "Email dan password wajib diisi"}), 400

    user = query(
        """SELECT u.id_user, u.first_name, u.last_name, u.email, u.password,
                  r.nama_role
           FROM users u
           JOIN roles r ON u.roles_id_role = r.id_role
           WHERE u.email = %s""",
        (email,), fetchall=False
    )

    if not user:
        return jsonify({"error": "Email atau password salah"}), 401

    # Cek password polosan langsung sesuai database lu
    if password != user["password"]:
        return jsonify({"error": "Email atau password salah"}), 401

    # PENTING: lowercase role agar konsisten di frontend
    role = (user["nama_role"] or "").strip().lower()

    result = {
        "id":    user["id_user"],
        "nama":  f"{user['first_name']} {user['last_name']}".strip(),
        "email": user["email"],
        "role":  role,
    }

    session["user_id"]   = result["id"]
    session["user_nama"] = result["nama"]
    session["role"]      = role

    return jsonify(result)

@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logout berhasil"})

@auth_bp.route("/me", methods=["GET"])
def me():
    if "user_id" not in session:
        return jsonify({"error": "Belum login"}), 401
    return jsonify({
        "id":   session["user_id"],
        "nama": session["user_nama"],
        "role": session["role"],
    })