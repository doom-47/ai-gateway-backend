CREATE TABLE usage_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    model_name VARCHAR(255) NOT NULL,
    input_tokens INT NOT NULL,
    output_tokens INT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
