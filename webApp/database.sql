CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    firstname VARCHAR(50) NOT NULL,
    lastname VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    companyname VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,  -- Links to the business (user)
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50),
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    age INT CHECK (age >= 0),
    gender ENUM('male', 'female', 'other'),
    location VARCHAR(255),  -- Can store city, state, or country
    loyalty_status ENUM('new', 'regular', 'vip', 'churned') DEFAULT 'new',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

CREATE TABLE Suppliers (
    supplier_id INT AUTO_INCREMENT PRIMARY KEY,
    supplier_name VARCHAR(100) NOT NULL,
    contact_number VARCHAR(15),
    email VARCHAR(100) UNIQUE,
    address TEXT
);

CREATE TABLE Products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    description TEXT,
    category VARCHAR(50),
    stock_quantity INT DEFAULT 0 CHECK (stock_quantity >= 0),
    reorder_level INT DEFAULT 0 CHECK (reorder_level >= 0),
    supplier_id INT,
    price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (supplier_id) REFERENCES Suppliers(supplier_id) ON DELETE SET NULL
);

CREATE TABLE Transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    customer_id INT,
    product_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10,2) NOT NULL CHECK (unit_price >= 0),
    total_amount DECIMAL(10,2) NOT NULL CHECK (total_amount >= 0),
    transaction_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    payment_method ENUM('cash', 'credit', 'debit', 'online') NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id) ON DELETE SET NULL,
    FOREIGN KEY (product_id) REFERENCES Products(product_id) ON DELETE CASCADE
);

CREATE TABLE Returns (
    return_id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    refund_amount DECIMAL(10,2) NOT NULL CHECK (refund_amount >= 0),
    reason TEXT,
    return_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (transaction_id) REFERENCES Transactions(transaction_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES Products(product_id) ON DELETE CASCADE
);

CREATE TABLE Revenue (
    revenue_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    date DATE NOT NULL,
    gross_revenue DECIMAL(15,2) NOT NULL CHECK (gross_revenue >= 0),
    net_revenue DECIMAL(15,2) NOT NULL CHECK (net_revenue >= 0),
    discounts_applied DECIMAL(15,2) DEFAULT 0 CHECK (discounts_applied >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

CREATE TABLE Customer_Segments (
    segment_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    segment_name VARCHAR(50) NOT NULL,  -- e.g., "Frequent Shoppers", "High-Spenders"
    description TEXT,
    customer_count INT DEFAULT 0 CHECK (customer_count >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

CREATE TABLE Customer_CLV (
    clv_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    customer_id INT NOT NULL,
    lifetime_value DECIMAL(15,2) NOT NULL CHECK (lifetime_value >= 0),
    last_purchase_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id) ON DELETE CASCADE
);

CREATE TABLE Sales_Forecasts (
    forecast_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    forecast_period VARCHAR(20) NOT NULL, -- e.g., "Next 3 months"
    predicted_sales DECIMAL(15,2) NOT NULL CHECK (predicted_sales >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

CREATE TABLE Stock_Forecasts (
    stock_forecast_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    forecasted_demand INT NOT NULL CHECK (forecasted_demand >= 0),
    restock_recommendation VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES Products(product_id) ON DELETE CASCADE
);

CREATE TABLE Historical_Trends (
    trend_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    year YEAR NOT NULL,
    total_sales DECIMAL(15,2) NOT NULL CHECK (total_sales >= 0),
    top_category VARCHAR(50),
    campaign_performance JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

CREATE TABLE Sentiment_Analysis (
    sentiment_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    total_reviews INT NOT NULL CHECK (total_reviews >= 0),
    positive_reviews INT NOT NULL CHECK (positive_reviews >= 0),
    neutral_reviews INT NOT NULL CHECK (neutral_reviews >= 0),
    negative_reviews INT NOT NULL CHECK (negative_reviews >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

CREATE TABLE Anomalies (
    anomaly_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    anomaly_type ENUM('sales_spike', 'returns_spike', 'fraudulent_activity') NOT NULL,
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    details TEXT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

CREATE TABLE ESG_Scores (
    esg_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    environmental_score DECIMAL(5,2),
    social_score DECIMAL(5,2),
    governance_score DECIMAL(5,2),
    total_esg_score DECIMAL(5,2) GENERATED ALWAYS AS (
        (environmental_score + social_score + governance_score) / 3
    ) STORED,
    recommendations TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);