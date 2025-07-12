import Product
import sales
import sales_report
import users

def admin_menu():
    while True:
        print("\n=== Inventory Management (Admin) ===")
        print("1. Add Product")
        print("2. View Products")
        print("3. Make a Sale")
        print("4. View All Sales")
        print("5. Update Product")
        print("6. Delete Product")
        print("7. Register New User")
        print("8. View Reports")
        print("9. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            Product.add_product()
        elif choice == "2":
            Product.view_products()
        elif choice == "3":
            sales.make_sale()
        elif choice == "4":
            sales_report.view_all_sales()
        elif choice == "5":
            Product.update_product()
        elif choice == "6":
            Product.delete_product()
        elif choice == "7":
            users.register_user()
        elif choice == "8":
            sales_report.view_todays_sales()
            sales_report.view_total_revenue()
            sales_report.view_top_selling_products()
        elif choice == "9":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


def staff_menu():
    while True:
        print("\n=== Inventory Management (Staff) ===")
        print("1. Add Product")
        print("2. View Products")
        print("3. Make a Sale")
        print("4. View All Sales")
        print("5. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            Product.add_product()
        elif choice == "2":
            Product.view_products()
        elif choice == "3":
            sales.make_sale()
        elif choice == "4":
            sales_report.view_all_sales()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    print("=== Welcome to SISMS ===")
    user_role = users.login_user()

    if not user_role:
        exit(" Exiting. Login required.")

    if user_role == "admin":
        admin_menu()
    else:
        staff_menu()
