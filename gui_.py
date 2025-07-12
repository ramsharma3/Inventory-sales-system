# gui_app.py
import tkinter as tk
from tkinter import messagebox
import bcrypt
from connect_mysql import get_connection
from tkinter import ttk

# === Global Role Variable ===
user_role = None

# === LOGIN ===
def login_user(username, password, root_window):
    global user_role
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password, role FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()

    if result:
        hashed_pw, role = result
        if bcrypt.checkpw(password.encode(), hashed_pw.encode()):
            user_role = role
            messagebox.showinfo("Login", f"Welcome, {username} ({role})!")
            root_window.destroy()
            open_dashboard()
        else:
            messagebox.showerror("Error", "Invalid password.")
    else:
        messagebox.showerror("Error", "User not found.")

    cursor.close()
    conn.close()


def open_login_window():
    root = tk.Tk()
    root.title("Login - SISMS")
    root.geometry("300x200")

    tk.Label(root, text="Username").pack(pady=5)
    entry_username = tk.Entry(root)
    entry_username.pack()

    tk.Label(root, text="Password").pack(pady=5)
    entry_password = tk.Entry(root, show="*")
    entry_password.pack()

    def handle_login():
        uname = entry_username.get()
        pwd = entry_password.get()
        if uname and pwd:
            login_user(uname, pwd, root)
        else:
            messagebox.showwarning("Warning", "All fields are required!")

    tk.Button(root, text="Login", command=handle_login, bg="#007ACC", fg="white").pack(pady=10)
    root.mainloop()


# === DASHBOARD ===
def open_dashboard():
    dash = tk.Tk()
    dash.title("SISMS Dashboard")
    dash.geometry("400x500")

    tk.Label(dash, text=f"Welcome ({user_role.upper()})", font=("Arial", 14)).pack(pady=10)

    tk.Button(dash, text="Add Product", width=25, command=open_add_product_window).pack(pady=5)
    tk.Button(dash, text="Make a Sale", width=25, command=open_make_sale_window).pack(pady=5)
    tk.Button(dash, text="View Reports", width=25, command=open_reports_window).pack(pady=5)
    tk.Button(dash, text="View Products", width=25, command=open_view_products_window).pack(pady=5)

    if user_role == "admin":
        tk.Button(dash, text="Register User", width=25, command=open_register_user_window).pack(pady=5)

    tk.Button(dash, text="Exit", width=25, command=dash.destroy).pack(pady=30)
    dash.mainloop()


# === ADD PRODUCT ===
def open_add_product_window():
    win = tk.Toplevel()
    win.title("Add New Product")
    win.geometry("400x400")

    fields = ["Name", "Brand", "Category", "Price", "Stock", "Min Stock"]
    entries = {}

    for idx, field in enumerate(fields):
        tk.Label(win, text=field).grid(row=idx, column=0, padx=10, pady=5, sticky="w")
        entry = tk.Entry(win)
        entry.grid(row=idx, column=1, padx=10, pady=5)
        entries[field.lower()] = entry

    def save_product():
        try:
            name = entries["name"].get()
            brand = entries["brand"].get()
            category = entries["category"].get()
            price = float(entries["price"].get())
            stock = int(entries["stock"].get())
            min_stock = int(entries["min stock"].get())

            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO products (name, brand, category, price, stock, min_stock)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (name, brand, category, price, stock, min_stock))
            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo("Success", "Product added successfully.")
            win.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to add product.\n{e}")

    tk.Button(win, text="Add Product", command=save_product, bg="#28A745", fg="white").grid(row=len(fields), column=0, columnspan=2, pady=15)


# === MAKE SALE ===
def open_make_sale_window():
    win = tk.Toplevel()
    win.title("Make a Sale")
    win.geometry("400x350")

    tk.Label(win, text="Product ID:").pack(pady=5)
    entry_product_id = tk.Entry(win)
    entry_product_id.pack()

    tk.Label(win, text="Quantity:").pack(pady=5)
    entry_quantity = tk.Entry(win)
    entry_quantity.pack()

    tk.Label(win, text="Customer Name:").pack(pady=5)
    entry_customer = tk.Entry(win)
    entry_customer.pack()

    def make_sale_logic():
        try:
            product_id = int(entry_product_id.get())
            quantity = int(entry_quantity.get())
            customer_name = entry_customer.get()

            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT name, price, stock FROM products WHERE id = %s", (product_id,))
            product = cursor.fetchone()

            if not product:
                messagebox.showerror("Error", "Product not found.")
                return

            name, price, stock = product

            if quantity > stock:
                messagebox.showerror("Error", f"Not enough stock. Available: {stock}")
                return

            total_price = quantity * price

            cursor.execute("""
                INSERT INTO sales (product_id, quantity, total_price, customer_name)
                VALUES (%s, %s, %s, %s)
            """, (product_id, quantity, total_price, customer_name))

            cursor.execute("UPDATE products SET stock = %s WHERE id = %s", (stock - quantity, product_id))
            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo("Success", f"Sold {quantity} x '{name}' to {customer_name}")
            win.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Sale failed.\n{e}")

    tk.Button(win, text="Confirm Sale", command=make_sale_logic, bg="#007ACC", fg="white").pack(pady=15)


# === REPORTS ===
def open_reports_window():
    win = tk.Toplevel()
    win.title("Sales Reports")
    win.geometry("400x300")

    def run_report(query, label):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            output = "\n".join([str(row) for row in result])
            messagebox.showinfo(label, output if output else "No data found.")
            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(win, text="All Sales", width=25, command=lambda: run_report(
        "SELECT * FROM sales ORDER BY date DESC", "All Sales")
    ).pack(pady=5)

    tk.Button(win, text="Today's Sales", width=25, command=lambda: run_report(
        "SELECT * FROM sales WHERE DATE(date) = CURDATE()", "Today's Sales")
    ).pack(pady=5)

    tk.Button(win, text="Total Revenue", width=25, command=lambda: run_report(
        "SELECT SUM(total_price) FROM sales", "Total Revenue")
    ).pack(pady=5)

    tk.Button(win, text="Top Selling Products", width=25, command=lambda: run_report(
        "SELECT product_id, SUM(quantity) as sold FROM sales GROUP BY product_id ORDER BY sold DESC LIMIT 5",
        "Top Selling")
    ).pack(pady=5)


# === REGISTER USER ===
def open_register_user_window():
    win = tk.Toplevel()
    win.title("Register User")
    win.geometry("300x250")

    tk.Label(win, text="Username:").pack(pady=5)
    entry_user = tk.Entry(win)
    entry_user.pack()

    tk.Label(win, text="Password:").pack(pady=5)
    entry_pass = tk.Entry(win, show="*")
    entry_pass.pack()

    tk.Label(win, text="Role (admin/staff):").pack(pady=5)
    entry_role = tk.Entry(win)
    entry_role.pack()

    def register_user():
        username = entry_user.get()
        password = entry_pass.get()
        role = entry_role.get().lower()

        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                           (username, hashed, role))
            conn.commit()
            messagebox.showinfo("Success", "User registered successfully.")
            win.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()
            conn.close()

    tk.Button(win, text="Register", command=register_user, bg="#28A745", fg="white").pack(pady=15)


def open_view_products_window():
    win = tk.Toplevel()
    win.title("View All Products")
    win.geometry("800x400")

    tree = ttk.Treeview(win, columns=("ID", "Name", "Brand", "Category", "Price", "Stock", "Min Stock"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Brand", text="Brand")
    tree.heading("Category", text="Category")
    tree.heading("Price", text="Price")
    tree.heading("Stock", text="Stock")
    tree.heading("Min Stock", text="Min Stock")

    tree.column("ID", width=50)
    tree.column("Name", width=120)
    tree.column("Brand", width=100)
    tree.column("Category", width=100)
    tree.column("Price", width=80)
    tree.column("Stock", width=80)
    tree.column("Min Stock", width=100)

    tree.pack(fill="both", expand=True, padx=10, pady=10)

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, brand, category, price, stock, min_stock FROM products")
        products = cursor.fetchall()

        for row in products:
            tree.insert("", tk.END, values=row)

        cursor.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("Error", str(e))


# === START ===
if __name__ == "__main__":
    open_login_window()
