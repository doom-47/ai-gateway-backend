import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Qazx@009",
    database="ai_gateway"
)

print("Connected to MySQL!")
