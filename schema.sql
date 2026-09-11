-- Wall Trustworthiness Database Schema
CREATE DATABASE IF NOT EXISTS wall_trust;
USE wall_trust;

CREATE TABLE IF NOT EXISTS walls (
    id INT AUTO_INCREMENT PRIMARY KEY,
    location VARCHAR(255) NOT NULL,
    age FLOAT NOT NULL,
    height FLOAT NOT NULL,
    thickness FLOAT NOT NULL,
    cracks INT NOT NULL,
    dampness INT NOT NULL,
    repairs INT NOT NULL,
    score INT NOT NULL,
    verdict VARCHAR(50) NOT NULL,
    personality VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
