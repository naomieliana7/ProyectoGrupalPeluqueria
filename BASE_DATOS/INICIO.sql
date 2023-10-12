-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema bd_peluqueria
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `bd_peluqueria` ;

-- -----------------------------------------------------
-- Schema bd_peluqueria
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `bd_peluqueria` DEFAULT CHARACTER SET utf8 ;
USE `bd_peluqueria` ;

-- -----------------------------------------------------
-- Table `bd_peluqueria`.`usuario`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bd_peluqueria`.`usuario` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre_peluqueria` VARCHAR(255) NOT NULL,
  `direccion` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bd_peluqueria`.`clientes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bd_peluqueria`.`clientes` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre_apellido` VARCHAR(255) NOT NULL,
  `direccion` VARCHAR(255) NOT NULL,
  `telefono` INT NOT NULL,
  `correo` VARCHAR(45) NOT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  `usuario_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_clientes_usuarios1_idx` (`usuario_id` ASC) VISIBLE,
  CONSTRAINT `fk_clientes_usuarios1`
    FOREIGN KEY (`usuario_id`)
    REFERENCES `bd_peluqueria`.`usuario` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bd_peluqueria`.`empleados`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bd_peluqueria`.`empleados` (
  `id` INT NOT NULL,
  `nombre` VARCHAR(255) NOT NULL,
  `apellido` VARCHAR(255) NOT NULL,
  `telefono` INT NOT NULL,
  `correo` VARCHAR(255) NOT NULL,
  `especialidad` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bd_peluqueria`.`servicios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bd_peluqueria`.`servicios` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre_servicio` VARCHAR(45) NULL,
  `precio` INT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bd_peluqueria`.`reservas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bd_peluqueria`.`reservas` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  `cliente_id` INT NOT NULL,
  `servicio_id` INT NOT NULL,
  `peluquero_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_reservas_clientes_idx` (`cliente_id` ASC) VISIBLE,
  INDEX `fk_reservas_servicios1_idx` (`servicio_id` ASC) VISIBLE,
  INDEX `fk_reservas_peluqueros1_idx` (`peluquero_id` ASC) VISIBLE,
  CONSTRAINT `fk_reservas_clientes`
    FOREIGN KEY (`cliente_id`)
    REFERENCES `bd_peluqueria`.`clientes` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_reservas_servicios1`
    FOREIGN KEY (`servicio_id`)
    REFERENCES `bd_peluqueria`.`servicios` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_reservas_peluqueros1`
    FOREIGN KEY (`peluquero_id`)
    REFERENCES `bd_peluqueria`.`empleados` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bd_peluqueria`.`pagos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bd_peluqueria`.`pagos` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `monto` INT NOT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  `cliente_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_pagos_clientes1_idx` (`cliente_id` ASC) VISIBLE,
  CONSTRAINT `fk_pagos_clientes1`
    FOREIGN KEY (`cliente_id`)
    REFERENCES `bd_peluqueria`.`clientes` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bd_peluqueria`.`peluqueros`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bd_peluqueria`.`peluqueros` (
  `id` INT NOT NULL,
  `nombre_peluquero` VARCHAR(255) NOT NULL,
  `apellido` VARCHAR(255) NOT NULL,
  `correo` VARCHAR(255) NOT NULL,
  `especialidad` VARCHAR(255) NOT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
