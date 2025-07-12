from connect_mysql import get_connection

def make_sale():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Step 1: Ask for product ID and quantity sold
        product_id = int(input("Enter Product ID: "))
        quantity = int(input("Enter Quantity Sold: "))

        # Step 2: Fetch product info
        cursor.execute("SELECT name, price, stock FROM products WHERE id = %s", (product_id,))
        product = cursor.fetchone()

        if not product:
            print("Product not found.")
            return

        name, price, stock = product

        # Step 3: Check stock availability
        if quantity > stock:
            print(f"Not enough stock. Only {stock} units available.")
            return

        # Step 4: Calculate total price
        total_price = quantity * price

        # Step 5: Ask for customer name
        customer_name = input("Enter Customer Name: ")

        # Step 6: Insert into sales table
        sale_query = """
        INSERT INTO sales (product_id, quantity, total_price, customer_name)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sale_query, (product_id, quantity, total_price, customer_name))

        # Step 7: Update product stock
        new_stock = stock - quantity
        cursor.execute("UPDATE products SET stock = %s WHERE id = %s", (new_stock, product_id))

        conn.commit()
        print(f"Sale recorded! {quantity} units of '{name}' sold to {customer_name}.")

    except Exception as e:
        print("Error during sale:", e)

    finally:
        cursor.close()
        conn.close()
