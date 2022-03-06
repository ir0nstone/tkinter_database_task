import tkinter as tk

from page import Page
from interact import insert_product, commit, list_products, get_product


class MainProductPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        p1 = ProductPage(self)
        p2 = ProductViewPage(self)

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="bottom", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = tk.Button(buttonframe, text="Add New Product", command=p1.show)
        b2 = tk.Button(buttonframe, text="View Products", command=p2.show)

        b1.pack(side="left")
        b2.pack(side="left")

        p1.show()


class ProductPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        title = tk.Label(self, text="Add New Product")
        title.config(font=("Arial", 40))

        # input
        self.name_var = tk.StringVar()
        self.cost_var = tk.StringVar()
        self.stock_var = tk.StringVar()

        name_label = tk.Label(self, text='Name')
        name_entry = tk.Entry(self, textvariable=self.name_var)
        cost_label = tk.Label(self, text='Cost')
        cost_entry = tk.Entry(self, textvariable=self.cost_var)
        stock_label = tk.Label(self, text='Stock')
        stock_entry = tk.Entry(self, textvariable=self.stock_var)

        title.grid(row=0, column=0, rowspan=4, columnspan=10)
        name_label.grid(row=5, column=0)
        name_entry.grid(row=5, column=1)
        cost_label.grid(row=6, column=0)
        cost_entry.grid(row=6, column=1)
        stock_label.grid(row=7, column=0)
        stock_entry.grid(row=7, column=1)

        # button
        sub_btn = tk.Button(self, text='Submit', command=self.submit)
        sub_btn.grid(row=9, column=0, columnspan=2)

    def submit(self):
        name = self.name_var.get()
        cost = int(self.cost_var.get())
        stock = int(self.stock_var.get())

        insert_product(name, cost, stock)
        commit()

        self.name_var.set('')
        self.cost_var.set('')
        self.stock_var.set('')


class ProductViewPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        title = tk.Label(self, text="View Product")
        title.config(font=("Arial", 40))

        title.grid(row=0, column=0, rowspan=4, columnspan=10)

        # choose product
        tk.Label(self, text="Product:").grid(row=4, column=0)
        products = list_products()
        self.product_options = [f'{x[0]} {x[1]}' for x in products]
        self.product_var = tk.StringVar()
        self.product_var.set(self.product_options[0])

        product_menu = tk.OptionMenu(self, self.product_var, *self.product_options)
        product_menu.grid(row=4, column=1)

        # product information labels
        tk.Label(self, text="ID:").grid(row=5, column=0)
        tk.Label(self, text="Name:").grid(row=6, column=0)
        tk.Label(self, text="Cost:").grid(row=7, column=0)
        tk.Label(self, text="Stock:").grid(row=8, column=0)

        # grab product
        self.productID = int(self.product_var.get().split()[0])
        self.product_info = get_product(self.productID)

        self.productIDInfo = tk.Label(self, text=f'{self.product_info[0]}')
        self.productNameInfo = tk.Label(self, text=f'{self.product_info[1]}')
        self.productCostInfo = tk.Label(self, text=f'{self.product_info[2]}')
        self.productStockInfo = tk.Label(self, text=f'{self.product_info[3]}')

        self.productIDInfo.grid(row=5, column=1)
        self.productNameInfo.grid(row=6, column=1)
        self.productCostInfo.grid(row=7, column=1)
        self.productStockInfo.grid(row=8, column=1)

        # button
        sub_btn = tk.Button(self, text='View Customer Information', command=self.submit)
        sub_btn.grid(row=201, column=0, columnspan=2)

    def submit(self):
        self.productID = int(self.product_var.get().split()[0])
        self.product_info = get_product(self.productID)

        self.productIDInfo.config(text=f'{self.product_info[0]}')
        self.productNameInfo.config(text=f'{self.product_info[1]}')
        self.productCostInfo.config(text=f'{self.product_info[2]}')
        self.productStockInfo.config(text=f'{self.product_info[3]}')