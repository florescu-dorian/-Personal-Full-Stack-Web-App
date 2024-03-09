CREATE TABLE IF NOT EXISTS `nft` (
`nft_id`            int(11)       NOT NULL AUTO_INCREMENT   	COMMENT 'the image id',
`user_id`             int(11)  NOT NULL                	  COMMENT 'the user id',
`description`         varchar(100)  NOT NULL                	  COMMENT 'the image description',
`token`               int(2)  DEFAULT NULL           	      COMMENT 'The token value',
`file_data`                varchar(100)  DEFAULT NULL           	      COMMENT 'The image file data',
PRIMARY KEY  (`nft_id`),
FOREIGN KEY (user_id) REFERENCES users(user_id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT="NFTs";