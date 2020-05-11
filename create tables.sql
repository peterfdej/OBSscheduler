CREATE TABLE `OBSdb`.`host` ( `hostname` VARCHAR(255) NOT NULL , `port` VARCHAR(5) NOT NULL , `pass` VARCHAR(255) NOT NULL ) ENGINE = InnoDB;
ALTER TABLE `host` ADD PRIMARY KEY( `hostname`);
CREATE TABLE `OBSdb`.`scedules` ( `dtime` VARCHAR(14) NOT NULL , `scene` VARCHAR(255) NOT NULL , `transition` VARCHAR(255) NOT NULL , `sourceoff` VARCHAR(255) NOT NULL , `sourceon` VARCHAR(255) NOT NULL , `processed` TINYINT(1) NOT NULL DEFAULT '0' ) ENGINE = InnoDB;
ALTER TABLE `scedules` ADD PRIMARY KEY( `dtime`);
CREATE TABLE `OBSdb`.`scenenames` ( `scene` VARCHAR(255) NOT NULL ) ENGINE = InnoDB;
CREATE TABLE `OBSdb`.`sourcenames` ( `scene` VARCHAR(255) NOT NULL , `source` VARCHAR(255) NOT NULL ) ENGINE = InnoDB;
CREATE TABLE `OBSdb`.`transitionnames` ( `transition` VARCHAR(255) NOT NULL ) ENGINE = InnoDB;