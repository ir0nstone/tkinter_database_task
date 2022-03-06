import sqlite3

conn = sqlite3.connect('database.db')

# drop tables
conn.execute('DROP TABLE IF EXISTS customer')
conn.execute('DROP TABLE IF EXISTS supplier')
conn.execute('DROP TABLE IF EXISTS product')
conn.execute('DROP TABLE IF EXISTS customer')
conn.execute('DROP TABLE IF EXISTS orders')
conn.execute('DROP TABLE IF EXISTS productOrderLink')
conn.execute('DROP TABLE IF EXISTS supplierProduct')

conn.commit()

# create customer table
conn.execute('''
    CREATE TABLE customer
    (
        customerID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        surname VARCHAR(30) NOT NULL,
        forename VARCHAR(30) NOT NULL,
        address VARCHAR(250) NOT NULL,
        telephone VARCHAR(20) NOT NULL,
        email VARCHAR(50) NOT NULL
    );
''')

conn.commit()

# create supplier table
conn.execute('''
    CREATE TABLE supplier
    (
        supplierID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        name VARCHAR(30) NOT NULL,
        address VARCHAR(100) NOT NULL,
        email VARCHAR(50) NOT NULL
    );
''')

conn.commit()

# create product table
conn.execute('''
    CREATE TABLE product
    (
        productID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        name VARCHAR(30) NOT NULL,
        cost INTEGER NOT NULL,
        stock INTEGER NOT NULL
    );
''')

conn.commit()

# create order table
conn.execute('''
    CREATE TABLE orders
    (
        orderID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        customerID INTEGER NOT NULL,
        status VARCHAR(30) NOT NULL,

        FOREIGN KEY (customerID) REFERENCES customer(customerID)
    );
''')

conn.commit()

# create productOrderLink table
conn.execute('''
    CREATE TABLE productOrderLink
    (
        orderID INTEGER  NOT NULL,
        productID INTEGER NOT NULL,
        quantity INTEGER NOT NULL,

        FOREIGN KEY (orderID) REFERENCES orders(orderID),
        FOREIGN KEY (productID) REFERENCES product(productID),

        PRIMARY KEY (orderID, productID)
    );
''')

conn.commit()

# create supplierProduct table
conn.execute('''
    CREATE TABLE supplierProduct
    (
        productID INTEGER NOT NULL,
        supplierID INTEGER  NOT NULL,
        cost INTEGER NOT NULL,

        FOREIGN KEY (productID) REFERENCES product(productID),
        FOREIGN KEY (supplierID) REFERENCES supplier(supplierID),

        PRIMARY KEY (productID, supplierID)
    );
''')

conn.commit()
