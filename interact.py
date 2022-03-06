from itertools import product
import sqlite3

conn = sqlite3.connect('database.db')


# basics
def commit():
    conn.commit()


def close():
    conn.close()


# empty tables
def empty_tables():
    conn.execute('DELETE FROM customer')
    conn.execute('DELETE FROM sqlite_sequence WHERE name="customer"')
    conn.execute('DELETE FROM supplier')
    conn.execute('DELETE FROM sqlite_sequence WHERE name="supplier"')
    conn.execute('DELETE FROM product')
    conn.execute('DELETE FROM sqlite_sequence WHERE name="product"')
    conn.execute('DELETE FROM orders')
    conn.execute('DELETE FROM sqlite_sequence WHERE name="orders"')
    conn.execute('DELETE FROM productOrderLink')
    conn.execute('DELETE FROM sqlite_sequence WHERE name="productOrderLink"')
    conn.execute('DELETE FROM supplierProduct')
    conn.execute('DELETE FROM sqlite_sequence WHERE name="supplierProduct"')

    commit()


## insert data
def insert_customer(surname, forename, address, telephone, email):
    conn.execute(f'INSERT INTO customer (surname, forename, address, telephone, email) VALUES (?, ?, ?, ?, ?);',
                 (surname, forename, address, telephone, email))


def insert_supplier(name, address, email):
    conn.execute(f'INSERT INTO supplier (name, address, email) VALUES (?, ?, ?);', (name, address, email))


def insert_product(name, cost, stock):
    conn.execute(f'INSERT INTO product (name, cost, stock) VALUES (?, ?, ?);', (name, cost, stock))


def insert_order(customerID, status='ready'):
    conn.execute(f'INSERT INTO orders (customerID, status) VALUES (?, ?);', (customerID, status))


def insert_productOrderLink(orderID, productID, quantity):
    conn.execute(f'INSERT INTO productOrderLink (orderID, productID, quantity) VALUES (?, ?, ?);',
                 (orderID, productID, quantity))


def insert_supplierProduct(productID, supplierID, cost):
    conn.execute(f'INSERT INTO supplierProduct (productID, supplierID, cost) VALUES (?, ?, ?);',
                 (productID, supplierID, cost))


## update data
def update_product_stock(productID, new_stock):
    conn.execute('UPDATE product SET stock=? WHERE productID=?', (new_stock, productID))


def update_product_quantity(orderID, productID, new_quantity):
    conn.execute('UPDATE productOrderLink SET quantity=? WHERE orderID=? AND productID=?',
                 (new_quantity, orderID, productID))


def decrease_stock(productID, amount):
    new_stock = get_stock(productID) - amount
    update_product_stock(productID, new_stock)


def increase_product_quantity(orderID, productID, amount):
    new_quantity = get_product_quantity(orderID, productID) + amount
    update_product_quantity(orderID, productID, new_quantity)


## list data
def list_customers():
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM customer')
    return cursor.fetchall()


def list_orders():
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM orders')
    return cursor.fetchall()


def list_products():
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM product')
    return cursor.fetchall()


def list_suppliers():
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM supplier')
    return cursor.fetchall()


## extract data
def get_customer(customerID):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM customer WHERE customerID=?', (customerID,))
    return cursor.fetchall()[0]


def get_product(productID):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM product WHERE productID=?', (productID,))
    return cursor.fetchall()[0]


def get_supplier_id(name, address, email):
    cursor = conn.cursor()
    cursor.execute('SELECT supplierID FROM supplier WHERE name=? AND address=? AND email=?', (name, address, email))
    return cursor.fetchall()[0][0]


def get_supplier(supplierID):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM supplier WHERE supplierID=?', (supplierID,))
    return cursor.fetchall()[0]


def get_stock(productID):
    cursor = conn.cursor()
    cursor.execute('SELECT stock FROM product WHERE productID=?', (productID,))
    return cursor.fetchall()[0][0]


def get_order_customer(orderID):
    cursor = conn.cursor()
    cursor.execute('SELECT customerID FROM orders WHERE orderID=?', (orderID,))
    return cursor.fetchall()[0][0]


def get_products_in_order(orderID):
    cursor = conn.cursor()
    cursor.execute('SELECT product.name, quantity FROM product, productOrderLink WHERE product.productID = productOrderLink.productID AND orderID=?', (orderID,))
    return cursor.fetchall()


def get_products_from_supplier(supplierID):
    cursor = conn.cursor()
    cursor.execute('SELECT product.name, supplierProduct.cost FROM product, supplierProduct WHERE product.productID = supplierProduct.productID AND supplierProduct.supplierID=?', (supplierID,))
    return cursor.fetchall()


def get_product_quantity(orderID, productID):
    cursor = conn.cursor()
    cursor.execute('SELECT quantity FROM productOrderLink WHERE orderID=? AND productID=?', (orderID, productID))
    return cursor.fetchall()[0][0]


# check if customer has order
def check_customer_order(customerID):
    cursor = conn.cursor()
    cursor.execute('SELECT orderID FROM orders WHERE customerID=?', (customerID,))
    return cursor.fetchall()


# check if customer's order has a product
def check_order_product(orderID, productID):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productOrderLink WHERE orderID=? AND productID=?;', (orderID, productID))
    return cursor.fetchall()


## update
def update_customer(customerID, surname, forename, address, telephone, email):
    conn.execute('UPDATE customer SET surname=?, forename=?, address=?, telephone=?, email=? WHERE customerID=?', (surname, forename, address, telephone, email, customerID))


## delete
def delete_customer(customerID):
    delete_customer_orders(customerID)
    conn.execute('DELETE FROM customer WHERE customerID=?', (customerID,))

def delete_order(orderID):
    conn.execute('DELETE FROM productOrderLink WHERE orderID=?', (orderID,))
    conn.execute('DELETE FROM orders WHERE orderID=?', (orderID,))

def delete_customer_orders(customerID):
    cursor = conn.cursor()
    cursor.execute('SELECT orderID FROM orders WHERE customerID=?;', (customerID,))
    orders = cursor.fetchall()

    for order in orders:
        delete_order(order[0])

def delete_product(productID):
    conn.execute('DELETE FROM productOrderLink WHERE productID=?', (productID,))
    conn.execute('DELETE FROM supplierProduct WHERE productID=?', (productID,))
    conn.execute('DELETE FROM product WHERE productID=?', (productID,))

def delete_supplier(supplierID):
    conn.execute('DELETE FROM supplierProduct WHERE supplierID=?', (supplierID,))
    conn.execute('DELETE FROM supplier WHERE supplierID=?', (supplierID,))
