import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "SR112@ujjain",
        database = "inventory_db"
    )
    
