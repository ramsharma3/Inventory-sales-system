import bcrypt
from connect_mysql import get_connection

def register_user():
    conn = get_connection()
    cursor = conn.cursor()

    username = input("Enter new username: ")
    password = input("Enter new password: ")
    role = input("Enter role (admin/staff): ").lower()

    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", 
                       (username, hashed_pw, role))
        conn.commit()
        print("User registered successfully.")
    except Exception as e:
        print("Error:", e)

    cursor.close()
    conn.close()


def login_user():
    conn = get_connection()
    cursor = conn.cursor()

    username = input("Username: ")
    password = input("Password: ")

    cursor.execute("SELECT password, role FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()

    if result:
        hashed_pw, role = result
        if bcrypt.checkpw(password.encode(), hashed_pw.encode()):
            print(f"Login successful as {role.upper()}")
            return role
        else:
            print("Invalid password.")
    else:
        print("User not found.")

    cursor.close()
    conn.close()
    return None
