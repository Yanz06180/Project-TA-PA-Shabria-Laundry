from flask import Blueprint, request, jsonify
from db import query, execute
import random, string

transaksi_bp = Blueprint("transaksi", __name__)

def gen_id():
    return "TRX-" + "".join(random.choices(string.digits, k=3))

@transaksi_bp.route("/", methods=["GET"])
def get_all():
    date_from = request.args.get("from", "2000-01-01")
    date_to   = request.args.get("to",   "2099-12-31")

    rows = query(
        """SELECT t.id_transaksi, t.tanggal_masuk, t.est_tanggal_selesai,
                  t.total_bayar, t.mtd_pembayaran, t.sudah_dibayar,
                  p.id_pelanggan,
                  CONCAT(p.pel_first_name,' ',p.pel_last_name) AS pelanggan_nama,
                  CONCAT(u.first_name,' ',u.last_name) AS kasir_nama,
                  u.id_user
           FROM transaksi t
           JOIN pelanggan p ON t.pelanggan_id_pelanggan = p.id_pelanggan
           JOIN users u     ON t.users_id_user = u.id_user
           WHERE DATE(t.tanggal_masuk) BETWEEN %s AND %s
           ORDER BY t.tanggal_masuk DESC""",
        (date_from, date_to)
    )

    for trx in rows:
        trx["detail"] = query(
            """SELECT dt.*, l.lay_nama, l.icon, l.satuan
               FROM detail_transaksi dt
               JOIN layanan l ON dt.layanan_id_layanan = l.id_layanan
               WHERE dt.transaksi_id_transaksi = %s""",
            (trx["id_transaksi"],)
        )
    return jsonify(rows)

@transaksi_bp.route("/<string:id>", methods=["GET"])
def get_one(id):
    trx = query(
        """SELECT t.*, CONCAT(p.pel_first_name,' ',p.pel_last_name) AS pelanggan_nama,
                  p.pel_no_telepon, p.pel_alamat,
                  CONCAT(u.first_name,' ',u.last_name) AS kasir_nama
           FROM transaksi t
           JOIN pelanggan p ON t.pelanggan_id_pelanggan = p.id_pelanggan
           JOIN users u     ON t.users_id_user = u.id_user
           WHERE t.id_transaksi = %s""",
        (id,), fetchall=False
    )
    if not trx:
        return jsonify({"error": "Tidak ditemukan"}), 404
    trx["detail"] = query(
        """SELECT dt.*, l.lay_nama, l.icon, l.satuan
           FROM detail_transaksi dt
           JOIN layanan l ON dt.layanan_id_layanan = l.id_layanan
           WHERE dt.transaksi_id_transaksi = %s""",
        (id,)
    )
    return jsonify(trx)

@transaksi_bp.route("/", methods=["POST"])
def create():
    d   = request.get_json()
    tid = gen_id()

    execute(
        """INSERT INTO transaksi
           (id_transaksi, pelanggan_id_pelanggan, users_id_user,
            tanggal_masuk, est_tanggal_selesai, total_bayar, mtd_pembayaran, sudah_dibayar)
           VALUES (%s,%s,%s,NOW(),%s,%s,%s,%s)""",
        (tid, d["id_pelanggan"], d["id_user"],
         d.get("est_tanggal_selesai"), d["total_bayar"],
         d["mtd_pembayaran"], int(d.get("sudah_dibayar", 1)))
    )

    for item in d.get("items", []):
        did = execute(
            """INSERT INTO detail_transaksi
               (transaksi_id_transaksi, pelanggan_id_pelanggan,
                layanan_id_layanan, sub_harga, status_pengerjaan,
                jumlah_barang, berat_barang, catatan)
               VALUES (%s,%s,%s,%s,'Antrean',%s,%s,%s)""",
            (tid, d["id_pelanggan"], item["id_layanan"], item["sub_harga"],
             item.get("jumlah_barang", 1), item.get("berat_barang", 0),
             item.get("catatan", ""))
        )
        for addon_id in item.get("addons", []):
            ao = query("SELECT tambahan_harga FROM add_on WHERE id_add_on=%s",
                       (addon_id,), fetchall=False)
            if ao:
                execute(
                    "INSERT INTO detail_addon (id_detail, add_on_id_add_on, harga_saat_itu) VALUES (%s,%s,%s)",
                    (did, addon_id, ao["tambahan_harga"])
                )

    return jsonify({"id_transaksi": tid}), 201

@transaksi_bp.route("/<string:id>/status", methods=["PATCH"])
def update_status(id):
    d = request.get_json()
    execute(
        "UPDATE detail_transaksi SET status_pengerjaan=%s WHERE transaksi_id_transaksi=%s",
        (d["status_pengerjaan"], id)
    )
    return jsonify({"message": "Status diupdate"})