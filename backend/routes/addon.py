from flask import Blueprint, request, jsonify
from db import query, execute

addon_bp = Blueprint("addon", __name__)

# Mengambil semua add-on yang masih aktif
@addon_bp.route("/", methods=["GET"])
def get_all():
    return jsonify(query("SELECT * FROM add_on WHERE aktif=1 ORDER BY id_add_on"))

# Menambah add-on / antar jemput baru
@addon_bp.route("/", methods=["POST"])
def create():
    d = request.get_json()
    execute(
        "INSERT INTO add_on (add_nama, tambahan_harga, aktif) VALUES (%s, %s, 1)",
        (d["add_nama"], d["tambahan_harga"])
    )
    return jsonify({"message": "Add-on berhasil ditambahkan"}), 201

# Mengedit add-on
@addon_bp.route("/<int:id>", methods=["PUT"])
def update(id):
    d = request.get_json()
    execute(
        "UPDATE add_on SET add_nama=%s, tambahan_harga=%s WHERE id_add_on=%s",
        (d["add_nama"], d["tambahan_harga"], id)
    )
    return jsonify({"message": "Add-on berhasil diupdate"})

# Menghapus add-on (Soft delete / set aktif = 0)
@addon_bp.route("/<int:id>", methods=["DELETE"])
def delete(id):
    execute("UPDATE add_on SET aktif=0 WHERE id_add_on=%s", (id,))
    return jsonify({"message": "Add-on berhasil dihapus"})