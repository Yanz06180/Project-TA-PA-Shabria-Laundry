from flask import Blueprint, request, jsonify, Response
from db import query, execute
import csv
from io import StringIO
from datetime import date


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
           JOIN jenis_barang j ON l.id_jenis_barang = j.id_jenis_barang
           JOIN transaksi t ON dt.transaksi_id_transaksi = t.id_transaksi
           WHERE DATE(t.tanggal_masuk) BETWEEN %s AND %s AND t.sudah_dibayar=1
           GROUP BY j.jenis_nama ORDER BY total DESC""",
        (df, dt)
    ))

@laporan_bp.route("/harian/download", methods=["GET"])
def download_laporan_harian():
    # Perbaikan: JOIN ke tabel users untuk ambil nama kasir
    # KUNCI: Pakai DATE_FORMAT buat buang jam, menit, detik dari TiDB!
    sql = """
        SELECT t.id_transaksi, 
               CONCAT(p.pel_first_name, ' ', p.pel_last_name) AS nama_pelanggan, 
               t.total_bayar, 
               t.mtd_pembayaran, 
               CONCAT(u.first_name, ' ', u.last_name) AS kasir_nama, 
               DATE_FORMAT(t.tanggal_masuk, '%%Y-%%m-%%d') AS tanggal_masuk 
        FROM transaksi t
        JOIN pelanggan p ON t.pelanggan_id_pelanggan = p.id_pelanggan
        JOIN users u ON t.users_id_user = u.id_user
        WHERE DATE(t.tanggal_masuk) = CURDATE() AND t.sudah_dibayar = 1
        ORDER BY t.tanggal_masuk DESC
    """
    data = query(sql, fetchall=True)
    
    si = StringIO()
    cw = csv.writer(si, delimiter=';')
    cw.writerow(['ID Transaksi', 'Nama Pelanggan', 'Total Bayar', 'Metode Pembayaran', 'Nama Kasir', 'Tanggal Transaksi'])
    
    for row in data:
        cw.writerow([
            row.get('id_transaksi', '-'),
            row.get('nama_pelanggan', '-'),
            row.get('total_bayar', 0),
            row.get('mtd_pembayaran', '-'),
            row.get('kasir_nama', '-'), 
            row.get('tanggal_masuk', '-') # Sekarang isinya cuma YYYY-MM-DD
        ])
            
    output = si.getvalue()
    tanggal = date.today().strftime("%Y-%m-%d")
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment;filename=Laporan_Harian_{tanggal}.csv"}
    )