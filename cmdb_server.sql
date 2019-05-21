-- MySQL dump 10.16  Distrib 10.2.22-MariaDB, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: CMDB
-- ------------------------------------------------------
-- Server version	10.2.22-MariaDB-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `CMDB_Servers`
--

DROP TABLE IF EXISTS `CMDB_Servers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `CMDB_Servers` (
  `host_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `Class` mediumtext DEFAULT NULL,
  `Number` bigint(21) DEFAULT NULL,
  `Name` mediumtext DEFAULT NULL,
  `DeplState` mediumtext DEFAULT NULL,
  `Landscape` mediumtext DEFAULT NULL,
  `PrivateCloud` bigint(21) DEFAULT NULL,
  `_IS` mediumtext DEFAULT NULL,
  `Component` mediumtext DEFAULT NULL,
  `Type` mediumtext DEFAULT NULL,
  `Role` mediumtext DEFAULT NULL,
  `vDCClusName_id` bigint(21) DEFAULT NULL,
  `IP` mediumtext DEFAULT NULL,
  `CPUcount` bigint(21) DEFAULT NULL,
  `RAMcount` bigint(21) DEFAULT NULL,
  `TotalSize` decimal(15,2) DEFAULT NULL,
  `owner` varchar(255) DEFAULT NULL,
  `Link` varchar(101) DEFAULT NULL,
  PRIMARY KEY (`host_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CMDB_Servers`
--

LOCK TABLES `CMDB_Servers` WRITE;
/*!40000 ALTER TABLE `CMDB_Servers` DISABLE KEYS */;
INSERT INTO `CMDB_Servers` VALUES (1,'Server',NULL,'host1',NULL,'PROD',NULL,NULL,NULL,NULL,NULL,NULL,'127.0.0.1',NULL,NULL,NULL,NULL,NULL),(2,'Server',NULL,'host2',NULL,'PROD',NULL,NULL,NULL,NULL,NULL,NULL,'127.0.0.1',NULL,NULL,NULL,NULL,NULL),(3,'Server',NULL,'host3',NULL,'PROD',NULL,NULL,NULL,NULL,NULL,NULL,'127.0.0.1',NULL,NULL,NULL,NULL,NULL),(4,'WS',NULL,'host4',NULL,'PROD',NULL,NULL,NULL,NULL,NULL,NULL,'127.0.0.1',NULL,NULL,NULL,NULL,NULL),(5,'Server',NULL,'host5',NULL,'TEST',NULL,NULL,NULL,NULL,NULL,NULL,'127.0.0.1',NULL,NULL,NULL,NULL,NULL),(6,'VM',NULL,'host6',NULL,'TEST',NULL,NULL,NULL,NULL,NULL,NULL,'127.0.0.1',NULL,NULL,NULL,NULL,NULL),(7,'WS',NULL,'localhost',NULL,'ADMIN',NULL,NULL,NULL,NULL,NULL,NULL,'127.0.0.1',NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `CMDB_Servers` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-05-19 13:07:13