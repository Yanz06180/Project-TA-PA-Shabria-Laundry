from flask import Blueprint, send_file
import io
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, inch
from reportlab.lib import colors

invoice_bp = Blueprint('invoice', __name__)

# --- 1. DESAIN INVOICE A4 (ESTETIK) ---
@invoice_bp.route("/invoice/download/<id_transaksi>", methods=["GET"])
def download_invoice(id_transaksi):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # --- HEADER INVOICE ---
    # Bikin blok warna biru di atas
    c.setFillColor(colors.HexColor("#1565C0"))
    c.rect(0, height - 40*mm, width, 40*mm, fill=1, stroke=0)
    
    # Masukin Logo
    logo_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'Logo.jpeg')
    try:
        # Mask='auto' biar background logo lu transparan menyatu sama biru
        c.drawImage(logo_path, 15*mm, height - 35*mm, width=25*mm, height=25*mm, preserveAspectRatio=True, mask='auto')
    except Exception as e:
        print(f"Gagal load logo: {e}")
        
    # Teks Perusahaan (Warna Putih)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(45*mm, height - 20*mm, "SHABRIA LAUNDRY")
    c.setFont("Helvetica", 10)
    c.drawString(45*mm, height - 26*mm, "Jl. Raya Salatiga No. 123 | Telp: 08123456789")
    
    # Tulisan INVOICE gede di kanan
    c.setFont("Helvetica-Bold", 30)
    c.drawRightString(width - 15*mm, height - 25*mm, "INVOICE")
    
    # --- DETAIL CUSTOMER & TRANSAKSI ---
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(15*mm, height - 55*mm, "Kepada Yth:")
    c.setFont("Helvetica", 11)
    c.drawString(15*mm, height - 62*mm, "Pelanggan Setia") # Nanti lu bisa passing data DB kesini
    
    c.setFont("Helvetica-Bold", 11)
    c.drawString(120*mm, height - 55*mm, "Detail Transaksi:")
    c.setFont("Helvetica", 11)
    c.drawString(120*mm, height - 62*mm, f"No. Nota  : {id_transaksi}")
    c.drawString(120*mm, height - 68*mm, "Status      : LUNAS")
    
    # --- TABEL LAYANAN ---
    # Header Tabel
    c.setFillColor(colors.HexColor("#F3F4F6"))
    c.rect(15*mm, height - 90*mm, width - 30*mm, 10*mm, fill=1, stroke=0)
    
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(20*mm, height - 87*mm, "DESKRIPSI LAYANAN")
    c.drawRightString(width - 20*mm, height - 87*mm, "SUBTOTAL")
    
    # Isi Tabel (Dummy dlu, nanti lu sambungin sama query DB lu)
    c.setFont("Helvetica", 10)
    c.drawString(20*mm, height - 100*mm, "1. Rincian Pakaian (Sesuai Database)")
    c.drawRightString(width - 20*mm, height - 100*mm, "Rp ...")
    
    # Garis Pembatas
    c.setStrokeColor(colors.lightgrey)
    c.line(15*mm, height - 110*mm, width - 15*mm, height - 110*mm)
    
    # Total Bayar
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.HexColor("#1565C0"))
    c.drawString(90*mm, height - 125*mm, "TOTAL BAYAR:")
    c.drawRightString(width - 20*mm, height - 125*mm, "Rp ...")
    
    # --- FOOTER ---
    c.setFillColor(colors.grey)
    c.setFont("Helvetica-Oblique", 9)
    c.drawCentredString(width/2, 20*mm, "Terima kasih telah mempercayakan pakaian Anda pada Shabria Laundry.")
    
    c.save()
    buffer.seek(0)
    # as_attachment=False biar ga di-download IDM
    return send_file(buffer, as_attachment=False, download_name=f"Invoice_{id_transaksi}.pdf", mimetype="application/pdf")


# --- 2. DESAIN LABEL THERMAL (RAPI & TEGAS) ---
# --- 2. DESAIN LABEL THERMAL 58mm (LURUS & PRO) ---
@invoice_bp.route("/label/download/<id_transaksi>", methods=["GET"])
def download_label(id_transaksi):
    buffer = io.BytesIO()
    
    # KUNCI FIX-NYA: Lebar wajib 58mm (ukuran standar printer kasir kecil)
    # Tinggi kita set 60mm (Proporsional lurus ke bawah)
    label_width = 58 * mm
    label_height = 60 * mm 
    
    c = canvas.Canvas(buffer, pagesize=(label_width, label_height))
    
    # Bikin Border Margin Tipis (2mm dari ujung kertas)
    c.setLineWidth(1)
    c.rect(2*mm, 2*mm, label_width - 4*mm, label_height - 4*mm)
    
    # Header Shabria Laundry
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(label_width/2, label_height - 10*mm, "SHABRIA")
    c.drawCentredString(label_width/2, label_height - 15*mm, "LAUNDRY")
    
    # Garis Putus-putus Pembatas
    c.setLineWidth(1)
    c.setDash(2, 2) # Bikin efek garis putus-putus
    c.line(4*mm, label_height - 20*mm, label_width - 4*mm, label_height - 20*mm)
    c.setDash(1, 0) # Reset garis normal
    
    # Label "ID TRANSAKSI"
    c.setFont("Helvetica", 8)
    c.drawCentredString(label_width/2, label_height - 27*mm, "ID TRANSAKSI:")
    
    # No Transaksi (Font Raksasa Biar Jelas di Kresek)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(label_width/2, label_height - 35*mm, f"{id_transaksi}")
    
    # Garis Putus-putus Pembatas Bawah
    c.setDash(2, 2)
    c.line(4*mm, label_height - 42*mm, label_width - 4*mm, label_height - 42*mm)
    c.setDash(1, 0)
    
    # Footer Slogan
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(label_width/2, 10*mm, "Cucian Bersih,")
    c.drawCentredString(label_width/2, 6*mm, "Hati Tenang")
    
    c.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=False, download_name=f"Label_{id_transaksi}.pdf", mimetype="application/pdf")