import sqlite3
import csv
import random

from interact import *


conn = sqlite3.connect('database.db')

# empty tables
empty_tables()


# populate customers
with open('mock_data/customer_mock_data.csv') as csvfile:
    f = csv.reader(csvfile)
    for row in f:
        insert_customer(*row)

commit()

# populate supplier
with open('mock_data/supplier_mock_data.csv') as csvfile:
    f = csv.reader(csvfile)
    for row in f:
        insert_supplier(*row)

commit()

# populate product
with open('mock_data/product_mock_data.csv') as csvfile:
    f = csv.reader(csvfile)
    for row in f:
        insert_product(*row, random.randint(1, 10), random.randint(1, 100))

commit()

# populate supplierProduct
for productID in range(11):
    for supplierID in range(21):
        insert_supplierProduct(productID, supplierID, random.randint(0, 3))

commit()

close()
