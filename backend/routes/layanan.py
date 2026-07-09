from flask import Blueprint, request, jsonify
from db import query, execute

layanan_bp = Blueprint("layanan", __name__)

@layanan_bp.route("/", methods=["GET"])
def get_all():
    # HAPUS 'WHERE l.aktif = 1' biar list nonaktif tetep dikirim ke frontend buat ditampilin abu-abu
    rows = query(
        """SELECT l.*, j.jenis_nama
        FROM layanan l
        JOIN jenis_barang j ON l.id_jenis_barang = j.id_jenis_barang"""
    )
    return jsonify(rows)

@layanan_bp.route("/jenis", methods=["GET"])
def get_jenis():
    return jsonify(query("SELECT * FROM jenis_barang ORDER BY id_jenis_barang"))

# 🌟 TAMBAHAN BARU: API buat nambahin Katalog/Jenis dari Modal
@layanan_bp.route("/jenis", methods=["POST"])
def create_jenis():
    try:
        # Ambil data JSON, kalau kosong (None) jadikan dictionary kosong {}
        d = request.get_json() or {}
        
        # JURUS AMAN: Coba cari key "jenis_nama". Kalau nggak ada, cari key "nama". 
        nama_katalog = d.get("jenis_nama") or d.get("nama")
        
        # Validasi kalau frontend ngirim form kosong
        if not nama_katalog:
            return jsonify({"error": "Nama katalog tidak boleh kosong! (Cek script frontend lu)"}), 400
            
        jid = execute(
            "INSERT INTO jenis_barang (jenis_nama) VALUES (%s)",
            (nama_katalog,)
        )
        return jsonify({"id_jenis_barang": jid, "message": "Katalog berhasil dibuat"}), 201
        
    except Exception as e:
        # JURUS PAMUNGKAS: Kalau database lu yang error (misal salah nama tabel/kolom),
        # server lu NGGAK BAKAL MELEDAK 500 HTML lagi. 
        # Dia bakal nge-return error aslinya dalam format JSON biar gampang dibaca!
        print(f"Error Database di create_jenis: {str(e)}")
        return jsonify({"error": f"Gagal menyimpan ke database: {str(e)}"}), 500

@layanan_bp.route("/<int:id>", methods=["GET"])
def get_one(id):
    row = query("SELECT * FROM layanan WHERE id_layanan = %s", (id,), fetchall=False)
    if not row:
        return jsonify({"error": "Layanan tidak ditemukan"}), 404
    return jsonify(row)

@layanan_bp.route("/", methods=["POST"])
def create():
    d = request.get_json()
    aktif = d.get("aktif", True)
    lid = execute(
        """INSERT INTO layanan (lay_nama, lay_harga, satuan, estimasi_hari, icon, id_jenis_barang, aktif)
           VALUES (%s, %s, %s, %s, %s, %s, %s)""",
        (d["lay_nama"], d["lay_harga"], d["satuan"], d.get("estimasi_hari", 0), d.get("icon", "🧺"), d["id_jenis_barang"], aktif)
    )
    return jsonify({"id_layanan": lid}), 201

@layanan_bp.route("/<int:id>", methods=["PUT"])
def update(id):
    d = request.get_json()
    aktif = d.get("aktif", True)
    execute(
        """UPDATE layanan SET lay_nama=%s, lay_harga=%s, satuan=%s,
           estimasi_hari=%s, icon=%s, id_jenis_barang=%s, aktif=%s WHERE id_layanan=%s""",
        (d["lay_nama"], d["lay_harga"], d["satuan"], d.get("estimasi_hari", 0), d.get("icon", "🧺"), d["id_jenis_barang"], aktif, id)
    )
    return jsonify({"message": "Layanan diupdate"})

@layanan_bp.route("/<int:id>", methods=["DELETE"])
def delete(id):
    execute("UPDATE layanan SET aktif=0 WHERE id_layanan=%s", (id,))
    return jsonify({"message": "Layanan dinonaktifkan"})