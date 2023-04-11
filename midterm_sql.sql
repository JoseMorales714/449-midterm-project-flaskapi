use 449_midterm;
CREATE TABLE IF NOT EXISTS `users` (
`id` int NOT NULL AUTO_INCREMENT,
`username` varchar(50) NOT NULL,
`password` varchar(255) NOT NULL,
 PRIMARY KEY (`id`)
) ENGINE=InnODB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

