-- =============================================================
--  SHABRIA LAUNDRY — SCHEMA DATABASE (TiDB / MySQL compatible)
--  Jalankan file ini sekali di TiDB Cloud SQL Editor
--  atau via mysql client:
--    mysql -h HOST -P 4000 -u USER -p < schema.sql
-- =============================================================

CREATE DATABASE IF NOT EXISTS shabria_laundry CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE shabria_laundry;

-- ── ROLE ─────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS role (
    id_role     INT AUTO_INCREMENT PRIMARY KEY,
    nama_role   VARCHAR(50)  NOT NULL,          -- 'admin' | 'manager'
    deskripsi   VARCHAR(255)
);

INSERT IGNORE INTO role (id_role, nama_role, deskripsi) VALUES
(1, 'admin',   'Kasir — kelola transaksi & pelanggan'),
(2, 'manager', 'Owner — monitoring & laporan');

-- ── USER ─────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS user (
    id_user     INT AUTO_INCREMENT PRIMARY KEY,
    first_name  VARCHAR(100) NOT NULL,
    last_name   VARCHAR(100) NOT NULL,
    email       VARCHAR(150) NOT NULL UNIQUE,
    password    VARCHAR(255) NOT NULL,           -- bcrypt hash
    id_role     INT NOT NULL,
    aktif       TINYINT(1) DEFAULT 1,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_role) REFERENCES role(id_role)
);

-- Password = bcrypt('admin123') dan bcrypt('manager123')
INSERT IGNORE INTO user (id_user, first_name, last_name, email, password, id_role) VALUES
(1, 'Siti',   'Aminah',   'siti@shabria.com',    '$2b$12$placeholder_hash_admin1',   1),
(2, 'Budi',   'Kurniawan', 'budi@shabria.com',   '$2b$12$placeholder_hash_admin2',   1),
(3, 'Hendra', 'Kusuma',   'manager@shabria.com', '$2b$12$placeholder_hash_manager',  2);

-- ── PELANGGAN ─────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS pelanggan (
    id_pelanggan    INT AUTO_INCREMENT PRIMARY KEY,
    pel_first_name  VARCHAR(100) NOT NULL,
    pel_last_name   VARCHAR(100) NOT NULL DEFAULT '',
    pel_no_telepon  VARCHAR(20)  NOT NULL,
    pel_alamat      VARCHAR(255),
    total_transaksi INT DEFAULT 0,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT IGNORE INTO pelanggan (id_pelanggan, pel_first_name, pel_last_name, pel_no_telepon, pel_alamat) VALUES
(1, 'Ahmad',  'Fauzi',   '081111111111', 'Jl. Mawar No. 12, Bandung'),
(2, 'Dewi',   'Lestari', '082222222222', 'Jl. Melati No. 5, Bandung'),
(3, 'Rudi',   'Hartono', '083333333333', 'Jl. Anggrek No. 8, Bandung'),
(4, 'Sri',    'Wahyuni', '084444444444', 'Jl. Dahlia No. 3, Bandung'),
(5, 'Eko',    'Prasetyo','085555555555', 'Jl. Kenanga No. 7, Bandung');

-- ── JENIS_BARANG ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS jenis_barang (
    id_jenis_barang INT AUTO_INCREMENT PRIMARY KEY,
    jenis_nama      VARCHAR(100) NOT NULL
);

INSERT IGNORE INTO jenis_barang (id_jenis_barang, jenis_nama) VALUES
(1, 'Cuci Komplit'),
(2, 'Setrika Saja'),
(3, 'Cuci Kering'),
(4, 'Cuci Lipat'),
(5, 'Pakaian Satuan'),
(6, 'Spesial');

-- ── LAYANAN ──────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS layanan (
    id_layanan      INT AUTO_INCREMENT PRIMARY KEY,
    lay_nama        VARCHAR(200) NOT NULL,
    lay_harga       INT NOT NULL,               -- harga dalam Rupiah
    satuan          VARCHAR(20) NOT NULL,        -- 'kg' | 'pcs' | 'item'
    estimasi_hari   INT DEFAULT 0,
    icon            VARCHAR(10) DEFAULT '🧺',
    id_jenis_barang INT NOT NULL,
    aktif           TINYINT(1) DEFAULT 1,
    FOREIGN KEY (id_jenis_barang) REFERENCES jenis_barang(id_jenis_barang)
);

INSERT IGNORE INTO layanan (lay_nama, lay_harga, satuan, estimasi_hari, icon, id_jenis_barang) VALUES
('Cuci Komplit - Regular',  7000,  'kg', 3, '👔', 1),
('Cuci Komplit - Express',  10000, 'kg', 1, '⚡', 1),
('Cuci Komplit - Same Day', 15000, 'kg', 0, '🚀', 1),
('Setrika Saja - Regular',  4000,  'kg', 2, '🔥', 2),
('Setrika Saja - Express',  6000,  'kg', 1, '🔥', 2),
('Cuci Kering - Regular',   5000,  'kg', 2, '🫧', 3),
('Cuci Kering - Express',   7000,  'kg', 1, '🫧', 3),
('Cuci Lipat - Regular',    6000,  'kg', 2, '👕', 4),
('Jas / Blazer',            20000, 'pcs', 3, '🤵', 5),
('Gaun / Dress',            22000, 'pcs', 3, '👗', 5),
('Jaket / Hoodie',          15000, 'pcs', 2, '🧥', 5),
('Kemeja Formal / Batik',   12000, 'pcs', 2, '👔', 5),
('Cuci Karpet - Kecil',     15000, 'item', 3, '🧹', 6),
('Cuci Karpet - Sedang',    30000, 'item', 3, '🧹', 6),
('Cuci Sepatu - Sneakers',  25000, 'pcs', 3, '👟', 6),
('Cuci Sepatu - Kulit',     35000, 'pcs', 3, '👞', 6),
('Cuci Bedcover - Single',  25000, 'item', 3, '🛏️', 6),
('Cuci Bedcover - Queen',   35000, 'item', 3, '🛏️', 6),
('Cuci Boneka - Kecil',     15000, 'pcs', 2, '🧸', 6),
('Cuci Boneka - Sedang',    25000, 'pcs', 2, '🧸', 6);

-- ── ADD_ON ───────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS add_on (
    id_add_on       INT AUTO_INCREMENT PRIMARY KEY,
    add_nama        VARCHAR(100) NOT NULL,
    tambahan_harga  INT NOT NULL,
    icon            VARCHAR(10) DEFAULT '✨',
    aktif           TINYINT(1) DEFAULT 1
);

INSERT IGNORE INTO add_on (add_nama, tambahan_harga, icon) VALUES
('Parfum Downy',   3000,  '🌸'),
('Parfum Molto',   3000,  '🌺'),
('Setrika Ekstra', 2000,  '🔥'),
('Pick Up Only',   5000,  '🏍️'),
('Delivery Only',  5000,  '📦');

-- ── TRANSAKSI ────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS transaksi (
    id_transaksi        VARCHAR(20) PRIMARY KEY,   -- format: TRX-001
    id_pelanggan        INT NOT NULL,
    id_user             INT NOT NULL,              -- kasir yang input
    tanggal_masuk       DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    est_tanggal_selesai DATE,
    tanggal_keluar      DATETIME,
    total_bayar         INT NOT NULL DEFAULT 0,
    mtd_pembayaran      ENUM('Cash','Cashless') NOT NULL,
    sudah_dibayar       TINYINT(1) DEFAULT 0,
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_pelanggan) REFERENCES pelanggan(id_pelanggan),
    FOREIGN KEY (id_user) REFERENCES user(id_user)
);

-- ── DETAIL_TRANSAKSI ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS detail_transaksi (
    id_detail           INT AUTO_INCREMENT PRIMARY KEY,
    id_transaksi        VARCHAR(20) NOT NULL,
    id_layanan          INT NOT NULL,
    sub_harga           INT NOT NULL,
    status_pengerjaan   ENUM('Antrean','Dicuci','Disetrika','Siap','Selesai','Dibatalkan') DEFAULT 'Antrean',
    jumlah_barang       INT DEFAULT 1,
    berat_barang        DECIMAL(6,2) DEFAULT 0,
    catatan             TEXT,
    FOREIGN KEY (id_transaksi) REFERENCES transaksi(id_transaksi),
    FOREIGN KEY (id_layanan)   REFERENCES layanan(id_layanan)
);

-- ── DETAIL_ADDON (join detail_transaksi ↔ add_on) ───────────
CREATE TABLE IF NOT EXISTS detail_addon (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    id_detail       INT NOT NULL,
    id_add_on       INT NOT NULL,
    harga_saat_itu  INT NOT NULL,
    FOREIGN KEY (id_detail)  REFERENCES detail_transaksi(id_detail),
    FOREIGN KEY (id_add_on)  REFERENCES add_on(id_add_on)
);

-- ── PENGELUARAN (laporan loss) ───────────────────────────────
CREATE TABLE IF NOT EXISTS pengeluaran (
    id_pengeluaran  INT AUTO_INCREMENT PRIMARY KEY,
    id_user         INT NOT NULL,
    deskripsi       VARCHAR(255) NOT NULL,
    jumlah          INT NOT NULL,
    kategori        VARCHAR(50) DEFAULT 'Operasional',
    tanggal         DATE NOT NULL DEFAULT (CURRENT_DATE),
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_user) REFERENCES user(id_user)
);
