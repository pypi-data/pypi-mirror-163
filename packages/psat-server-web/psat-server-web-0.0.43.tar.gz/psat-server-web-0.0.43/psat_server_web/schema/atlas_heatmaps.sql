-- ATLAS Heatmaps.
-- site = 01a, 02a, 03a, 04a, etc.
-- pixel = 0 to 4095 for a 128x128 pixel mask
drop table if exists `atlas_heatmaps`;

create table `atlas_heatmaps` (
`id` bigint unsigned not null auto_increment,
`site` varchar(10),
`pixel` int unsigned not null,
`ndet` int unsigned not null,
PRIMARY KEY `pk_id` (`id`),
UNIQUE KEY `idx_site_pixel` (`site`, `pixel`)
) ENGINE=MyISAM;
