from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import requests

app = Flask(__name__)
# Connect to the database
db_config = {
    "host": "localhost", #Change localhost to mysql while deploying and running from docker
    "user": "root",
    "password": "test1234",
    "database": "book_store"
}
@app.route('/')
def index():
    # Get all products from the database
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT id,title,author,price FROM products")
    # Fetch the product data using cursor.fetchall()
    products = cursor.fetchall()
    return render_template("prod_admin.html", products=products)

@app.route('/products')
def main_products():
    key1 = 'bkg'                       # in case running in standalone mode
    # Get the data from the request
    data = request.args                 # comment this code when running in standalone mode
    key1 = data.get('c_name')           # comment this code when running in standalone mode

    print(f'Login Microservice has passed Username {key1} to Product Microservice after successful Login')
    
    # Get all products from the database
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT id,title,author,price FROM products")
    
    # Fetch the product data using cursor.fetchall()
    products = cursor.fetchall()
    
    return render_template('prod_main.html', products=products, key1=key1)

@app.route('/order/<user_name>/<title>/<author>/<price>')
def order(user_name,title,author,price):
    print(f'order_product Method: User: {user_name} Product Title: {title} Author: {author}')
    # Get all products from the database
    data_order = {'user_name': user_name, 'title': title, 'author': author, 'price':price}
    print(f'Order being processed with details Customer {user_name}, Book Title:{title} Book Author:{author} Price of Book: Rs{price}')
    # Send the JSON message to the Checkout microservice to add username, mobile no. and address to order_checkout table
    response = requests.get('http://localhost:5002/', params=data_order)
    print('Order successfully sent to process_order')
    #return 'Order successfully sent to process_order'
    return response.text    

# Route to add/edit products Delete Module if not working
@app.route('/manage_product/<int:id>', methods=['GET', 'POST'])
def manage_product(id):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        price = request.form['price']
        
        if id == 0:
            cursor.execute("INSERT INTO products (title, author, price) VALUES (%s, %s, %s)", (title, author, price))
        else:
            cursor.execute("UPDATE products SET title=%s, author=%s, price=%s WHERE id=%s", (title, author, price, id))
        
        connection.commit()
        cursor.close()
        return redirect('/')
    
    if id == 0:
        return render_template('manage_product.html', product=None)
    else:
        cursor.execute('SELECT * FROM products WHERE id = %s', (id,))
        product = cursor.fetchone()
        cursor.close()
        return render_template('manage_product.html', product=product)


@app.route('/edit_product/<id>', methods=['GET', 'POST'])
def edit_product(id):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        price = request.form['price']

        cursor.execute("UPDATE products SET title=%s, author=%s, price=%s WHERE id=%s", (title, author, price, id))
        connection.commit()
        cursor.close()
        return redirect(url_for('index'))  # Use url_for to generate the correct URL

    cursor.execute('SELECT * FROM products WHERE id = %s', (id,))
    product = cursor.fetchone()
    cursor.close()
    return render_template('edit_product.html', product=product)


@app.route('/delete_product/<id>')
def delete_product(id):
    # Delete the product with the specified ID
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM products WHERE id=%s", (id,))
    connection.commit()

    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5001)

