-- MySQL dump 10.13  Distrib 8.0.40, for Linux (x86_64)
--
-- Host: localhost    Database: shayaDB
-- ------------------------------------------------------
-- Server version	8.0.40-0ubuntu0.24.04.1

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
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categories` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(120) NOT NULL,
  `description` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
INSERT INTO `categories` VALUES (1,'Cafe pergamino seco',''),(2,'Cafe procesado',''),(3,'Otros',''),(4,'Productos rapidos','');
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dry_parchment_coffees`
--

DROP TABLE IF EXISTS `dry_parchment_coffees`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dry_parchment_coffees` (
  `id` int NOT NULL AUTO_INCREMENT,
  `farmer_id` int NOT NULL,
  `variety` varchar(200) NOT NULL,
  `altitude` float NOT NULL,
  `processed` tinyint(1) NOT NULL,
  `price` float NOT NULL,
  `observation` text NOT NULL,
  PRIMARY KEY (`id`),
  KEY `farmer_id` (`farmer_id`),
  CONSTRAINT `dry_parchment_coffees_ibfk_1` FOREIGN KEY (`farmer_id`) REFERENCES `farmers` (`id`) ON DELETE SET DEFAULT
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dry_parchment_coffees`
--

LOCK TABLES `dry_parchment_coffees` WRITE;
/*!40000 ALTER TABLE `dry_parchment_coffees` DISABLE KEYS */;
INSERT INTO `dry_parchment_coffees` VALUES (3,1,'Tipica',1759,1,2140000,'NA'),(4,2,'Caturra',1250,0,2560000,'NA');
/*!40000 ALTER TABLE `dry_parchment_coffees` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `farmers`
--

DROP TABLE IF EXISTS `farmers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `farmers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(120) NOT NULL,
  `location` varchar(120) NOT NULL,
  `farm_name` varchar(120) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `observation` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `farmers`
--

LOCK TABLES `farmers` WRITE;
/*!40000 ALTER TABLE `farmers` DISABLE KEYS */;
INSERT INTO `farmers` VALUES (1,'Juan Pablo Diaz','Somondoco','Los pantanos','3138237896','NA'),(2,'Marco fidel','Richa','Los naranjos','3002119277','NA');
/*!40000 ALTER TABLE `farmers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventories`
--

DROP TABLE IF EXISTS `inventories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventories` (
  `id` int NOT NULL AUTO_INCREMENT,
  `category_id` int NOT NULL,
  `product_id` int NOT NULL,
  `quantity` int NOT NULL,
  `entry_date` datetime NOT NULL,
  `observation` text,
  PRIMARY KEY (`id`),
  KEY `category_id` (`category_id`),
  CONSTRAINT `inventories_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`) ON DELETE SET DEFAULT
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventories`
--

LOCK TABLES `inventories` WRITE;
/*!40000 ALTER TABLE `inventories` DISABLE KEYS */;
INSERT INTO `inventories` VALUES (19,1,3,0,'2025-01-11 17:26:00',''),(24,2,5,5,'2025-01-11 20:55:00','Sábado 11 de enero, 3 moliendas'),(25,2,6,8,'2025-01-11 20:57:00','Sábado 11 de enero, 3 moliendas'),(27,2,8,3,'2025-01-11 21:02:00','Sábado 11 de enero, 3 moliendas, cafe que entra para preparaciones'),(28,1,4,20,'2025-01-11 21:02:00','Café con un poco de pasilla, aromas suaves y buena prueba de calidad'),(29,2,9,13,'2025-01-23 21:43:00','Jueves 23 de enero, 3 moliendas'),(30,2,10,13,'2025-01-23 21:43:00','Jueves 23 de enero, 3 moliendas'),(31,2,11,6,'2025-01-23 21:50:00','Jueves 23 de enero, 3 moliendas'),(32,3,3,0,'2025-01-11 22:08:00',''),(33,3,4,10,'2025-01-12 11:36:00','');
/*!40000 ALTER TABLE `inventories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_details`
--

DROP TABLE IF EXISTS `order_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_details` (
  `id` int NOT NULL AUTO_INCREMENT,
  `product_id` int NOT NULL,
  `category_id` int DEFAULT NULL,
  `order_id` int DEFAULT NULL,
  `unit_price` float NOT NULL,
  `quantity` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `category_id` (`category_id`),
  KEY `order_id` (`order_id`),
  CONSTRAINT `order_details_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`),
  CONSTRAINT `order_details_ibfk_2` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_details`
--

LOCK TABLES `order_details` WRITE;
/*!40000 ALTER TABLE `order_details` DISABLE KEYS */;
INSERT INTO `order_details` VALUES (7,1,4,7,2000,1),(8,5,2,8,32000,10),(9,8,2,9,150000,1),(10,9,2,10,32000,3),(11,10,2,11,32000,3),(12,5,2,12,32000,2),(13,5,2,13,32000,2),(14,9,2,14,32000,4),(15,11,2,15,32000,2);
/*!40000 ALTER TABLE `order_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `id` int NOT NULL AUTO_INCREMENT,
  `sub_total` float NOT NULL,
  `order_date` datetime NOT NULL,
  `observation` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES (7,2000,'2025-01-13 14:31:00',''),(8,320000,'2025-01-13 16:21:00',''),(9,150000,'2025-01-13 16:21:00',''),(10,96000,'2025-01-13 16:21:00',''),(11,96000,'2025-01-13 16:21:00',''),(12,64000,'2025-01-15 16:45:00',''),(13,64000,'2025-01-14 16:45:00',''),(14,128000,'2025-01-15 16:45:00',''),(15,64000,'2025-01-08 16:45:00','');
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `others_in_inventories`
--

DROP TABLE IF EXISTS `others_in_inventories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `others_in_inventories` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(120) NOT NULL,
  `price` float NOT NULL,
  `description` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `others_in_inventories`
--

LOCK TABLES `others_in_inventories` WRITE;
/*!40000 ALTER TABLE `others_in_inventories` DISABLE KEYS */;
INSERT INTO `others_in_inventories` VALUES (3,'Vasos',100,'Vasos'),(4,'Vasos',200,'Vasos');
/*!40000 ALTER TABLE `others_in_inventories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `processed_coffees`
--

DROP TABLE IF EXISTS `processed_coffees`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `processed_coffees` (
  `id` int NOT NULL AUTO_INCREMENT,
  `dry_parchment_coffee_id` int NOT NULL,
  `weight` float NOT NULL,
  `processed_category` varchar(120) NOT NULL,
  `processed_parchment_weight` float NOT NULL,
  `responsible` varchar(120) NOT NULL,
  `price` float NOT NULL,
  `total_price` float NOT NULL,
  PRIMARY KEY (`id`),
  KEY `dry_parchment_coffee_id` (`dry_parchment_coffee_id`),
  CONSTRAINT `processed_coffees_ibfk_1` FOREIGN KEY (`dry_parchment_coffee_id`) REFERENCES `dry_parchment_coffees` (`id`) ON DELETE SET DEFAULT
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `processed_coffees`
--

LOCK TABLES `processed_coffees` WRITE;
/*!40000 ALTER TABLE `processed_coffees` DISABLE KEYS */;
INSERT INTO `processed_coffees` VALUES (5,3,1,'Grano',40,'Lucia Londono',32000,640000),(6,3,0.5,'Grano',10,'Lucia Londono',20000,200000),(8,3,5,'Molido',50,'Lucia Londono',150000,750000),(9,4,1,'Molido',40,'Lucia Londono',32000,640000),(10,4,1,'Molido',40,'Lucia Londono',32000,640000),(11,4,1,'Grano',20,'Lucia Londono',32000,320000);
/*!40000 ALTER TABLE `processed_coffees` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(120) NOT NULL,
  `price` float NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (1,'Cafe',2000),(2,'Aromática',2000),(3,'Capuccino',4000),(4,'Café con leche',2500),(5,'Americano doble',4000);
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(120) NOT NULL,
  `password_hash` varchar(120) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Juan','juan'),(2,'Juan2','juan2');
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

-- Dump completed on 2025-01-16 20:19:55
