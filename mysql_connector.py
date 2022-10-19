import mysql.connector

conn = mysql.connector.connect(
    host = "localhost",
    user = "user",
    passwd = "password",
    database = "rent_data"
)
sql = conn.cursor()