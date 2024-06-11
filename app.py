from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Initialize database connection
def Database():
    conn = sqlite3.connect("pythontut.db")
    return conn

@app.route('/inventory', methods=['GET'])
def get_inventory():
    conn = Database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM `product`")
    products = cursor.fetchall()
    conn.close()
    return jsonify(products)

@app.route('/inventory', methods=['POST'])
def add_inventory():
    data = request.json
    conn = Database()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO `product` (product_name, product_qty, product_price) VALUES(?, ?, ?)",
                   (data['product_name'], data['product_qty'], data['product_price']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Product added successfully"}), 201

@app.route('/inventory/<int:product_id>', methods=['DELETE'])
def delete_inventory(product_id):
    conn = Database()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM `product` WHERE `product_id` = ?", (product_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Product deleted successfully"})

@app.route('/cart/<int:customer_id>', methods=['POST'])
def add_to_cart(customer_id):
    data = request.json
    product_id = data['product_id']
    quantity = data['quantity']
    conn = Database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM `product` WHERE `product_id` = ?", (product_id,))
    product = cursor.fetchone()
    if product and product[2] >= quantity:
        cursor.execute("UPDATE `product` SET product_qty = product_qty - ? WHERE product_id = ?", (quantity, product_id))
        cursor.execute("INSERT INTO `cart` (customer_id, product_id, quantity) VALUES (?, ?, ?)",
                       (customer_id, product_id, quantity))
        conn.commit()
        message = f"Added {quantity} of product {product_id} to cart for customer {customer_id}."
    else:
        message = "Insufficient inventory for the requested product."
    conn.close()
    return jsonify({"message": message})

@app.route('/discount', methods=['POST'])
def apply_discount():
    data = request.json
    cart_value = data['cart_value']
    discount_id = data['discount_id']
    discount_coupons = {
        1: {"percentage": 20, "max_cap": 150},
        2: {"percentage": 10, "max_cap": 50}
    }
    if discount_id in discount_coupons:
        discount = discount_coupons[discount_id]
        discount_amount = (discount["percentage"] / 100) * cart_value
        if discount_amount > discount["max_cap"]:
            discount_amount = discount["max_cap"]
        final_price = cart_value - discount_amount
        return jsonify({"cart_value_after_discount": final_price})
    else:
        return jsonify({"message": "Invalid discount coupon."}), 400

if __name__ == '__main__':
    app.run(debug=True)
