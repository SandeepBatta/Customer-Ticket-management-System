CREATE TABLE users (
	userid INT AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(100) NOT NULL,
	email VARCHAR(100) NOT NULL UNIQUE,
	age INT,
	gender ENUM('Male', 'Female', 'Other')
);
 
INSERT INTO users (name, email, age, gender)
SELECT DISTINCT `Customer Name`, `Customer Email`, `Customer Age`, `Customer Gender` FROM customer_support_tickets;
 
 
CREATE TABLE products (
	productid INT AUTO_INCREMENT PRIMARY KEY,
	product VARCHAR(100) NOT NULL
);
 
INSERT INTO products (product)
SELECT DISTINCT `Product Purchased` FROM customer_support_tickets;
