from flask import Blueprint, request, jsonify
from db import query, execute

pelanggan_bp = Blueprint("pelanggan", __name__)


@pelanggan_bp.route("/", methods=["GET"])
def get_all():
    search = request.args.get("q", "")
    if search:
        rows = query(
            """SELECT * FROM pelanggan
               WHERE pel_first_name LIKE %s OR pel_last_name LIKE %s OR pel_no_telepon LIKE %s
               ORDER BY pel_first_name""",
            (f"%{search}%", f"%{search}%", f"%{search}%")
        )
    else:
        rows = query("SELECT * FROM pelanggan ORDER BY pel_first_name")
    return jsonify(rows)


@pelanggan_bp.route("/<int:id>", methods=["GET"])
def get_one(id):
    row = query("SELECT * FROM pelanggan WHERE id_pelanggan = %s", (id,), fetchall=False)
    if not row:
        return jsonify({"error": "Pelanggan tidak ditemukan"}), 404
    return jsonify(row)


@pelanggan_bp.route("/", methods=["POST"])
def create():
    d = request.get_json()
    lid = execute(
        """INSERT INTO pelanggan (pel_first_name, pel_last_name, pel_no_telepon, pel_alamat)
           VALUES (%s, %s, %s, %s)""",
        (d["pel_first_name"], d.get("pel_last_name", ""), d["pel_no_telepon"], d.get("pel_alamat", ""))
    )
    return jsonify({"id_pelanggan": lid, "message": "Pelanggan berhasil ditambahkan"}), 201


@pelanggan_bp.route("/<int:id>", methods=["PUT"])
def update(id):
    d = request.get_json()
    execute(
        """UPDATE pelanggan SET pel_first_name=%s, pel_last_name=%s,
           pel_no_telepon=%s, pel_alamat=%s WHERE id_pelanggan=%s""",
        (d["pel_first_name"], d.get("pel_last_name", ""), d["pel_no_telepon"], d.get("pel_alamat", ""), id)
    )
    return jsonify({"message": "Pelanggan berhasil diupdate"})


@pelanggan_bp.route("/<int:id>", methods=["DELETE"])
def delete(id):
    execute("DELETE FROM pelanggan WHERE id_pelanggan = %s", (id,))
    return jsonify({"message": "Pelanggan berhasil dihapus"})
