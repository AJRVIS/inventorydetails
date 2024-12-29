from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Step 1: Initialize the database
DATABASE = 'inventory.db'

def init_db():
    """Initialize the SQLite database."""
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL
        )
    """)
    connection.commit()
    connection.close()

# Initialize the database when the app starts
init_db()

# Step 2: Routes
@app.route('/')
def index():
    """Display all products."""
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    connection.close()
    return render_template('index.html', products=products)

@app.route('/add', methods=['POST'])
def add_product():
    """Add a new product."""
    name = request.form['name']
    quantity = request.form['quantity']
    price = request.form['price']
    if not name or not quantity or not price:
        flash("All fields are required!")
        return redirect(url_for('index'))
    
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO products (name, quantity, price) VALUES (?, ?, ?)", (name, int(quantity), float(price)))
    connection.commit()
    connection.close()
    flash("Product added successfully!")
    return redirect(url_for('index'))

@app.route('/delete/<int:product_id>')
def delete_product(product_id):
    """Delete a product."""
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    connection.commit()
    connection.close()
    flash("Product deleted successfully!")
    return redirect(url_for('index'))

@app.route('/update/<int:product_id>', methods=['POST'])
def update_product(product_id):
    """Update product quantity."""
    quantity = request.form['quantity']
    if not quantity:
        flash("Quantity is required!")
        return redirect(url_for('index'))
    
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("UPDATE products SET quantity = ? WHERE id = ?", (int(quantity), product_id))
    connection.commit()
    connection.close()
    flash("Product updated successfully!")
    return redirect(url_for('index'))

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
