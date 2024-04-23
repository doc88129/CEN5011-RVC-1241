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
-- Table structure for table `message`
--

DROP TABLE IF EXISTS `message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `message` (
  `message_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) DEFAULT NULL,
  `content` text,
  `datetime_posted` datetime DEFAULT CURRENT_TIMESTAMP,
  `title` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`message_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `message`
--

LOCK TABLES `message` WRITE;
/*!40000 ALTER TABLE `message` DISABLE KEYS */;
INSERT INTO `message` VALUES (2,'Example User','Prepare to embark on a culinary journey like no other with this divine recipe for quinoa salad! Picture a vibrant medley of fluffy quinoa grains, tossed with crisp, garden-fresh vegetables, tangy feta cheese, and a zesty homemade vinaigrette. Each bite is a symphony of flavors and textures, with the nutty quinoa perfectly complementing the crunchy vegetables and creamy cheese. But here\'s the best part: not only is this salad absolutely scrumptious, but it\'s also a nutritional powerhouse, packed with protein, fiber, and essential vitamins and minerals. Get ready to tantalize your taste buds and nourish your body with this heavenly quinoa salad sensation!','2024-04-22 12:38:03','Heavenly Quinoa Salad Revelation'),(3,'Example User','Prepare to elevate your breakfast game to new heights with this sensational recipe for avocado toast! Imagine perfectly ripe avocados mashed onto thick slices of artisanal bread, topped with a sprinkle of sea salt, a drizzle of extra virgin olive oil, and a dash of zesty chili flakes. Each bite is a harmonious blend of creamy avocado, crunchy toast, and savory seasonings, creating a symphony of flavors that dance on your palate. But here\'s the best part: not only is this avocado toast absolutely delicious, but it\'s also incredibly nutritious, packed with heart-healthy fats, fiber, and essential nutrients to fuel your day. Get ready to indulge in this avocado toast delight and start your morning off right! Only 370 calories!','2024-04-22 12:38:29','Sensational Avocado Toast Delight'),(4,'Example User','Prepare to satisfy your sweet tooth in the most wholesome and delicious way possible with this tempting recipe for mango coconut chia pudding! Imagine creamy coconut milk infused with sweet, tropical mango puree, mixed with nutritious chia seeds and a hint of vanilla extract. Each spoonful is a symphony of flavors and textures, with the luscious mango perfectly complementing the creamy coconut and the delicate crunch of chia seeds. But here\'s the best part: not only is this chia pudding absolutely decadent, but it\'s also incredibly good for you, packed with fiber, antioxidants, and essential omega-3 fatty acids. Get ready to indulge guilt-free in this mango coconut chia pudding delight and treat yourself to a taste of paradise!','2024-04-22 12:38:52','Tempting Mango Coconut Chia Pudding Delight'),(5,'Test Bot','Prepare to be transported to the sun-kissed shores of the Mediterranean with this exquisite recipe for stuffed peppers! Picture vibrant bell peppers, stuffed to the brim with a flavorful filling of savory ground lamb, fragrant herbs, aromatic spices, and tender pearl couscous. Each bite is a culinary masterpiece, bursting with the rich flavors of the Mediterranean and a tantalizing blend of textures. But here\'s the best part: not only are these stuffed peppers absolutely divine, but they\'re also packed with wholesome ingredients and essential nutrients, making them as nourishing as they are delicious. Get ready to savor every mouthful of this Mediterranean-inspired culinary revelation!','2024-04-22 12:40:27','Exquisite Mediterranean Stuffed Peppers Revelation'),(6,'Test User 24','I just stumbled upon the most mouthwatering recipe for spaghetti and meatballs, and I\'m positively ecstatic to share it! Picture this: perfectly al dente spaghetti noodles cradling succulent, homemade meatballs, all simmered in a rich and flavorful tomato sauce bursting with the essence of ripe tomatoes and aromatic herbs. The best part? It\'s not just delicious; it\'s also incredibly nutritious! With lean ground meat, vibrant vegetables, and whole grain pasta, this dish is a powerhouse of wholesome goodness. I can already imagine the tantalizing aroma wafting through the kitchen as it cooks, and I simply cannot wait to dive into this delectable, guilt-free feast!','2024-04-22 13:07:39','Spaghetti and Meatballs');
/*!40000 ALTER TABLE `message` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-04-22 23:27:32
