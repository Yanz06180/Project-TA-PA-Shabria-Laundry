from flask import Blueprint, jsonify, request
import io
import pandas as pd
import json
import base64
import urllib.request
import urllib.error
from db import query
import os

report_bp = Blueprint('report', __name__)

@report_bp.route('/api/send-report', methods=['POST'])
def send_report():
    try:
        req_data = request.get_json() or {}
        start_date = req_data.get('start_date')
        end_date = req_data.get('end_date')
        
        if not start_date or not end_date:
            return jsonify({"status": "error", "message": "Filter tanggal tidak boleh kosong"}), 400

        # Kueri lu yang udah aman format tanggalnya
        sql = """
            SELECT 
                t.id_transaksi AS `ID Transaksi`,
                CONCAT(p.pel_first_name, ' ', COALESCE(p.pel_last_name, '')) AS `Nama Pelanggan`,
                p.pel_no_telepon AS `No Telepon`,
                DATE_FORMAT(t.tanggal_masuk, '%%Y-%%m-%%d') AS `Tanggal Masuk`,
                DATE_FORMAT(t.est_tanggal_selesai, '%%Y-%%m-%%d') AS `Tanggal Keluar`,
                t.total_bayar AS `Total Bayar`,
                t.mtd_pembayaran AS `Metode Pembayaran`,
                IF(t.sudah_dibayar = 1, 'Lunas', 'Belum Lunas') AS `Status Pembayaran`
            FROM transaksi t
            JOIN pelanggan p ON t.pelanggan_id_pelanggan = p.id_pelanggan
            WHERE t.tanggal_masuk BETWEEN %s AND %s
            ORDER BY t.tanggal_masuk DESC
        """
        
        start_param = f"{start_date} 00:00:00"
        end_param = f"{end_date} 23:59:59"
        
        data_transaksi = query(sql, (start_param, end_param))
        period_info = f"Periode {start_date} s/d {end_date}"
        
        if not data_transaksi:
            return jsonify({"status": "error", "message": f"Tidak ada data transaksi pada {period_info}"}), 404

        # Bikin Excel di Memori
        df = pd.DataFrame(data_transaksi)
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Laporan Keuangan')
        
        excel_buffer.seek(0)
        
        # KUNCI API BREVO: Ubah Excel jadi base64 biar bisa dikirim lewat JSON API
        excel_base64 = base64.b64encode(excel_buffer.read()).decode('utf-8')
        filename_excel = f"Laporan_Laundry_{start_date}_to_{end_date}.xlsx"

        # Cek Brankas Railway
        api_key = os.environ.get("SMTP_BREVO")
        if not api_key:
            return jsonify({"status": "error", "message": "Kunci API Brevo (SMTP_BREVO) tidak ditemukan di Railway!"}), 500

        # ====================================================
        # JURUS PAMUNGKAS: KIRIM VIA HTTP API (BUKAN SMTP)
        # ====================================================
        payload = {
            "sender": {"email": "indehausyoo@gmail.com", "name": "Shabria Laundry"},
            "to": [{"email": "adechu121105@gmail.com"}],
            "subject": f"Laporan Transaksi Laundry Shabria ({period_info})",
            "textContent": f"Halo Owner,\n\nBerikut terlampir file spreadsheet laporan transaksi Laundry Shabria untuk {period_info}.\nLaporan ini di-generate otomatis oleh sistem.\n\nTerima kasih.",
            "attachment": [{"name": filename_excel, "content": excel_base64}]
        }

        # Nembak langsung ke server API Brevo via HTTPS (Pasti tembus blokiran Railway)
        req_api = urllib.request.Request(
            "https://api.brevo.com/v3/smtp/email",
            data=json.dumps(payload).encode('utf-8'),
            headers={
                "accept": "application/json",
                "api-key": api_key,  # Kunci SMTP Brevo lu berfungsi juga sebagai API Key!
                "content-type": "application/json"
            },
            method="POST"
        )

        try:
            # Kasih waktu 15 detik buat ngirim
            with urllib.request.urlopen(req_api, timeout=15) as response:
                pass # Kalau masuk sini berarti sukses terkirim!
        except urllib.error.HTTPError as e:
            err_msg = e.read().decode('utf-8')
            return jsonify({"status": "error", "message": f"Ditolak API Brevo: {err_msg}"}), 500
        except Exception as e:
            return jsonify({"status": "error", "message": f"Gagal konek ke API Brevo: {str(e)}"}), 500

        return jsonify({"status": "success", "message": f"Laporan berhasil dikirim ke email owner!"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500