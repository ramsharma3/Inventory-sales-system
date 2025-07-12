from connect_mysql import get_connection

def add_product():
    conn = get_connection()
    cursor = conn.cursor()

    name = input("Enter product name: ")
    brand = input("Enter brand: ")
    category = input("Enter category: ")
    price = float(input("Enter price: "))
    stock = int(input("Enter stock quantity: "))
    min_stock = int(input("Enter minimum stock threshold: "))

    query = """
    INSERT INTO products (name, brand, category, price, stock, min_stock)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (name, brand, category, price, stock, min_stock)

    cursor.execute(query, values)
    conn.commit()
    print("Product added successfully.")

    cursor.close()
    conn.close()


def view_products():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()

    print("\n Product List:")
    for row in rows:
        print(row)

    cursor.close()
    conn.close()


def update_product():
    conn = get_connection()
    cursor = conn.cursor()

    pid = int(input("Enter product ID to update: "))
    new_price = float(input("Enter new price: "))
    new_stock = int(input("Enter new stock: "))

    query = "UPDATE products SET price = %s, stock = %s WHERE id = %s"
    cursor.execute(query, (new_price, new_stock, pid))
    conn.commit()

    print(" Product updated successfully.")
    cursor.close()
    conn.close()


def delete_product():
    conn = get_connection()
    cursor = conn.cursor()

    pid = int(input("Enter product ID to delete: "))
    cursor.execute("DELETE FROM products WHERE id = %s", (pid,))
    conn.commit()

    print(" Product deleted successfully.")
    cursor.close()
    conn.close()


def low_stock_alert():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products WHERE stock <= min_stock")
    low_stock = cursor.fetchall()

    print("\n Low Stock Products:")
    for row in low_stock:
        print(row)

    cursor.close()
    conn.close()
