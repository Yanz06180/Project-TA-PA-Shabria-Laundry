from flask import Blueprint, send_file
import io
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from flask import request
import hashlib

# KUNCI UTAMA: Import query buat ngambil data dari database
from db import query 
SECRET_KEY = "SHABRIA_LAUNDRY_RAHASIA_NEGARA"

invoice_bp = Blueprint('invoice', __name__)

# Fungsi kecil buat bikin format Rupiah rapi
def format_rupiah(angka):
    return f"Rp {int(angka):,}".replace(",", ".")

@invoice_bp.route("/invoice/download/<id_transaksi>", methods=["GET"])
def download_invoice(id_transaksi):
    sig = request.args.get("sig")
    expected_sig = hashlib.sha256(f"{id_transaksi}{SECRET_KEY}".encode()).hexdigest()
    
    if sig != expected_sig:
        return "Akses Ditolak! Link tidak valid atau sudah dimanipulasi.", 403
    # --- 1. AMBIL DATA TRANSAKSI UTAMA DARI DB ---
    trx = query(
        """SELECT t.*, CONCAT(p.pel_first_name,' ',p.pel_last_name) AS pelanggan_nama
           FROM transaksi t
           LEFT JOIN pelanggan p ON t.pelanggan_id_pelanggan = p.id_pelanggan
           WHERE t.id_transaksi = %s""",
        (id_transaksi,), fetchall=False
    )
    
    if not trx:
        return "Transaksi tidak ditemukan di Database!", 404

    # --- 2. AMBIL DATA ITEM LAYANAN DARI DB ---
    details = query(
        """SELECT dt.*, l.lay_nama 
           FROM detail_transaksi dt
           JOIN layanan l ON dt.layanan_id_layanan = l.id_layanan
           WHERE dt.transaksi_id_transaksi = %s""",
        (id_transaksi,)
    )

    # --- 3. MULAI BIKIN PDF ---
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Header Biru
    c.setFillColor(colors.HexColor("#1565C0"))
    c.rect(0, height - 40*mm, width, 40*mm, fill=1, stroke=0)
    
    # Load Logo
    logo_path = os.path.join(os.path.dirname(__file__), '..','..', 'frontend','assets', 'Logo.jpeg')
    if os.path.exists(logo_path):
        try:
            c.drawImage(logo_path, 15*mm, height - 35*mm, width=25*mm, height=25*mm, preserveAspectRatio=True, mask='auto')
        except Exception:
            pass
        
    c.setFillColor(colors.white)
    c.setFont("Courier-Bold", 22)
    c.drawString(45*mm, height - 20*mm, "SHABRIA LAUNDRY")
    c.setFont("Courier", 10)
    c.drawString(45*mm, height - 26*mm, "Jl. Raya Salatiga No. 123 | Telp: 08123456789")
    
    c.setFont("Courier-Bold", 30)
    c.drawRightString(width - 15*mm, height - 25*mm, "INVOICE")
    
    # --- INFO CUSTOMER & TRANSAKSI ---
    c.setFillColor(colors.black)
    c.setFont("Courier-Bold", 11)
    c.drawString(15*mm, height - 55*mm, "Kepada Yth:")
    
    # Inject Nama Customer Beneran
    c.setFont("Courier", 11)
    nama_pel = trx["pelanggan_nama"] if trx["pelanggan_nama"] else "Customer Guest"
    c.drawString(15*mm, height - 62*mm, nama_pel) 
    
    c.setFont("Courier-Bold", 11)
    c.drawString(120*mm, height - 55*mm, "Detail Transaksi:")
    c.setFont("Courier", 11)
    c.drawString(120*mm, height - 62*mm, f"No. Nota  : {id_transaksi}")
    
    # Inject Status Bayar Beneran
    status = "LUNAS" if trx["sudah_dibayar"] else "BELUM BAYAR"
    c.drawString(120*mm, height - 68*mm, f"Status    : {status}")
    
    # --- HEADER TABEL ITEM ---
    c.setFillColor(colors.HexColor("#F3F4F6"))
    c.rect(15*mm, height - 90*mm, width - 30*mm, 10*mm, fill=1, stroke=0)
    
    c.setFillColor(colors.black)
    c.setFont("Courier-Bold", 10)
    c.drawString(20*mm, height - 87*mm, "DESKRIPSI LAYANAN")
    c.drawRightString(width - 20*mm, height - 87*mm, "SUBTOTAL")
    
    # --- LOOPING ITEM DARI DATABASE ---
    c.setFont("Courier", 10)
    y_pos = height - 100*mm
    
    for idx, item in enumerate(details):
        # Nentuin dia Kiloan atau Satuan
        qty_text = f"{item['jumlah_barang']} pcs" if item['berat_barang'] == 0 else f"{item['berat_barang']} kg"
        deskripsi = f"{idx+1}. {item['lay_nama']} ({qty_text})"
        subharga = format_rupiah(item['sub_harga'])
        
        c.drawString(20*mm, y_pos, deskripsi)
        c.drawRightString(width - 20*mm, y_pos, subharga)
        
        y_pos -= 7*mm # Turun 1 baris ke bawah
        
        # Biar ngga bablas nabrak bawah kalau cuciannya seabrek
        if y_pos < 60*mm:
            break
    
    # Garis Pembatas Bawah
    c.setStrokeColor(colors.lightgrey)
    c.line(15*mm, y_pos - 3*mm, width - 15*mm, y_pos - 3*mm)
    
# Total Bayar Asli
    y_pos -= 12*mm
    c.setFont("Courier-Bold", 14)
    c.setFillColor(colors.HexColor("#1565C0"))
    c.drawString(90*mm, y_pos, "TOTAL BAYAR:")
    c.drawRightString(width - 20*mm, y_pos, format_rupiah(trx["total_bayar"]))
    
    # --- TAMBAHAN CASH & KEMBALIAN ---
    uang_cash = int(trx.get("uang_cash") or 0)
    kembalian = uang_cash - int(trx["total_bayar"])
    
    y_pos -= 6*mm
    c.setFont("Courier", 11)
    c.setFillColor(colors.black)
    c.drawString(90*mm, y_pos, "TUNAI/CASH:")
    c.drawRightString(width - 20*mm, y_pos, format_rupiah(uang_cash))
    
    y_pos -= 6*mm
    c.drawString(90*mm, y_pos, "KEMBALIAN:")
    c.drawRightString(width - 20*mm, y_pos, format_rupiah(kembalian))
    
    # --- FOOTER ---
    c.setFillColor(colors.grey)
    c.setFont("Courier-Oblique", 9)
    c.drawCentredString(width/2, 20*mm, "Terima kasih telah mempercayakan pakaian Anda pada Shabria Laundry.")
    
    c.save()
    buffer.seek(0)
    
    return send_file(buffer, as_attachment=False, download_name=f"Invoice_{id_transaksi}.pdf", mimetype="application/pdf")