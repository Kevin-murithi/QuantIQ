-- Enable strict SQL mode for consistency
SET sql_mode = 'STRICT_ALL_TABLES';

-- Create the database
CREATE DATABASE IF NOT EXISTS quant_iq_saas;
USE quant_iq_saas;

-- Clients Table
CREATE TABLE Clients (
  client_id INT AUTO_INCREMENT PRIMARY KEY,
  firstname VARCHAR(50) NOT NULL,
  lastname VARCHAR(50) NOT NULL,
  email VARCHAR(100) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL,
  companyname VARCHAR(255),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Products Table
CREATE TABLE Products (
  product_id INT AUTO_INCREMENT PRIMARY KEY,
  client_id INT NOT NULL,
  product_name VARCHAR(255) NOT NULL,
  category VARCHAR(100),
  price DECIMAL(10, 2),
  stock_level INT,
  reorder_threshold INT,
  seasonal_indicator BOOLEAN,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (client_id) REFERENCES Clients(client_id) ON DELETE CASCADE
);

-- Sales Table
CREATE TABLE Sales (
  sale_id INT AUTO_INCREMENT PRIMARY KEY,
  client_id INT NOT NULL,
  product_id INT NOT NULL,
  customer_id INT NOT NULL,
  quantity_sold INT,
  sale_datetime DATETIME DEFAULT CURRENT_TIMESTAMP,
  sales_channel ENUM('online', 'in-store'),
  transaction_amount DECIMAL(10, 2),
  FOREIGN KEY (client_id) REFERENCES Clients(client_id) ON DELETE CASCADE,
  FOREIGN KEY (product_id) REFERENCES Products(product_id) ON DELETE CASCADE,
  FOREIGN KEY (customer_id) REFERENCES Customers(customer_id) ON DELETE CASCADE
);

-- Customers Table
CREATE TABLE Customers (
  customer_id INT AUTO_INCREMENT PRIMARY KEY,
  client_id INT NOT NULL,
  first_name VARCHAR(255),
  last_name VARCHAR(255),
  email VARCHAR(100),
  phone VARCHAR(15),
  demographics JSON,
  loyalty_program_status BOOLEAN,
  customer_segment_id INT,
  FOREIGN KEY (client_id) REFERENCES Clients(client_id) ON DELETE CASCADE,
  FOREIGN KEY (customer_segment_id) REFERENCES Customer_Segments(segment_id) ON DELETE SET NULL
);

-- Inventory Table
CREATE TABLE Inventory (
  inventory_id INT AUTO_INCREMENT PRIMARY KEY,
  client_id INT NOT NULL,
  product_id INT NOT NULL,
  stock_level INT,
  reorder_level INT,
  last_restock_date DATETIME,
  FOREIGN KEY (client_id) REFERENCES Clients(client_id) ON DELETE CASCADE,
  FOREIGN KEY (product_id) REFERENCES Products(product_id) ON DELETE CASCADE
);

-- Customer Segments Table
CREATE TABLE Customer_Segments (
  segment_id INT AUTO_INCREMENT PRIMARY KEY,
  client_id INT NOT NULL,
  segment_name VARCHAR(100),
  segmentation_criteria JSON,
  FOREIGN KEY (client_id) REFERENCES Clients(client_id) ON DELETE CASCADE
);

-- Uploaded Files Table
CREATE TABLE Uploaded_Files (
  file_id INT AUTO_INCREMENT PRIMARY KEY,
  client_id INT NOT NULL,
  filename VARCHAR(255),
  upload_datetime DATETIME DEFAULT CURRENT_TIMESTAMP,
  file_type ENUM('CSV', 'Excel'),
  parsing_errors TEXT,
  FOREIGN KEY (client_id) REFERENCES Clients(client_id) ON DELETE CASCADE
);

-- Client Custom Fields Table
CREATE TABLE Client_Custom_Fields (
  custom_field_id INT AUTO_INCREMENT PRIMARY KEY,
  client_id INT NOT NULL,
  table_name VARCHAR(100),
  field_name VARCHAR(100),
  field_type ENUM('VARCHAR', 'INT', 'BOOLEAN', 'DATE', 'DECIMAL', 'TEXT', 'JSON'),
  field_default_value TEXT,
  FOREIGN KEY (client_id) REFERENCES Clients(client_id) ON DELETE CASCADE
);

-- Indexes for optimized queries
CREATE INDEX idx_products_client_id ON Products(client_id);
CREATE INDEX idx_sales_client_id ON Sales(client_id);
CREATE INDEX idx_customers_client_id ON Customers(client_id);
CREATE INDEX idx_inventory_client_id ON Inventory(client_id);
CREATE INDEX idx_uploaded_files_client_id ON Uploaded_Files(client_id);
CREATE INDEX idx_customer_segments_client_id ON Customer_Segments(client_id);