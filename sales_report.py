from connect_mysql import get_connection

def view_all_sales():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT s.id, p.name, s.quantity, s.total_price, s.customer_name, s.date
        FROM sales s
        JOIN products p ON s.product_id = p.id
        ORDER BY s.date DESC
    """)
    
    rows = cursor.fetchall()

    print("\nAll Sales:")
    for row in rows:
        print(f"ID: {row[0]}, Product: {row[1]}, Qty: {row[2]}, Total: ₹{row[3]}, Customer: {row[4]}, Date: {row[5]}")

    cursor.close()
    conn.close()
    
def view_todays_sales():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT s.id, p.name, s.quantity, s.total_price, s.customer_name, s.date
        FROM sales s
        JOIN products p ON s.product_id = p.id
        WHERE DATE(s.date) = CURDATE()
        ORDER BY s.date DESC
    """)

    rows = cursor.fetchall()

    print("\nToday's Sales:")
    if not rows:
        print("No sales recorded today.")
    else:
        for row in rows:
            print(f"ID: {row[0]}, Product: {row[1]}, Qty: {row[2]}, Total: ₹{row[3]}, Customer: {row[4]}, Date: {row[5]}")

    cursor.close()
    conn.close()

def view_total_revenue():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(total_price) FROM sales")
    result = cursor.fetchone()
    total = result[0] if result[0] is not None else 0

    print(f"\nTotal Revenue from All Sales: ₹{total:.2f}")

    cursor.close()
    conn.close()

def view_top_selling_products():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT p.name, SUM(s.quantity) AS total_sold
        FROM sales s
        JOIN products p ON s.product_id = p.id
        GROUP BY s.product_id
        ORDER BY total_sold DESC
        LIMIT 5
    """)

    rows = cursor.fetchall()

    print("\nTop 5 Best-Selling Products:")
    if not rows:
        print("No sales data available.")
    else:
        for name, qty in rows:
            print(f"{name}: {qty} units sold")

    cursor.close()
    conn.close()

