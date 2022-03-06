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
        insert_customer(*row, '90')

commit()

# populate supplier
with open('mock_data/supplier_mock_data.csv') as csvfile:
    f = csv.reader(csvfile)
    for row in f:
        insert_supplier(*row, 'yes', 'no')

commit()

# populate product
with open('mock_data/product_mock_data.csv') as csvfile:
    f = csv.reader(csvfile)
    for row in f:
        insert_product(*row, random.randint(1, 10), random.randint(1, 40))

commit()

# populate supplierProduct
for productID in range(11):
    for supplierID in range(21):
        insert_supplierProduct(productID, supplierID, random.randint(0, 3))

commit()

exit(0)
close()



# populate order manually
for _ in range(500):
    insert_order(random.randint(0, 999))      # 1000 customers

commit()

# populate productOrderLink
for _ in range(20):
    insert_productOrderLink(random.randint(0, 9), random.randint(0, 499), random.randint(0, 5))      # 10 products, 500 orders

commit()



commit()

close()
