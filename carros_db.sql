-- Criando o banco de dados
CREATE DATABASE carros_db;

-- Usando esse banco
USE carros_db;

-- Tabela de carros (dados do jogo)
CREATE TABLE carros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    modelo VARCHAR(100) NOT NULL,
    marca VARCHAR(100) NOT NULL,
    potencia INT NOT NULL,
    ano INT NOT NULL,
    carroceria VARCHAR(50) NOT NULL
);

-- Tabela de jogadores
CREATE TABLE jogadores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    sobrenome VARCHAR(50) NOT NULL,
    usuario VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    pontuacao INT DEFAULT 0
);

-- Tabela de validação (dados reais para IA comparar)
CREATE TABLE validacao (
    id INT AUTO_INCREMENT PRIMARY KEY,
    modelo VARCHAR(100) NOT NULL UNIQUE,
    marca VARCHAR(100) NOT NULL,
    potencia INT NOT NULL,
    ano INT NOT NULL,
    carroceria VARCHAR(50) NOT NULL
);

-- Inserindo exemplos na tabela carros
INSERT INTO carros (modelo, marca, potencia, ano, carroceria) VALUES
('Civic', 'Honda', 155, 2020, 'Sedan'),
('Corolla', 'Toyota', 144, 2019, 'Sedan'),
('Mustang', 'Ford', 450, 2021, 'Coupé'),
('Uno Mille', 'Fiat', 70, 2010, 'Hatch'),
('Gol', 'Volkswagen', 105, 2018, 'Hatch'),
('Onix', 'Chevrolet', 116, 2022, 'Hatch'),
('Ranger', 'Ford', 200, 2021, 'Picape'),
('Hilux', 'Toyota', 204, 2020, 'Picape'),
('Compass', 'Jeep', 178, 2021, 'SUV'),
('Renegade', 'Jeep', 139, 2019, 'SUV'),
('320i', 'BMW', 184, 2022, 'Sedan'),
('A3', 'Audi', 190, 2021, 'Hatch'),
('Celta', 'Chevrolet', 78, 2012, 'Hatch'),
('Sandero', 'Renault', 118, 2019, 'Hatch'),
('T-Cross', 'Volkswagen', 150, 2020, 'SUV'),
('Argo', 'Fiat', 109, 2022, 'Hatch'),
('Cronos', 'Fiat', 130, 2023, 'Sedan'),
('Polo', 'Volkswagen', 128, 2022, 'Hatch'),
('Fox', 'Volkswagen', 104, 2021, 'Hatch'),
('Kwid', 'Renault', 70, 2023, 'Hatch'),
('Creta', 'Hyundai', 166, 2022, 'SUV'),
('HR-V', 'Honda', 173, 2023, 'SUV'),
('Corvette', 'Chevrolet', 495, 2021, 'Coupé'),
('Astra', 'Chevrolet', 140, 2011, 'Hatch'),
('Palio', 'Fiat', 85, 2017, 'Hatch');

-- Inserindo veículos reais na tabela de validacao
INSERT INTO validacao (marca, modelo, ano, potencia, carroceria) VALUES
-- Aqui foram colocados 200 exemplos reais de carros para nossa IA fazer a comparação
-- Listarei os 40 primeiros como exemplo
('Chevrolet', 'Onix', 2022, 116, 'Hatch'),
('Chevrolet', 'Celta', 2012, 78, 'Hatch'),
('Chevrolet', 'Corvette', 2021, 495, 'Coupe'),
('Chevrolet', 'Astra', 2011, 140, 'Hatch'),
('Chevrolet', 'S10', 2023, 206, 'Picape'),
('Fiat', 'Uno mille', 2010, 70, 'Hatch'),
('Fiat', 'Palio', 2017, 85, 'Hatch'),
('Fiat', 'Argo', 2022, 109, 'Hatch'),
('Fiat', 'Cronos', 2023, 130, 'Sedan'),
('Fiat', 'Strada', 2022, 105, 'Picape'),
('Ford', 'Mustang', 2021, 450, 'Coupe'),
('Ford', 'Ranger', 2021, 200, 'Picape'),
('Ford', 'Ka', 2020, 85, 'Hatch'),
('Ford', 'Fusion', 2020, 248, 'Sedan'),
('Ford', 'Ecosport', 2021, 137, 'SUV'),
('Toyota', 'Corolla', 2019, 144, 'Sedan'),
('Toyota', 'Hilux', 2020, 204, 'Picape'),
('Toyota', 'Etios', 2021, 98, 'Hatch'),
('Toyota', 'Yaris', 2022, 106, 'Hatch'),
('Toyota', 'Rav4', 2023, 222, 'SUV'),
('Volkswagen', 'Gol', 2018, 105, 'Hatch'),
('Volkswagen', 'T-cross', 2020, 150, 'SUV'),
('Volkswagen', 'Polo', 2022, 128, 'Hatch'),
('Volkswagen', 'Fox', 2021, 104, 'Hatch'),
('Volkswagen', 'Virtus', 2023, 130, 'Sedan'),
('Honda', 'Civic', 2020, 155, 'Sedan'),
('Honda', 'Hr-v', 2023, 173, 'SUV'),
('Honda', 'Fit', 2020, 116, 'Hatch'),
('Honda', 'City', 2022, 126, 'Sedan'),
('Honda', 'Accord', 2021, 192, 'Sedan'),
('Renault', 'Kwid', 2023, 70, 'Hatch'),
('Renault', 'Sandero', 2019, 118, 'Hatch'),
('Renault', 'Logan', 2021, 115, 'Sedan'),
('Renault', 'Captur', 2022, 170, 'SUV'),
('Renault', 'Duster', 2023, 170, 'SUV'),
('Jeep', 'Compass', 2021, 178, 'SUV'),
('Jeep', 'Renegade', 2019, 139, 'SUV'),
('Jeep', 'Wrangler', 2023, 285, 'SUV'),
('Jeep', 'Gladiator', 2023, 285, 'Picape'),
('Jeep', 'Cherokee', 2022, 271, 'SUV');
