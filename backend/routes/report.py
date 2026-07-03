from flask import Blueprint, jsonify, request
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import io
import pandas as pd
from db import query

report_bp = Blueprint('report', __name__)

@report_bp.route('/api/send-report', methods=['POST'])
def send_report():
    try:
        req_data = request.get_json() or {}
        start_date = req_data.get('start_date')
        end_date = req_data.get('end_date')
        
        if not start_date or not end_date:
            return jsonify({"status": "error", "message": "Filter tanggal tidak boleh kosong"}), 400

        # Kueri dengan format tanggal yang udah disunat biar Excel aman
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

        df = pd.DataFrame(data_transaksi)
        excel_buffer = io.BytesIO()
        
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Laporan Keuangan')
        
        excel_buffer.seek(0)

        # ====================================================
        # KONFIGURASI SMTP RELAY (BREVO)
        # ====================================================
        # Email yang lu daftarin di Brevo
        sender_email = "indehausyoo@gmail.com" 
        
        # MASUKIN KUNCI SMTP DARI BREVO DI SINI (BUKAN PASSWORD GMAIL!)
        sender_password = "xsmtpsib-fdbad16db01586b33859af496cf95057bc0c73e6c40b9cb06ccd88338422634f-ZpE2PxNMlNJs4bYy" 
        
        receiver_email = "adechu121105@gmail.com"

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = f"Laporan Transaksi Laundry Shabria ({period_info})"

        body = f"Halo Owner,\n\nBerikut terlampir file spreadsheet laporan transaksi Laundry Shabria untuk {period_info}.\nLaporan ini di-generate otomatis oleh sistem.\n\nTerima kasih."
        msg.attach(MIMEText(body, 'plain'))

        filename_excel = f"Laporan_Laundry_{start_date}_to_{end_date}.xlsx"
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(excel_buffer.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename="{filename_excel}"')
        msg.attach(part)

        # KUNCI UTAMA: Tembak ke server Brevo pake port 587 dan STARTTLS
        try:
            # Pake timeout 15 detik biar aman
            server = smtplib.SMTP('smtp-relay.brevo.com', 587, timeout=15)
            server.starttls() # Wajib dipanggil buat keamanan jalur
            server.login(sender_email, sender_password)
            server.send_message(msg)
            server.quit()
        except smtplib.SMTPAuthenticationError:
            return jsonify({"status": "error", "message": "Gagal login SMTP Brevo! Cek lagi email dan Kunci SMTP lu."}), 500
        except Exception as e:
            return jsonify({"status": "error", "message": f"Gagal kirim email: {str(e)}"}), 500

        return jsonify({"status": "success", "message": f"Laporan berhasil dikirim ke email owner!"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500