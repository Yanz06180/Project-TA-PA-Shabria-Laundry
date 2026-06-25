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
    d = request.get_json()
    jid = execute(
        "INSERT INTO jenis_barang (jenis_nama) VALUES (%s)",
        (d["jenis_nama"],)
    )
    return jsonify({"id_jenis_barang": jid, "message": "Katalog berhasil dibuat"}), 201

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