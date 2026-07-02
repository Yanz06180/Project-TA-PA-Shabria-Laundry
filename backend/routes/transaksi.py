from flask import Blueprint, request, jsonify
from db import query, execute
import requests # <-- INI TAMBAHAN BUAT NGE-HIT API FONNTE

transaksi_bp = Blueprint("transaksi", __name__)

# --- FUNGSI KIRIM WA (FONNTE) ---
def kirim_notif_wa(nomor_tujuan, pesan):
    url = "https://api.fonnte.com/send"
    headers = {
        "Authorization": "J3AHPsxHJE2duqmPT8oT" # <-- TOKEN
    }
    data = {
        "target": nomor_tujuan,
        "message": pesan,
        "countryCode": "62", 
    }
    try:
        response = requests.post(url, headers=headers, data=data)
        return response.json()
    except Exception as e:
        print("Error kirim WA:", e)
        return None
# --------------------------------

def gen_id():
    last_trx = query("SELECT id_transaksi FROM transaksi ORDER BY id_transaksi DESC LIMIT 1", fetchall=False)
    if last_trx and last_trx["id_transaksi"].startswith("TRX-"):
        last_num = int(last_trx["id_transaksi"].split("-")[1])
        new_num = last_num + 1
    else:
        new_num = 1
    return f"TRX-{new_num:03d}"

@transaksi_bp.route("/", methods=["GET"])
def get_all():
    date_from = request.args.get("from", "2000-01-01")
    date_to   = request.args.get("to",   "2099-12-31")

    # Kueri 1: Ngambil Induk Transaksi (Cuma 1x Nanya DB)
    rows = query(
        """SELECT t.id_transaksi, t.tanggal_masuk, t.est_tanggal_selesai,
                  t.total_bayar, t.mtd_pembayaran, t.sudah_dibayar,
                  p.id_pelanggan,
                  CONCAT(p.pel_first_name,' ',p.pel_last_name) AS pelanggan_nama,
                  CONCAT(u.first_name,' ',u.last_name) AS kasir_nama,
                  u.id_user
           FROM transaksi t
           LEFT JOIN pelanggan p ON t.pelanggan_id_pelanggan = p.id_pelanggan
           JOIN users u     ON t.users_id_user = u.id_user
           WHERE DATE(t.tanggal_masuk) BETWEEN %s AND %s
           ORDER BY t.tanggal_masuk DESC""",
        (date_from, date_to)
    )

    if not rows:
        return jsonify([])

    # 1. Kumpulin semua ID Transaksi yang didapet di array Python
    trx_ids = [r["id_transaksi"] for r in rows]
    
    # 2. Bikin placeholder %s sebanyak jumlah ID biar dinamis
    placeholders = ', '.join(['%s'] * len(trx_ids))
    
    # Kueri 2: Ngambil SEMUA Detail Transaksi SEKALIGUS (Cuma 1x Nanya DB lagi)
    all_details = query(
        f"""SELECT dt.*, l.lay_nama, l.icon, l.satuan
           FROM detail_transaksi dt
           JOIN layanan l ON dt.layanan_id_layanan = l.id_layanan
           WHERE dt.transaksi_id_transaksi IN ({placeholders})""",
        tuple(trx_ids)
    )

    # 3. Kita kelompokkan detail-nya ke masing-masing ID transaksi pakai Hash Map
    details_map = {}
    for detail in all_details:
        tid = detail["transaksi_id_transaksi"]
        if tid not in details_map:
            details_map[tid] = []
        details_map[tid].append(detail)

    # 4. Tempelin kembali detailnya ke tiap baris transaksi secara kilat di RAM
    for trx in rows:
        trx["detail"] = details_map.get(trx["id_transaksi"], [])

    return jsonify(rows)

@transaksi_bp.route("/<string:id>", methods=["GET"])
def get_one(id):
    trx = query(
        """SELECT t.*, CONCAT(p.pel_first_name,' ',p.pel_last_name) AS pelanggan_nama,
                  p.pel_no_telepon, p.pel_alamat,
                  CONCAT(u.first_name,' ',u.last_name) AS kasir_nama
           FROM transaksi t
           Left JOIN pelanggan p ON t.pelanggan_id_pelanggan = p.id_pelanggan
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
        for ao_req in item.get("addons", []):
            addon_id = ao_req["id"]
            qty      = ao_req["qty"]
            
            ao = query("SELECT tambahan_harga FROM add_on WHERE id_add_on=%s", (addon_id,), fetchall=False)
            if ao:
                execute(
                    "INSERT INTO detail_addon (id_detail, add_on_id_add_on, harga_saat_itu, jumlah_addon) VALUES (%s,%s,%s,%s)",
                    (did, addon_id, ao["tambahan_harga"], qty)
                )

    return jsonify({"id_transaksi": tid}), 201

@transaksi_bp.route("/<string:id>/status", methods=["PATCH"])
def update_status(id):
    d = request.get_json()
    status_baru = d["status_pengerjaan"]
    
    # 1. Update status di database
    execute(
        "UPDATE detail_transaksi SET status_pengerjaan=%s WHERE transaksi_id_transaksi=%s",
        (status_baru, id)
    )
    
    # 2. LOGIKA NOTIFIKASI WA KALAU STATUSNYA SELESAI
    if status_baru == 'Selesai':
        # Tarik data no telp dan nama dari database berdasarkan id transaksi
        trx_data = query(
            """SELECT p.pel_no_telepon, p.pel_first_name 
               FROM transaksi t
               JOIN pelanggan p ON t.pelanggan_id_pelanggan = p.id_pelanggan
               WHERE t.id_transaksi = %s""",
            (id,), fetchall=False
        )
        
        # Eksekusi kirim WA kalau nomor pelanggannya ada di database
        if trx_data and trx_data.get("pel_no_telepon"):
            nomor_hp = trx_data["pel_no_telepon"]
            nama = trx_data["pel_first_name"]
            
            pesan_teks = (f"Halo {nama} 👋\n\n"
                          f"Cucian kamu dengan nomor struk {id} di Shabria Laundry udah Selesai nih!\n"
                          f"Silakan diambil ke toko ya. Terima kasih!")
            
            kirim_notif_wa(nomor_hp, pesan_teks)

    return jsonify({"message": "Status diupdate dan notifikasi diproses (jika Selesai)"})