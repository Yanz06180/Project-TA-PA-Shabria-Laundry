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

    # 1. PERBAIKAN: Tambahin u.aktif di query lu biar database ngasih tau statusnya
    user = query(
        """SELECT u.id_user, u.first_name, u.last_name, u.email, u.password,
                  u.aktif, r.nama_role
           FROM users u
           JOIN roles r ON u.roles_id_role = r.id_role
           WHERE u.email = %s""",
        (email,), fetchall=False
    )

    if not user:
        return jsonify({"error": "Email atau password salah"}), 401

    if password != user["password"]:
        return jsonify({"error": "Email atau password salah"}), 401

    # 2. PINTU DEPAN: Cek status aktif, kalau 0 langsung tendang sebelum dikasih sesi!
    if user["aktif"] == 0 or user["aktif"] is False:
        return jsonify({"error": "Akun Anda telah dinonaktifkan oleh Owner!"}), 403

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
        
    # 3. TIKET MASIH BERLAKU?: Cek ulang ke database pas frontend minta data /me
    # Frontend lu (layout.js) kan selalu manggil rute ini pakai requireAuth() tiap pindah halaman
    user_db = query("SELECT aktif FROM users WHERE id_user = %s", (session["user_id"],), fetchall=False)
    
    # Kalau ternyata di tengah jalan dia dinonaktifkan sama Owner:
    if not user_db or user_db["aktif"] == 0:
        session.clear() # Hapus sesinya secara paksa
        return jsonify({"error": "Akun Anda telah dinonaktifkan!"}), 403

    return jsonify({
        "id":   session["user_id"],
        "nama": session["user_nama"],
        "role": session["role"],
    })