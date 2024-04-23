-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: fooddb
-- ------------------------------------------------------
-- Server version	8.0.36

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `height` decimal(5,2) DEFAULT NULL,
  `weight` decimal(5,2) DEFAULT NULL,
  `age` int DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'testor','test@test.com','$pbkdf2-sha256$29000$KOU8ZwzhPGcsxfjfm/OeUw$E7oafe5mPBb69iutfvrdvZTvBtAGtaIvM10d3f5pnUw',66.00,115.00,22,'Male'),(2,'testor2','test2@test.com','$pbkdf2-sha256$29000$urdWSsk5hxBijJHyvndOCQ$uAJvM36mTDC3Fc87Zq8K2YY7CliyDv.2sjjBOmqPmfI',66.00,115.00,22,'Male'),(3,'testor3','test3@test.com','$pbkdf2-sha256$29000$XOt9j/Feq3XO2ds75xzjfA$PUZK5gQhVLaMZuadZRIMq5fNQ6HYyE9vCQPFqp6tAh0',66.00,115.00,22,'Male'),(5,'Presenting','Presenter@fake.com','$pbkdf2-sha256$29000$dk7J.f.f03rPGUOoFcLYew$ez5wAjNIgBPsvJIwkMsEoeJxNiCzivrKVaaCcme0ww8',73.00,167.00,21,'Male'),(6,'Example User','example@example.com','$pbkdf2-sha256$29000$i7HWmpMSAkAIoTTmXOtdKw$zDqvXTCjT1YDd8kR6HqVXLsUwI/CbnfkOfHbyjINROI',66.00,123.00,23,'Female'),(7,'Test Bot','Test@dummy.com','$pbkdf2-sha256$29000$1BqjNEYoBeA8p5SS0vpfaw$h46dHa5w8cfn8e4PIsCs0j9WLSWe8LB0L1VFshCKkwc',71.00,164.00,18,'Male'),(10,'Test User 24','Test24@email.com','$pbkdf2-sha256$29000$KcXY.3/vfe/dGyNEiHHufQ$BvP4osegn.3yhS9TZFh5tNaa0MCWtf68mHRrQimzAz8',71.00,159.00,27,'Male');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-04-22 23:27:33
