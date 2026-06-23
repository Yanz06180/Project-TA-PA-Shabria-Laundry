from flask import Blueprint, request, jsonify
from db import query, execute
import bcrypt

# Definisikan Blueprint untuk route user
user_bp = Blueprint("user", __name__)

# Buka user.py, update fungsi get_all jadi kayak gini:
@user_bp.route("/", methods=["GET"])
def get_all():
    try:
        sql = """
            SELECT u.id_user, u.first_name, u.last_name, u.email, u.aktif,
                   r.nama_role, u.created_at
            FROM users u 
            JOIN roles r ON u.roles_id_role = r.id_role
            ORDER BY u.id_user
        """
        users = query(sql)
        return jsonify(users), 200
    except Exception as e:
        print(f"[USER GET ALL ERROR]: {e}")
        return jsonify({"error": "Gagal mengambil data user"}), 500


@user_bp.route("/", methods=["POST"])
def create():
    """
    Membuat akun user baru (Admin/Kasir) dengan password yang di-hash menggunakan bcrypt.
    """
    try:
        d = request.get_json()
        if not d:
            return jsonify({"error": "Data tidak valid atau kosong"}), 400
        
        first_name = d.get("first_name", "").strip()
        last_name = d.get("last_name", "").strip()
        email = d.get("email", "").strip()
        password = d.get("password", "")
        id_role = d.get("id_role")  # Biasanya 1 untuk Admin/Kasir di database Anda

        # Validasi dasar input teks
        if not first_name or not email or not password or not id_role:
            return jsonify({"error": "Nama depan, email, password, dan role wajib diisi"}), 400

        if len(password) < 6:
            return jsonify({"error": "Password minimal harus 6 karakter"}), 400

        # Cek apakah email sudah terdaftar agar tidak terjadi duplikasi data di TiDB
        check_email = query("SELECT id_user FROM users WHERE email = %s", (email,), fetchall=False)
        if check_email:
            return jsonify({"error": "Email sudah digunakan oleh akun lain"}), 400

        # Proses hashing password demi keamanan data
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Jalankan eksekusi query INSERT ke tabel users
        sql = """
            INSERT INTO users (first_name, last_name, email, password, roles_id_role, aktif)
            VALUES (%s, %s, %s, %s, %s, 1)
        """
        lid = execute(sql, (first_name, last_name, email, hashed_pw, id_role))
        
        return jsonify({"id_user": lid, "message": "Akun berhasil didaftarkan"}), 201

    except Exception as e:
        print(f"[USER CREATE CRASH]: {e}")
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500


@user_bp.route("/<int:id>/aktif", methods=["PATCH"])
def toggle(id):
    """
    Mengaktifkan atau menonaktifkan status akun staf (suspend/unsuspend).
    Mengubah nilai kolom 'aktif' menjadi 1 atau 0.
    """
    try:
        d = request.get_json()
        if not d or "aktif" not in d:
            return jsonify({"error": "Status 'aktif' diperlukan"}), 400

        status_aktif = int(d["aktif"])
        
        # Validasi apakah user yang mau di-toggle memang eksis
        user_exist = query("SELECT id_user FROM users WHERE id_user = %s", (id,), fetchall=False)
        if not user_exist:
            return jsonify({"error": "User tidak ditemukan"}), 404

        # Update status aktif di database
        execute("UPDATE users SET aktif = %s WHERE id_user = %s", (status_aktif, id))
        
        return jsonify({"message": f"Status akun user {id} berhasil diubah menjadi {status_aktif}"}), 200

    except Exception as e:
        print(f"[USER TOGGLE STATUS ERROR]: {e}")
        return jsonify({"error": "Gagal memperbarui status keaktifan user"}), 500