from flask import Blueprint, jsonify, request
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import io
import pandas as pd
from db import query  # Menggunakan fungsi query dari db.py kamu

# Bikin blueprint untuk route laporan
report_bp = Blueprint('report', __name__)

# Karena di api.js BASE_URL-nya 'http://https://project-ta-pa-shabria-laundry-backend.vercel.app/api' dan endpoint-nya '/send-report',
# URL utuhnya jadi '/api/send-report'
@report_bp.route('/api/send-report', methods=['POST'])
def send_report():
    try:
        # 1. Tangkap data filter tanggal dari Frontend (laporan.html -> api.js)
        req_data = request.get_json() or {}
        start_date = req_data.get('start_date')  # Format: 'YYYY-MM-DD'
        end_date = req_data.get('end_date')      # Format: 'YYYY-MM-DD'
        
        # Validasi input
        if not start_date or not end_date:
            return jsonify({"status": "error", "message": "Filter tanggal tidak boleh kosong"}), 400

        # 2. Query SQL Gabungan (JOIN transaksi & pelanggan sesuai skema database lu)
        # Sesuai request: menggabung nama depan & belakang, plus nampilin lunas/belum lunas
        sql = """
            SELECT 
                t.id_transaksi AS `ID Transaksi`,
                CONCAT(p.pel_first_name, ' ', COALESCE(p.pel_last_name, '')) AS `Nama Pelanggan`,
                p.pel_no_telepon AS `No Telepon`,
                t.tanggal_masuk AS `Tanggal Masuk`,
                t.tanggal_keluar AS `Tanggal Keluar`,
                t.total_bayar AS `Total Bayar`,
                t.mtd_pembayaran AS `Metode Pembayaran`,
                IF(t.sudah_dibayar = 1, 'Lunas', 'Belum Lunas') AS `Status Pembayaran`
            FROM transaksi t
            JOIN pelanggan p ON t.pelanggan_id_pelanggan = p.id_pelanggan
            WHERE t.tanggal_masuk BETWEEN %s AND %s
            ORDER BY t.tanggal_masuk DESC
        """
        
        # Tambahkan waktu agar mencakup sampai akhir hari (misal 23:59:59)
        start_param = f"{start_date} 00:00:00"
        end_param = f"{end_date} 23:59:59"
        
        # Eksekusi query
        data_transaksi = query(sql, (start_param, end_param))
        period_info = f"Periode {start_date} s/d {end_date}"
        
        # Cek jika data kosong di rentang tanggal tersebut
        if not data_transaksi:
            return jsonify({"status": "error", "message": f"Tidak ada data transaksi pada {period_info}"}), 404

        # 3. Generate file Excel di RAM (In-Memory) menggunakan Pandas
        df = pd.DataFrame(data_transaksi)
        excel_buffer = io.BytesIO()
        
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Laporan Keuangan')
        
        excel_buffer.seek(0)

        # =======================================================
        # 4. KONFIGURASI EMAIL SMTP (GANTI BAGIAN INI)
        # =======================================================
        sender_email = "indehausyoo@gmail.com"  # Ganti email pengirim
        sender_password = "pxwo yzht gfgf tksk"    # 🔴 WAJIB PAKAI 16 DIGIT APP PASSWORD GMAIL!
        receiver_email = "adechu121105@gmail.com" # Ganti email owner
        # =======================================================

        # Setel struktur email
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = f"Laporan Transaksi Laundry Shabria ({period_info})"

        body = f"Halo Owner,\n\nBerikut terlampir file spreadsheet laporan transaksi Laundry Shabria untuk {period_info}.\nLaporan ini di-generate otomatis oleh sistem (Filter Custom).\n\nTerima kasih."
        msg.attach(MIMEText(body, 'plain'))

        # 5. Lampirkan file Excel hasil generate
        filename_excel = f"Laporan_Laundry_{start_date}_to_{end_date}.xlsx"
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(excel_buffer.read())
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename="{filename_excel}"',
        )
        msg.attach(part)

        # 6. Proses Pengiriman via SMTP Server Gmail
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()

        return jsonify({"status": "success", "message": f"Laporan ({period_info}) berhasil dikirim ke email owner!"}), 200

    except Exception as e:
        # Menangkap error kalau ada masalah di server / SMTP / SQL
        return jsonify({"status": "error", "message": f"Terjadi kesalahan server: {str(e)}"}), 500