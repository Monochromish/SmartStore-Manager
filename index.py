import tkinter as tk
import mysql.connector


def connect():
    return mysql.connector.connect(
        host="localhost",
        user="your_mysql_username",  # Replace with your MySQL username
        password="your_mysql_password",  # Replace with your MySQL password
        database="your_database_name",  # Replace with your database name
    )


def fetchItems():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    conn.close()
    return items


def updateQuantity(item_id, quantity_change):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE items SET quantity = quantity + (%s) WHERE item_id = (%s)",
        (quantity_change, item_id),
    )
    conn.commit()
    conn.close()


def start():
    root = tk.Tk()
    root.title("SmartStore Manager")

    cart = {}

    def updateBill():
        total = sum(cart[item]["price"] * cart[item]["quantity"] for item in cart)
        bill_label.config(text=f"Total Bill: ${total:.2f}")
        updateCheckout()

    def updateCheckout():
        checkout_items_label.config(
            text="\n".join(
                [f"{cart[item]['name']} (x{cart[item]['quantity']})" for item in cart]
            )
        )

    def addItem(item_id, name, price):
        if item_id not in cart:
            cart[item_id] = {"name": name, "price": price, "quantity": 0}
        cart[item_id]["quantity"] += 1
        updateQuantity(item_id, -1)
        updateBill()
        updateItem()

    def removeItem(item_id):
        if item_id in cart and cart[item_id]["quantity"] > 0:
            cart[item_id]["quantity"] -= 1
            updateQuantity(item_id, 1)
            if cart[item_id]["quantity"] == 0:
                del cart[item_id]
            updateBill()
            updateItem()

    def checkout():
        for item_id in cart:
            updateQuantity(item_id, -cart[item_id]["quantity"])
        cart.clear()
        updateBill()
        updateItem()
        print("Checkout completed")

    def updateItem():
        for item_id, item_frame in item_frames.items():
            current_quantity = fetchQuantity(item_id)
            item_frame["quantity_label"].config(text=f"Quantity: {current_quantity}")
            item_frame["add_button"].config(
                state="normal" if current_quantity > 0 else "disabled"
            )
            item_frame["minus_button"].config(
                state="normal" if item_id in cart else "disabled"
            )

    def fetchQuantity(item_id):
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT quantity FROM items WHERE item_id = %s", (item_id,))
        quantity = cursor.fetchone()[0]
        conn.close()
        return quantity

    items_frame = tk.Frame(root)
    items_frame.pack(side="left", fill="both", expand=True)

    item_frames = {}

    for item in fetchItems():
        item_id, name, price, quantity = item
        item_frame = tk.Frame(items_frame, bd=2, relief="ridge")
        item_frame.pack(padx=10, pady=5, fill="x")

        tk.Label(item_frame, text=name).pack(side="left")
        tk.Label(item_frame, text=f"Price: ${price}").pack(side="left")
        quantity_label = tk.Label(item_frame, text=f"Quantity: {quantity}")
        quantity_label.pack(side="left")

        add_button = tk.Button(
            item_frame,
            text="+",
            command=lambda id=item_id, nm=name, pr=price: addItem(id, nm, pr),
        )
        add_button.pack(side="right")
        minus_button = tk.Button(
            item_frame, text="-", command=lambda id=item_id: removeItem(id)
        )
        minus_button.pack(side="right")

        item_frames[item_id] = {
            "frame": item_frame,
            "quantity_label": quantity_label,
            "add_button": add_button,
            "minus_button": minus_button,
        }

    cart_frame = tk.Frame(root)
    cart_frame.pack(side="right", fill="both", expand=True)

    checkout_items_label = tk.Label(cart_frame, text="", justify="left")
    checkout_items_label.pack()

    bill_label = tk.Label(cart_frame, text="Total Bill: $0.00")
    bill_label.pack()

    checkout_button = tk.Button(cart_frame, text="Checkout", command=checkout)
    checkout_button.pack()

    root.mainloop()


if __name__ == "__main__":
    start()
