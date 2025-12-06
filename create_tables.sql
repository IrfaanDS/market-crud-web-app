-- SQL to create the USERS table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(30) UNIQUE NOT NULL,
    email_address VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(60) NOT NULL,
    budget DECIMAL(10, 2) NOT NULL
);

-- SQL to create the ITEMS table
CREATE TABLE items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(30) UNIQUE NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    barcode VARCHAR(12) UNIQUE NOT NULL,
    description VARCHAR(1024),
    owner INT NULL,
    FOREIGN KEY (owner) REFERENCES users(id)
);