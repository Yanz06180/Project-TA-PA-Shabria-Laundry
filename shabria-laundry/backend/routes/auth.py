from flask import Blueprint, request, session, jsonify
import db
import bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Data tidak valid"}), 400
            
        email = data.get('email', '').strip()
        password = data.get('password', '')

        if not email or not password:
            return jsonify({"error": "Email dan password wajib diisi"}), 400

        # Query SQL disesuaikan: Kolom u.aktif dihapus karena tidak ada di tabel users
        sql = """
            SELECT u.*, r.nama_role AS role 
            FROM users u
            JOIN roles r ON u.roles_id_role = r.id_role
            WHERE u.email = %s
        """
        user = db.query(sql, (email,), fetchall=False)

        if not user:
            return jsonify({"error": "Email tidak terdaftar"}), 401

        # Validasi password menggunakan bcrypt
        if not bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            return jsonify({"error": "Password salah"}), 401

        # Set session di server Flask
        session['user_id'] = user['id_user']
        session['role'] = user['role']

        # Gabungkan nama depan dan belakang agar aman di frontend
        nama_lengkap = f"{user['first_name']} {user['last_name']}".strip()

        return jsonify({
            "id": user['id_user'],            
            "id_user": user['id_user'],
            "first_name": user['first_name'],
            "last_name": user['last_name'],
            "nama": nama_lengkap,             
            "email": user['email'],
            "role": user['role']
        }), 200

    except Exception as e:
        print(f"[AUTH LOGIN CRASH]: {e}")
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500


@auth_bp.route('/me', methods=['GET'])
def me():
    try:
        if 'user_id' not in session:
            return jsonify({"error": "Belum login atau session habis"}), 401

        # Query SQL disesuaikan: Kolom u.aktif dihapus agar tidak crash saat validasi session dashboard
        sql = """
            SELECT u.*, r.nama_role AS role 
            FROM users u
            JOIN roles r ON u.roles_id_role = r.id_role
            WHERE u.id_user = %s
        """
        user = db.query(sql, (session['user_id'],), fetchall=False)

        if not user:
            return jsonify({"error": "User tidak ditemukan"}), 401

        nama_lengkap = f"{user['first_name']} {user['last_name']}".strip()

        return jsonify({
            "id": user['id_user'],            
            "id_user": user['id_user'],
            "first_name": user['first_name'],
            "last_name": user['last_name'],
            "nama": nama_lengkap,             
            "email": user['email'],
            "role": user['role']
        }), 200

    except Exception as e:
        print(f"[AUTH ME CRASH]: {e}")
        return jsonify({"error": "Gagal memuat data session"}), 500


@auth_bp.route('/logout', methods=['POST'])
def logout():
    try:
        session.clear()
        return jsonify({"message": "Logout berhasil"}), 200
    except Exception as e:
        print(f"[AUTH LOGOUT CRASH]: {e}")
        return jsonify({"error": "Gagal melakukan logout"}), 500