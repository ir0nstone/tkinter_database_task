import tkinter as tk

from page import Page
from interact import insert_product, commit, list_products, get_product, delete_product, update_product


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

        self.products = []
        self.product_options = []

        title = tk.Label(self, text="View Product")
        title.config(font=("Arial", 40))
        title.grid(row=0, column=0, rowspan=4, columnspan=10)

        # choose product
        tk.Label(self, text="Product:").grid(row=4, column=0)

        self.product_var = tk.StringVar()
        self.reload_product_list()

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

        self.product_name_var = tk.StringVar()
        self.product_cost_var = tk.StringVar()
        self.product_stock_var = tk.StringVar()

        self.product_id_info = tk.Label(self, text=f'{self.product_info[0]}')

        product_name_info = tk.Entry(self, textvariable=self.product_name_var)
        self.product_name_var.set(f'{self.product_info[1]}')
        product_cost_info = tk.Entry(self, textvariable=self.product_cost_var)
        self.product_cost_var.set(f'{self.product_info[2]}')
        product_stock_info = tk.Entry(self, textvariable=self.product_stock_var)
        self.product_stock_var.set(f'{self.product_info[3]}')

        self.product_id_info.grid(row=5, column=1)
        product_name_info.grid(row=6, column=1)
        product_cost_info.grid(row=7, column=1)
        product_stock_info.grid(row=8, column=1)

        # button
        sub_btn = tk.Button(self, text='View Product Information', command=self.submit)
        sub_btn.grid(row=201, column=0, columnspan=2)

        # update button
        upd_btn = tk.Button(self, text='Update Product', command=self.update)
        upd_btn.grid(row=202, column=0, columnspan=2)

        # delete button
        del_btn = tk.Button(self, text='Delete Product', command=self.delete)
        del_btn.grid(row=203, column=0, columnspan=2)

    def submit(self):
        self.productID = int(self.product_var.get().split()[0])
        self.product_info = get_product(self.productID)

        self.product_id_info.config(text=f'{self.product_info[0]}')
        self.product_name_var.set(f'{self.product_info[1]}')
        self.product_cost_var.set(f'{self.product_info[2]}')
        self.product_stock_var.set(f'{self.product_info[3]}')

    def update(self):
        self.productID = int(self.product_var.get().split()[0])

        update_product(self.productID, self.product_name_var.get(), self.product_cost_var.get(), self.product_stock_var.get())
        commit()

    def delete(self):
        self.productID = int(self.product_var.get().split()[0])
        delete_product(self.productID)
        commit()

        self.reload_product_list()
        self.submit()

    def reload_product_list(self):
        self.products = list_products()
        self.product_options = [f'{x[0]} {x[1]}' for x in self.products]
        self.product_var.set(self.product_options[0])
