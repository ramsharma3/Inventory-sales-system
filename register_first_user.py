import bcrypt
from connect_mysql import get_connection

def register_first_admin():
    conn = get_connection()
    cursor = conn.cursor()

    username = input("Enter new admin username: ")
    password = input("Enter password: ")
    role = "admin"

    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                       (username, hashed_pw, role))
        conn.commit()
        print("Admin registered successfully.")
    except Exception as e:
        print("Error:", e)

    cursor.close()
    conn.close()

register_first_admin()
