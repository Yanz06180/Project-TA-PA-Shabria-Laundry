from flask import Blueprint, request, jsonify
from db import query, execute

laporan_bp = Blueprint("laporan", __name__)

@laporan_bp.route("/pengeluaran", methods=["GET"])
def get_pengeluaran():
    df = request.args.get("from", "2000-01-01")
    dt = request.args.get("to",   "2099-12-31")
    return jsonify(query(
        """SELECT p.*, CONCAT(u.first_name,' ',u.last_name) AS kasir_nama
           FROM pengeluaran p JOIN users u ON p.id_user = u.id_user
           WHERE p.tanggal BETWEEN %s AND %s
           ORDER BY p.tanggal DESC""",
        (df, dt)
    ))

@laporan_bp.route("/pengeluaran", methods=["POST"])
def add():
    d = request.get_json()
    lid = execute(
        "INSERT INTO pengeluaran (id_user,deskripsi,jumlah,kategori,tanggal) VALUES (%s,%s,%s,%s,CURDATE())",
        (d["id_user"], d["deskripsi"], d["jumlah"], d.get("kategori","Operasional"))
    )
    return jsonify({"id": lid}), 201

@laporan_bp.route("/ringkasan", methods=["GET"])
def ringkasan():
    df = request.args.get("from", "2000-01-01")
    dt = request.args.get("to",   "2099-12-31")
    p_in  = query(
        "SELECT COALESCE(SUM(total_bayar),0) AS total FROM transaksi WHERE sudah_dibayar=1 AND DATE(tanggal_masuk) BETWEEN %s AND %s",
        (df, dt), fetchall=False
    )
    p_out = query(
        "SELECT COALESCE(SUM(jumlah),0) AS total FROM pengeluaran WHERE tanggal BETWEEN %s AND %s",
        (df, dt), fetchall=False
    )
    count = query(
        "SELECT COUNT(*) AS total FROM transaksi WHERE DATE(tanggal_masuk) BETWEEN %s AND %s",
        (df, dt), fetchall=False
    )
    pemasukan    = int(p_in["total"])
    pengeluaran  = int(p_out["total"])
    return jsonify({
        "pemasukan":       pemasukan,
        "pengeluaran":     pengeluaran,
        "net_profit":      pemasukan - pengeluaran,
        "total_transaksi": int(count["total"]),
    })

@laporan_bp.route("/per-kategori", methods=["GET"])
def per_kategori():
    df = request.args.get("from", "2000-01-01")
    dt = request.args.get("to",   "2099-12-31")
    return jsonify(query(
        """SELECT j.jenis_nama, SUM(dt.sub_harga) AS total
           FROM detail_transaksi dt
           JOIN layanan l ON dt.layanan_id_layanan = l.id_layanan
           JOIN jenis_barang j ON l.jenis_barang_id_jenis_barang = j.id_jenis_barang
           JOIN transaksi t ON dt.transaksi_id_transaksi = t.id_transaksi
           WHERE DATE(t.tanggal_masuk) BETWEEN %s AND %s AND t.sudah_dibayar=1
           GROUP BY j.jenis_nama ORDER BY total DESC""",
        (df, dt)
    ))