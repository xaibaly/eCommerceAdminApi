INSERT INTO products (name, category, price) VALUES 
('Laptop', 'Electronics', 1200.00),
('Phone', 'Electronics', 800.00),
('Desk', 'Furniture', 150.00);

INSERT INTO inventory (product_id, stock_level) VALUES 
(1, 50), (2, 30), (3, 100);

INSERT INTO sales (product_id, quantity, date, revenue) VALUES 
(1, 2, '2025-05-01', 2400.00),
(2, 1, '2025-05-02', 800.00),
(3, 3, '2025-05-03', 450.00);
