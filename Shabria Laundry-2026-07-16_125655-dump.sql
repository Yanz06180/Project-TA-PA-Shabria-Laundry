-- MySQL dump 10.13  Distrib 8.0.33, for Win64 (x86_64)
--
-- Host: gateway01.ap-southeast-1.prod.alicloud.tidbcloud.com    Database: shabria_laundry
-- ------------------------------------------------------
-- Server version	8.0.11-TiDB-v8.5.3-serverless

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `add_on`
--

DROP TABLE IF EXISTS `add_on`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `add_on` (
  `id_add_on` int NOT NULL AUTO_INCREMENT,
  `add_nama` varchar(255) DEFAULT NULL,
  `tambahan_harga` int DEFAULT NULL,
  `aktif` tinyint(1) DEFAULT '1',
  `kategori` varchar(50) DEFAULT 'Add-on',
  PRIMARY KEY (`id_add_on`) /*T![clustered_index] CLUSTERED */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=30002;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `add_on`
--

LOCK TABLES `add_on` WRITE;
/*!40000 ALTER TABLE `add_on` DISABLE KEYS */;
INSERT INTO `add_on` VALUES (1,'Parfum Premium',5000,1,'Add-on'),(2,'Molto Sekali Bilas',3000,1,'Add-on'),(3,'Antar Jemput Jarak Dekat',10000,1,'Add-on'),(4,'Antar Jemput Jarak Jauh',25000,1,'Add-on');
/*!40000 ALTER TABLE `add_on` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detail_addon`
--

DROP TABLE IF EXISTS `detail_addon`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detail_addon` (
  `id_detail_addon` int NOT NULL AUTO_INCREMENT,
  `id_detail` int NOT NULL,
  `add_on_id_add_on` int NOT NULL,
  `harga_saat_itu` decimal(12,2) NOT NULL,
  `jumlah_addon` int DEFAULT '1',
  PRIMARY KEY (`id_detail_addon`) /*T![clustered_index] CLUSTERED */,
  KEY `fk_1` (`id_detail`),
  KEY `fk_2` (`add_on_id_add_on`),
  CONSTRAINT `fk_1` FOREIGN KEY (`id_detail`) REFERENCES `detail_transaksi` (`id_detail`) ON DELETE CASCADE,
  CONSTRAINT `fk_2` FOREIGN KEY (`add_on_id_add_on`) REFERENCES `add_on` (`id_add_on`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=1260001;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detail_addon`
--

LOCK TABLES `detail_addon` WRITE;
/*!40000 ALTER TABLE `detail_addon` DISABLE KEYS */;
INSERT INTO `detail_addon` VALUES (1,1,1,5000.00,1),(2,2,2,3000.00,1),(3,4,2,3000.00,2),(30001,30002,2,3000.00,1),(30002,30002,1,5000.00,1),(60001,60002,1,5000.00,1),(60002,60002,2,3000.00,1),(90001,90002,2,3000.00,1),(90002,90002,3,10000.00,1),(120001,120002,1,5000.00,1),(120002,120002,4,25000.00,1),(150001,150002,3,10000.00,1),(150002,150003,3,10000.00,1),(180001,180002,1,5000.00,1),(210001,210002,2,3000.00,1),(210002,210002,3,10000.00,1),(240001,240002,1,5000.00,1),(240002,240002,2,3000.00,1),(240003,240002,3,10000.00,1),(270001,270003,2,3000.00,1),(270002,270003,3,10000.00,1),(270003,270004,2,3000.00,1),(270004,270004,3,10000.00,1),(270005,270005,2,3000.00,1),(270006,270005,3,10000.00,1),(300001,300002,2,3000.00,1),(330001,360002,2,3000.00,1),(330002,360002,4,25000.00,1),(330003,360003,2,3000.00,1),(330004,360003,3,10000.00,1),(330005,360004,3,10000.00,1),(360001,420002,2,3000.00,3),(360002,420002,3,10000.00,1),(390001,450002,4,25000.00,1),(420001,480002,4,25000.00,1),(450001,510002,3,10000.00,1),(480001,540002,3,10000.00,1),(510001,570002,3,10000.00,1),(540001,600002,2,3000.00,1),(540002,600002,3,10000.00,1),(570001,630002,2,3000.00,1),(570002,630002,3,10000.00,1),(600001,660002,2,3000.00,1),(600002,660002,3,10000.00,1),(630001,690002,1,5000.00,1),(630002,690002,4,25000.00,1),(660001,720002,1,5000.00,1),(660002,720002,4,25000.00,1),(690001,750002,1,5000.00,1),(690002,750002,4,25000.00,1),(720001,780002,1,5000.00,1),(720002,780002,4,25000.00,1),(750001,810002,1,5000.00,1),(750002,810002,2,3000.00,1),(750003,810002,3,10000.00,1),(780001,840002,2,3000.00,1),(780002,840002,3,10000.00,1),(810001,870002,1,5000.00,4),(810002,870002,2,3000.00,2),(810003,870002,3,10000.00,1),(810004,870003,1,5000.00,4),(810005,870003,2,3000.00,2),(810006,870003,3,10000.00,1),(810007,870004,1,5000.00,4),(810008,870004,2,3000.00,2),(810009,870004,3,10000.00,1),(840001,900002,1,5000.00,2),(840002,900002,2,3000.00,1),(840003,900002,3,10000.00,1),(840004,900003,1,5000.00,2),(840005,900003,2,3000.00,1),(840006,900003,3,10000.00,1),(870001,930002,1,5000.00,1),(870002,930002,2,3000.00,2),(870003,930002,3,10000.00,1),(870004,930003,1,5000.00,1),(870005,930003,2,3000.00,2),(870006,930003,3,10000.00,1),(900001,960002,2,3000.00,1),(900002,960002,3,10000.00,1),(900003,960003,2,3000.00,1),(900004,960003,3,10000.00,1),(900005,960004,2,3000.00,1),(900006,960004,3,10000.00,1),(900007,960005,2,3000.00,1),(900008,960005,3,10000.00,1),(930001,990002,1,5000.00,3),(930002,990002,2,3000.00,2),(930003,990002,4,25000.00,1),(930004,990009,1,5000.00,7),(930005,990009,2,3000.00,4),(930006,990009,4,25000.00,1),(960001,1020002,1,5000.00,1),(960002,1020002,2,3000.00,1),(960003,1020002,4,25000.00,1),(960004,1020003,1,5000.00,1),(960005,1020003,2,3000.00,1),(960006,1020003,4,25000.00,1),(990001,1050002,1,5000.00,2),(990002,1050002,2,3000.00,1),(990003,1050002,3,10000.00,1),(990004,1050007,1,5000.00,1),(990005,1050007,2,3000.00,1),(990006,1050007,3,10000.00,1),(1020001,1080003,1,5000.00,1),(1020002,1080003,2,3000.00,1),(1020003,1080003,3,10000.00,1),(1050001,1110002,4,25000.00,1),(1080001,1140002,1,5000.00,2),(1080002,1140002,2,3000.00,1),(1080003,1140002,3,10000.00,1),(1110001,1170002,1,5000.00,1),(1110002,1170002,4,25000.00,1),(1140001,1200002,1,5000.00,2),(1140002,1200002,3,10000.00,1),(1170001,1230002,3,10000.00,1),(1170002,1230004,3,10000.00,1),(1170003,1230005,2,3000.00,1),(1200001,1260002,2,3000.00,2),(1200002,1260002,3,10000.00,1),(1200003,1260007,2,3000.00,1),(1200004,1260007,3,10000.00,1),(1230001,1290002,1,5000.00,1),(1230002,1290002,3,10000.00,1),(1230003,1290004,1,5000.00,2),(1230004,1290004,3,10000.00,1);
/*!40000 ALTER TABLE `detail_addon` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detail_transaksi`
--

DROP TABLE IF EXISTS `detail_transaksi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detail_transaksi` (
  `id_detail` int NOT NULL AUTO_INCREMENT,
  `transaksi_id_transaksi` varchar(20) NOT NULL,
  `pelanggan_id_pelanggan` int NOT NULL,
  `layanan_id_layanan` int NOT NULL,
  `sub_harga` decimal(12,2) NOT NULL,
  `status_pengerjaan` varchar(50) DEFAULT 'Antrean',
  `jumlah_barang` int DEFAULT '1',
  `berat_barang` int DEFAULT '0',
  `catatan` text DEFAULT NULL,
  PRIMARY KEY (`id_detail`) /*T![clustered_index] CLUSTERED */,
  KEY `fk_1` (`transaksi_id_transaksi`),
  KEY `fk_2` (`pelanggan_id_pelanggan`),
  KEY `fk_3` (`layanan_id_layanan`),
  CONSTRAINT `fk_1` FOREIGN KEY (`transaksi_id_transaksi`) REFERENCES `transaksi` (`id_transaksi`) ON DELETE CASCADE,
  CONSTRAINT `fk_2` FOREIGN KEY (`pelanggan_id_pelanggan`) REFERENCES `pelanggan` (`id_pelanggan`),
  CONSTRAINT `fk_3` FOREIGN KEY (`layanan_id_layanan`) REFERENCES `layanan` (`id_layanan`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=1320002;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detail_transaksi`
--

LOCK TABLES `detail_transaksi` WRITE;
/*!40000 ALTER TABLE `detail_transaksi` DISABLE KEYS */;
INSERT INTO `detail_transaksi` VALUES (1,'TRX-001',1,1,40000.00,'Selesai',1,5,'Baju kerja'),(2,'TRX-002',1,4,40000.00,'Siap',2,0,'Selimut'),(3,'TRX-003',1,5,60000.00,'Dibatalkan',2,0,'Bed cover'),(4,'TRX-004',1,3,20000.00,'Antrean',1,5,'Pakaian harian'),(5,'TRX-005',1,2,18000.00,'Selesai',1,3,'Seragam'),(30002,'TRX-006',1,11,12000.00,'Selesai',1,0,''),(60002,'TRX-007',60001,4,40000.00,'Selesai',2,0,''),(90002,'TRX-008',90001,2,6000.00,'Selesai',1,1,''),(120002,'TRX-009',1,11,12000.00,'Siap',1,0,''),(150002,'TRX-010',60001,6,50000.00,'Antrean',2,0,''),(150003,'TRX-011',60001,2,6000.00,'Antrean',1,1,''),(180002,'TRX-012',60001,2,6000.00,'Antrean',1,1,''),(210002,'TRX-013',60001,2,6000.00,'Antrean',1,1,''),(240002,'TRX-014',60001,3,12000.00,'Selesai',1,3,''),(270002,'TRX-015',60001,2,6000.00,'Antrean',1,1,''),(270003,'TRX-016',60001,3,4000.00,'Antrean',1,1,''),(270004,'TRX-017',60001,2,6000.00,'Antrean',1,1,''),(270005,'TRX-017',60001,13,40000.00,'Antrean',2,0,''),(300002,'TRX-018',60001,4,20000.00,'Antrean',1,0,''),(330002,'TRX-019',60001,3,4000.00,'Antrean',1,1,''),(360002,'TRX-020',60001,3,4000.00,'Antrean',1,1,''),(360003,'TRX-021',60001,3,4000.00,'Antrean',1,1,''),(360004,'TRX-022',60001,3,4000.00,'Antrean',1,1,''),(390002,'TRX-023',60001,3,4000.00,'Antrean',1,1,''),(420002,'TRX-024',60001,3,4000.00,'Selesai',1,1,''),(450002,'TRX-025',60001,3,4000.00,'Antrean',1,1,''),(480002,'TRX-026',90001,3,4000.00,'Antrean',1,1,''),(510002,'TRX-027',90001,3,4000.00,'Antrean',1,1,''),(540002,'TRX-028',60001,3,4000.00,'Antrean',1,1,''),(570002,'TRX-029',60001,3,4000.00,'Antrean',1,1,''),(600002,'TRX-030',60001,3,4000.00,'Antrean',1,1,''),(630002,'TRX-031',60001,2,6000.00,'Antrean',1,1,''),(660002,'TRX-032',60001,3,4000.00,'Antrean',1,1,''),(690002,'TRX-033',90001,2,18000.00,'Antrean',1,3,''),(720002,'TRX-034',90001,2,24000.00,'Selesai',1,4,''),(750002,'TRX-035',60001,2,18000.00,'Antrean',1,3,''),(780002,'TRX-036',60001,3,12000.00,'Selesai',1,3,''),(810002,'TRX-037',60001,11,24000.00,'Selesai',2,0,''),(840002,'TRX-038',60001,2,6000.00,'Antrean',1,1,''),(870002,'TRX-039',60001,2,6000.00,'Antrean',1,1,''),(870003,'TRX-039',60001,9,18000.00,'Antrean',1,0,''),(870004,'TRX-039',60001,14,70000.00,'Antrean',2,0,''),(900002,'TRX-040',90001,1,8000.00,'Antrean',1,1,''),(900003,'TRX-040',90001,7,70000.00,'Antrean',2,0,''),(930002,'TRX-041',90001,2,6000.00,'Selesai',1,1,''),(930003,'TRX-041',90001,8,15000.00,'Selesai',1,0,''),(960002,'TRX-042',60001,2,6000.00,'Antrean',1,1,''),(960003,'TRX-042',60001,9,36000.00,'Antrean',2,0,''),(960004,'TRX-042',60001,4,60000.00,'Antrean',3,0,''),(960005,'TRX-042',60001,11,36000.00,'Antrean',3,0,''),(990002,'TRX-043',60001,2,6000.00,'Antrean',1,1,''),(990003,'TRX-043',60001,3,8000.00,'Antrean',1,2,''),(990004,'TRX-043',60001,9,36000.00,'Antrean',2,0,''),(990005,'TRX-043',60001,13,60000.00,'Antrean',3,0,''),(990006,'TRX-043',60001,6,50000.00,'Antrean',2,0,''),(990007,'TRX-043',60001,7,35000.00,'Antrean',1,0,''),(990008,'TRX-043',60001,9,72000.00,'Antrean',4,0,''),(990009,'TRX-044',60001,1,32000.00,'Selesai',1,4,''),(990010,'TRX-044',60001,4,40000.00,'Selesai',2,0,''),(990011,'TRX-044',60001,6,75000.00,'Selesai',3,0,''),(990012,'TRX-044',60001,8,30000.00,'Selesai',2,0,''),(990013,'TRX-044',60001,9,18000.00,'Selesai',1,0,''),(990014,'TRX-044',60001,10,50000.00,'Selesai',2,0,''),(990015,'TRX-044',60001,11,24000.00,'Selesai',2,0,''),(990016,'TRX-044',60001,12,30000.00,'Selesai',1,0,''),(990017,'TRX-044',60001,13,20000.00,'Selesai',1,0,''),(990018,'TRX-044',60001,14,105000.00,'Selesai',3,0,''),(1020002,'TRX-045',120001,1,80000.00,'Antrean',1,10,''),(1020003,'TRX-046',60001,1,120000.00,'Antrean',1,15,''),(1050002,'TRX-047',60001,12,30000.00,'Antrean',1,0,''),(1050003,'TRX-047',60001,12,30000.00,'Antrean',1,0,''),(1050004,'TRX-047',60001,10,25000.00,'Antrean',1,0,''),(1050005,'TRX-047',60001,9,18000.00,'Antrean',1,0,''),(1050006,'TRX-047',60001,6,50000.00,'Antrean',2,0,''),(1050007,'TRX-048',120001,1,16000.00,'Antrean',1,2,''),(1080002,'TRX-049',150004,1,16000.00,'Antrean',1,2,''),(1080003,'TRX-050',150004,1,24000.00,'Selesai',1,3,''),(1110002,'TRX-051',90001,2,6000.00,'Selesai',1,1,''),(1140002,'TRX-052',60001,8,15000.00,'Selesai',1,0,''),(1140003,'TRX-052',60001,1,24000.00,'Selesai',1,3,''),(1170002,'TRX-053',180001,13,100000.00,'Selesai',5,0,''),(1200002,'TRX-054',60001,2,12000.00,'Selesai',1,2,''),(1230002,'TRX-055',150004,60002,-5000.00,'Antrean',1,1,''),(1230003,'TRX-055',150004,60002,-15000.00,'Antrean',1,3,''),(1230004,'TRX-056',210006,2,12000.00,'Antrean',1,2,''),(1230005,'TRX-057',210006,60002,-20000.00,'Antrean',1,4,''),(1260002,'TRX-058',60001,2,6000.00,'Antrean',1,1,''),(1260003,'TRX-058',60001,5,30000.00,'Antrean',1,0,''),(1260004,'TRX-059',60001,3,4000.00,'Selesai',1,1,''),(1260005,'TRX-060',90001,2,18000.00,'Antrean',1,3,''),(1260006,'TRX-061',60001,3,4000.00,'Antrean',1,1,''),(1260007,'TRX-062',60001,3,4000.00,'Antrean',1,1,''),(1290002,'TRX-063',240001,2,6000.00,'Antrean',1,1,''),(1290003,'TRX-063',240001,4,20000.00,'Antrean',1,0,''),(1290004,'TRX-064',60001,2,6000.00,'Antrean',1,1,''),(1290005,'TRX-064',60001,7,70000.00,'Antrean',2,0,'');
/*!40000 ALTER TABLE `detail_transaksi` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `jenis_barang`
--

DROP TABLE IF EXISTS `jenis_barang`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `jenis_barang` (
  `id_jenis_barang` int NOT NULL AUTO_INCREMENT,
  `jenis_nama` varchar(30) NOT NULL,
  PRIMARY KEY (`id_jenis_barang`) /*T![clustered_index] CLUSTERED */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=90002;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `jenis_barang`
--

LOCK TABLES `jenis_barang` WRITE;
/*!40000 ALTER TABLE `jenis_barang` DISABLE KEYS */;
INSERT INTO `jenis_barang` VALUES (1,'Pakaian Harian'),(2,'Selimut'),(3,'Bed Cover'),(4,'Sprei'),(5,'Boneka'),(6,'Jas / Blazer'),(7,'Gamis'),(8,'Kebaya'),(9,'Sepatu'),(10,'Tas'),(11,'Karpet'),(12,'Jaket Tebal'),(13,'Bantal'),(14,'Gordyn / Kurtain'),(15,'Seragam Sekolah'),(16,'Cuci Motor'),(17,'Cuci Mobil'),(30002,'Cuci Keranjang'),(60002,'Cuci Reguler Karpet');
/*!40000 ALTER TABLE `jenis_barang` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `layanan`
--

DROP TABLE IF EXISTS `layanan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `layanan` (
  `id_layanan` int NOT NULL AUTO_INCREMENT,
  `lay_nama` varchar(255) NOT NULL,
  `lay_harga` int NOT NULL,
  `satuan` varchar(50) NOT NULL,
  `estimasi_hari` int DEFAULT '0',
  `icon` varchar(255) DEFAULT '🧺',
  `id_jenis_barang` int NOT NULL,
  `aktif` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id_layanan`) /*T![clustered_index] CLUSTERED */,
  KEY `fk_1` (`id_jenis_barang`),
  CONSTRAINT `fk_1` FOREIGN KEY (`id_jenis_barang`) REFERENCES `jenis_barang` (`id_jenis_barang`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=120002;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `layanan`
--

LOCK TABLES `layanan` WRITE;
/*!40000 ALTER TABLE `layanan` DISABLE KEYS */;
INSERT INTO `layanan` VALUES (1,'Cuci Kilat Pakaian Harian',8000,'kg',0,'🧺',1,0),(2,'Cuci Express Pakaian Harian',6000,'kg',0,'🧺',1,1),(3,'Cuci Reguler Pakaian Harian',4000,'kg',0,'🧺',1,1),(4,'Cuci Reguler Selimut',20000,'pcs',0,'🧺',2,1),(5,'Cuci Kilat Selimut',30000,'pcs',0,'🧺',2,1),(6,'Cuci Reguler Bed Cover',25000,'pcs',0,'🧺',3,1),(7,'Cuci Express Bed Cover',35000,'pcs',0,'🧺',3,1),(8,'Cuci Reguler Sprei',15000,'pcs',0,'🧺',4,1),(9,'Cuci Reguler Boneka',18000,'pcs',0,'🧺',5,1),(10,'Cuci Express Jas/Blazer',25000,'pcs',0,'🧺',6,1),(11,'Cuci Reguler Gamis',12000,'pcs',0,'🧺',7,1),(12,'Cuci Kilat Kebaya',30000,'pcs',0,'🧺',8,0),(13,'Cuci Reguler Sepatu',20000,'pcs',0,'🧺',9,0),(14,'Cuci Reguler Karpet',35000,'pcs',0,'🧺',11,1),(15,'Cuci Express Jaket Tebal',22000,'pcs',0,'🧺',12,1),(16,'Cuci Motor Bersih Express',25000,'pcs',1,'🧺',16,1),(17,'Cuci Motor Bersih Express Premium',50000,'pcs',1,'🌀',16,1),(18,'Cuci Motor',20000,'item',0,'🏍️',16,1),(30002,'Cuci motor',15000,'item',0,'🏍️',16,1),(60002,'Cuci Express Pakaian Harian',-5000,'kg',-10,'🧺',17,1),(90002,'Cuci Express Jas/Blazer',25000,'kg',0,'🧺',6,1),(90003,'Cuci Kendaraan ***',-111111,'kg',1,'🧺',17,1);
/*!40000 ALTER TABLE `layanan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pelanggan`
--

DROP TABLE IF EXISTS `pelanggan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pelanggan` (
  `id_pelanggan` int NOT NULL AUTO_INCREMENT,
  `pel_first_name` varchar(100) NOT NULL,
  `pel_last_name` varchar(100) DEFAULT NULL,
  `pel_no_telepon` varchar(20) NOT NULL,
  `pel_alamat` text DEFAULT NULL,
  PRIMARY KEY (`id_pelanggan`) /*T![clustered_index] CLUSTERED */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=270001;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pelanggan`
--

LOCK TABLES `pelanggan` WRITE;
/*!40000 ALTER TABLE `pelanggan` DISABLE KEYS */;
INSERT INTO `pelanggan` VALUES (1,'Agus','Santoso','081325671202','Jl. Kartini No. 5, Argomulyo, Salatiga'),(60001,'Bryan','Jonathan','6281227472488','Jl. Salatiga Semarang'),(90001,'Yesaya','Ranu','6281385124665',''),(120001,'Bernard','PH','62882003106960',''),(150002,'PH','Tjahyo','08111111111111','(Opsional)'),(150004,'Abraham','Kiwil','6281337654406',''),(180001,'Cristiano','Ronaldo','6288200101234','Salatiga'),(210006,'Maulana','','08882525556',''),(240001,'Agil','','62882525556','');
/*!40000 ALTER TABLE `pelanggan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pengeluaran`
--

DROP TABLE IF EXISTS `pengeluaran`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pengeluaran` (
  `id_pengeluaran` int NOT NULL AUTO_INCREMENT,
  `id_user` int NOT NULL,
  `deskripsi` varchar(255) NOT NULL,
  `jumlah` int NOT NULL,
  `kategori` varchar(50) DEFAULT 'Operasional',
  `tanggal` datetime NOT NULL,
  PRIMARY KEY (`id_pengeluaran`) /*T![clustered_index] CLUSTERED */,
  KEY `fk_1` (`id_user`),
  CONSTRAINT `fk_1` FOREIGN KEY (`id_user`) REFERENCES `users` (`id_user`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=210001;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pengeluaran`
--

LOCK TABLES `pengeluaran` WRITE;
/*!40000 ALTER TABLE `pengeluaran` DISABLE KEYS */;
INSERT INTO `pengeluaran` VALUES (1,2,'Beli Molto',2000,'Operasional','2026-06-23 00:00:00'),(30001,2,'Beli deterjen',4500,'Operasional','2026-07-02 00:00:00'),(60001,3,'Pembelian pemutih',60000,'Operasional','2026-07-03 00:00:00'),(90001,3,'Beli Pewangi',3000,'Operasional','2026-07-09 00:00:00'),(120001,3,'Beli pemutih',40000,'Operasional','2026-07-11 08:48:04'),(150001,3,'Beli Molto',150000,'Operasional','2026-07-11 10:03:14'),(180001,2,'Beli Harimau',-1111,'Operasional','2026-07-16 04:48:30');
/*!40000 ALTER TABLE `pengeluaran` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `id_role` int NOT NULL,
  `nama_role` varchar(20) NOT NULL,
  `deskripsi` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id_role`) /*T![clustered_index] CLUSTERED */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'admin','Kasir - mengelola transaksi harian dan input data pelanggan'),(2,'owner','Pemilik usaha - akses dashboard, laporan, dan rekap keuangan');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transaksi`
--

DROP TABLE IF EXISTS `transaksi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transaksi` (
  `id_transaksi` varchar(20) NOT NULL,
  `tanggal_masuk` datetime NOT NULL,
  `est_tanggal_selesai` datetime DEFAULT NULL,
  `tanggal_keluar` datetime DEFAULT NULL,
  `total_bayar` decimal(12,2) NOT NULL,
  `mtd_pembayaran` varchar(25) DEFAULT NULL,
  `users_id_user` int NOT NULL,
  `pelanggan_id_pelanggan` int NOT NULL,
  `sudah_dibayar` tinyint(1) DEFAULT '0',
  `uang_cash` int DEFAULT '0',
  PRIMARY KEY (`id_transaksi`) /*T![clustered_index] CLUSTERED */,
  KEY `fk_1` (`users_id_user`),
  KEY `fk_2` (`pelanggan_id_pelanggan`),
  CONSTRAINT `fk_1` FOREIGN KEY (`users_id_user`) REFERENCES `users` (`id_user`),
  CONSTRAINT `fk_2` FOREIGN KEY (`pelanggan_id_pelanggan`) REFERENCES `pelanggan` (`id_pelanggan`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transaksi`
--

LOCK TABLES `transaksi` WRITE;
/*!40000 ALTER TABLE `transaksi` DISABLE KEYS */;
INSERT INTO `transaksi` VALUES ('TRX-001','2026-06-20 08:00:00','2026-06-22 08:00:00',NULL,45000.00,'Cash',2,1,1,0),('TRX-002','2026-06-21 09:30:00','2026-06-23 09:30:00',NULL,43000.00,'Cashless',2,1,1,0),('TRX-003','2026-06-22 14:15:00','2026-06-24 14:15:00',NULL,60000.00,'Cash',2,1,0,0),('TRX-004','2026-06-23 10:00:00','2026-06-25 10:00:00',NULL,25000.00,'Cashless',2,1,1,0),('TRX-005','2026-06-23 11:20:00','2026-06-25 11:20:00',NULL,18000.00,'Cash',2,1,0,0),('TRX-006','2026-06-23 12:55:07',NULL,NULL,20000.00,'Cash',2,1,1,0),('TRX-007','2026-06-24 11:15:38',NULL,NULL,48000.00,'Cash',2,60001,1,0),('TRX-008','2026-06-24 12:32:17',NULL,NULL,19000.00,'Cash',2,90001,1,0),('TRX-009','2026-06-24 13:58:14',NULL,NULL,42000.00,'Cash',2,1,1,0),('TRX-010','2026-06-25 14:15:33',NULL,NULL,60000.00,'Cashless',2,60001,1,0),('TRX-011','2026-06-25 14:20:17',NULL,NULL,16000.00,'Cashless',2,60001,1,0),('TRX-012','2026-06-25 14:37:42',NULL,NULL,11000.00,'Cash',2,60001,1,0),('TRX-013','2026-06-26 03:02:03',NULL,NULL,19000.00,'Cashless',2,60001,1,0),('TRX-014','2026-06-26 07:47:30',NULL,NULL,46000.00,'Cashless',2,60001,1,0),('TRX-015','2026-06-26 23:38:34',NULL,NULL,6000.00,'Cash',2,60001,1,0),('TRX-016','2026-06-26 23:45:50',NULL,NULL,17000.00,'Cashless',2,60001,1,0),('TRX-017','2026-06-26 23:53:55',NULL,NULL,59000.00,'Cashless',2,60001,1,0),('TRX-018','2026-06-27 00:28:06',NULL,NULL,23000.00,'Cashless',2,60001,1,0),('TRX-019','2026-06-27 07:31:28',NULL,NULL,4000.00,'Cashless',2,60001,1,0),('TRX-020','2026-06-27 07:41:14',NULL,NULL,32000.00,'Cashless',2,60001,1,0),('TRX-021','2026-06-27 07:48:13',NULL,NULL,17000.00,'Cashless',2,60001,1,0),('TRX-022','2026-06-27 07:52:45',NULL,NULL,14000.00,'Cashless',2,60001,1,0),('TRX-023','2026-06-27 11:59:44',NULL,NULL,4000.00,'Cashless',2,60001,1,0),('TRX-024','2026-06-27 14:23:26',NULL,NULL,23000.00,'Cashless',2,60001,1,0),('TRX-025','2026-06-28 12:29:11',NULL,NULL,29000.00,'Cashless',2,60001,1,0),('TRX-026','2026-06-28 15:27:22',NULL,NULL,29000.00,'Cashless',2,90001,1,0),('TRX-027','2026-06-29 10:35:36',NULL,NULL,14000.00,'Cashless',2,90001,1,0),('TRX-028','2026-06-29 10:52:51',NULL,NULL,14000.00,'Cashless',2,60001,1,0),('TRX-029','2026-06-29 13:07:46',NULL,NULL,14000.00,'Cashless',2,60001,1,0),('TRX-030','2026-07-02 03:34:18',NULL,NULL,17000.00,'Cashless',2,60001,1,0),('TRX-031','2026-07-02 13:41:40',NULL,NULL,19000.00,'Cashless',2,60001,1,0),('TRX-032','2026-07-02 13:50:22',NULL,NULL,17000.00,'Cashless',2,60001,1,0),('TRX-033','2026-07-02 13:58:09',NULL,NULL,58000.00,'Cashless',2,90001,1,0),('TRX-034','2026-07-02 14:05:29',NULL,NULL,69000.00,'Cashless',2,90001,1,0),('TRX-035','2026-07-02 14:13:58',NULL,NULL,58000.00,'Cashless',2,60001,1,0),('TRX-036','2026-07-02 14:36:20',NULL,NULL,52000.00,'Cashless',2,60001,1,0),('TRX-037','2026-07-02 14:51:49',NULL,NULL,42000.00,'Cashless',2,60001,1,0),('TRX-038','2026-07-03 15:02:08',NULL,NULL,19000.00,'Cash',3,60001,1,50000),('TRX-039','2026-07-04 10:10:46',NULL,NULL,130000.00,'Cashless',3,60001,1,130000),('TRX-040','2026-07-04 10:24:55',NULL,NULL,101000.00,'Cashless',3,90001,1,101000),('TRX-041','2026-07-04 10:32:55',NULL,NULL,42000.00,'Cashless',3,90001,1,42000),('TRX-042','2026-07-06 10:13:20',NULL,NULL,151000.00,'Cash',3,60001,1,200000),('TRX-043','2026-07-06 10:24:59',NULL,NULL,355000.00,'Cash',3,60001,1,400000),('TRX-044','2026-07-06 10:31:05',NULL,NULL,637000.00,'Cashless',3,60001,1,637000),('TRX-045','2026-07-07 10:18:27',NULL,NULL,185000.00,'Cash',3,120001,1,200000),('TRX-046','2026-07-07 10:26:56',NULL,NULL,265000.00,'Cash',3,60001,1,300000),('TRX-047','2026-07-09 05:00:32',NULL,NULL,176000.00,'Cashless',3,60001,1,176000),('TRX-048','2026-07-09 06:00:56',NULL,NULL,42000.00,'Cashless',3,120001,1,42000),('TRX-049','2026-07-09 06:42:00',NULL,NULL,16000.00,'Cashless',3,150004,1,16000),('TRX-050','2026-07-09 06:52:16',NULL,NULL,58000.00,'Cashless',3,150004,1,58000),('TRX-051','2026-07-09 09:04:17',NULL,NULL,31000.00,'Cash',3,90001,1,40000),('TRX-052','2026-07-09 09:25:29',NULL,NULL,88000.00,'Cashless',3,60001,1,88000),('TRX-053','2026-07-11 09:10:54',NULL,NULL,130000.00,'Cash',3,180001,1,150000),('TRX-054','2026-07-11 11:50:32',NULL,NULL,42000.00,'Cash',3,60001,1,50000),('TRX-055','2026-07-15 16:10:28',NULL,NULL,-10000.00,'Cashless',3,150004,1,-10000),('TRX-056','2026-07-15 16:15:39',NULL,NULL,22000.00,'Cashless',3,210006,1,22000),('TRX-057','2026-07-15 16:18:28',NULL,NULL,-8000.00,'Cash',3,210006,1,0),('TRX-058','2026-07-16 03:30:46',NULL,NULL,52000.00,'Cash',3,60001,1,100000),('TRX-059','2026-07-16 03:32:39',NULL,NULL,4000.00,'Cashless',3,60001,1,4000),('TRX-060','2026-07-16 03:34:42',NULL,NULL,18000.00,'Cash',3,90001,1,20000),('TRX-061','2026-07-16 03:39:50',NULL,NULL,4000.00,'Cash',3,60001,1,10000),('TRX-062','2026-07-16 03:41:07',NULL,NULL,17000.00,'Cash',2,60001,1,20000),('TRX-063','2026-07-16 04:42:25',NULL,NULL,41000.00,'Cashless',2,240001,1,41000),('TRX-064','2026-07-16 04:57:17',NULL,NULL,96000.00,'Cash',2,60001,1,100000);
/*!40000 ALTER TABLE `transaksi` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id_user` int NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `nomor_telepon` varchar(20) NOT NULL,
  `gaji` decimal(12,2) DEFAULT NULL,
  `roles_id_role` int NOT NULL,
  `aktif` tinyint(1) DEFAULT '1',
  `created_at` timestamp DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_user`) /*T![clustered_index] CLUSTERED */,
  KEY `users_roles_fk` (`roles_id_role`),
  CONSTRAINT `users_roles_fk` FOREIGN KEY (`roles_id_role`) REFERENCES `roles` (`id_role`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Shabrina','Anggita','shabrina.owner@laundryshabria.com','owner123','081398761001',5000000.00,2,1,'2026-06-23 13:16:41'),(2,'Reza','Pratama','reza.admin@laundryshabria.com','admin123','081398761002',2200000.00,1,1,'2026-06-23 13:16:41'),(3,'Lala','Marlina','lala.admin@laundryshabria.com','admin123','081398761003',2200000.00,1,1,'2026-06-23 13:16:41'),(4,'Doni','Saputro','doni.admin@laundryshabria.com','admin123','081398761004',2200000.00,1,0,'2026-06-23 13:16:41');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-07-16 12:57:23
