/*
Authors: Sandeep Batta, Satya Priyanka Ponduru, Vikranth Nallapuneni

Description:
This SQL script creates tables for managing users, products, sales, and tickets, and populates them with data from the customer_support_tickets table.

Tables Created:
1. users - Stores information about users.
2. products - Stores information about products.
3. sales - Stores information about sales transactions.
4. tickets - Stores information about support tickets.

Inserts:
Data from the customer_support_tickets table is inserted into the corresponding tables to populate them.
*/

-- Create the 'ctms' database
-- Sandeep Batta
CREATE DATABASE IF NOT EXISTS ctms;

-- Use the 'ctms' database
-- Sandeep Batta
USE ctms;

-- Create table 'users' to store user information
-- SATYA PRIYANKA PONDURU 
CREATE TABLE users (
	userid INT AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(100) NOT NULL,
	email VARCHAR(100) NOT NULL UNIQUE,
	age INT,
	gender ENUM('Male', 'Female', 'Other')
);
-- Insert unique user information from customer_support_tickets into the 'users' table
-- SATYA PRIYANKA PONDURU
INSERT INTO users (name, email, age, gender)
SELECT DISTINCT `Customer Name`, `Customer Email`, `Customer Age`, `Customer Gender` FROM customer_support_tickets;

-- Create table 'products' to store product information
-- SATYA PRIYANKA PONDURU
CREATE TABLE products (
	productid INT AUTO_INCREMENT PRIMARY KEY,
	product VARCHAR(100) NOT NULL
);

-- Insert unique product information from customer_support_tickets into the 'products' table
-- SATYA PRIYANKA PONDURU
INSERT INTO products (product)
SELECT DISTINCT `Product Purchased` FROM customer_support_tickets;

-- Create table 'sales' to store sales transactions
-- Vikranth Nallapuneni
CREATE TABLE sales (
	saleid INT AUTO_INCREMENT PRIMARY KEY,
	userid INT,
	productid INT,
	date_of_purchase DATE NOT NULL,
	FOREIGN KEY (userid) REFERENCES users(userid),
	FOREIGN KEY (productid) REFERENCES products(productid)
);


-- Insert sales information from customer_support_tickets into the 'sales' table
-- Vikranth Nallapuneni
INSERT INTO sales (userid, productid, date_of_purchase)
SELECT DISTINCT userid, productid, `Date of Purchase` FROM customer_support_tickets csp
JOIN users u ON csp.`Customer Name` = u.name AND csp.`Customer Email` = u.email AND csp.`Customer Age` = u.age AND csp.`Customer Gender` = u.gender
JOIN products p ON csp.`Product Purchased` = p.product;
 


-- Create table 'tickets' to store support tickets
-- Sandeep Batta
CREATE TABLE tickets (
	ticketid INT AUTO_INCREMENT PRIMARY KEY,
	userid INT,
	saleid INT,
	type VARCHAR(100) NOT NULL,
	subject VARCHAR(255) NOT NULL,
	description TEXT NOT NULL,
	create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	status VARCHAR(50) DEFAULT 'Open',
	resolution TEXT,
	priority VARCHAR(50) DEFAULT 'Low',
	channel VARCHAR(50),
	close_time TIMESTAMP,
	customer_satisfaction_rating INT,
	FOREIGN KEY (userid) REFERENCES users(userid),
	FOREIGN KEY (saleid) REFERENCES sales(saleid)
);

-- Insert support ticket information from customer_support_tickets into the 'tickets' table
-- Sandeep Batta
INSERT INTO tickets (userid, saleid, type, subject, description, create_time, status, resolution, priority, channel, close_time, customer_satisfaction_rating)
SELECT DISTINCT
	u.userid,
	s.saleid,
	`Ticket Type`,
	`Ticket Subject`,
	`Ticket Description`,
	`First Response Time`,
	`Ticket Status`,
	`Resolution`,
	`Ticket Priority`,
	`Ticket Channel`,
	`Time to Resolution`,
	`Customer Satisfaction Rating`
FROM customer_support_tickets csp
JOIN users u ON csp.`Customer Name` = u.name AND csp.`Customer Email` = u.email AND csp.`Customer Age` = u.age AND csp.`Customer Gender` = u.gender
JOIN products p ON csp.`Product Purchased` = p.product
JOIN sales s ON csp.`Date of Purchase` = s.date_of_purchase AND u.userid = s.userid AND p.productid = s.productid;
