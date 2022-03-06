import tkinter as tk

from page import Page
from interact import insert_supplier, insert_supplierProduct, commit, list_products, get_supplier_id, list_suppliers, get_products_from_supplier, get_supplier, delete_supplier


class MainSupplierPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        p1 = SupplierPage(self)
        p2 = SupplierViewPage(self)

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="bottom", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = tk.Button(buttonframe, text="Add New Supplier", command=p1.show)
        b2 = tk.Button(buttonframe, text="View Supplier Information", command=p2.show)

        b1.pack(side="left")
        b2.pack(side="left")

        p1.show()


class SupplierPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        title = tk.Label(self, text="Add New Supplier")
        title.config(font=("Arial", 40))
        title.grid(row=0, column=0, rowspan=4, columnspan=10)

        # input
        tk.Label(self, text='Name').grid(row=5, column=0)
        tk.Label(self, text='Address').grid(row=6, column=0)
        tk.Label(self, text='Email').grid(row=7, column=0)

        self.name_var = tk.StringVar()
        self.address_var = tk.StringVar()
        self.email_var = tk.StringVar()

        name_entry = tk.Entry(self, textvariable=self.name_var)
        address_entry = tk.Entry(self, textvariable=self.address_var)
        email_entry = tk.Entry(self, textvariable=self.email_var)

        name_entry.grid(row=5, column=1)
        address_entry.grid(row=6, column=1)
        email_entry.grid(row=7, column=1)

        # add products
        product_label = tk.Label(self, text="Products:")
        products = list_products()
        self.product_options = [f'{x[0]} {x[1]}' for x in products]

        self.products_vars = []
        self.products_vars.append(tk.StringVar())
        self.products_vars[0].set(self.product_options[0])

        self.price_vars = []
        self.price_vars.append(tk.StringVar())

        # list for all further duplicated widgets to destroy them
        self.choice_widgets = []

        product_menu = tk.OptionMenu(self, self.products_vars[0], *self.product_options)
        product_price = tk.Entry(self, textvariable=self.price_vars[0])

        product_label.grid(row=5, column=10)
        product_menu.grid(row=6, column=10)
        product_price.grid(row=6, column=11)

        self.current_idx = 0

        # new product button
        pro_btn = tk.Button(self, text='New Product', command=self.new_product)
        pro_btn.grid(row=200, column=10, columnspan=2)

        # button
        sub_btn = tk.Button(self, text='Submit', command=self.submit)
        sub_btn.grid(row=9, column=0, columnspan=2)

    def submit(self):
        name = self.name_var.get()
        address = self.address_var.get()
        email = self.email_var.get()

        insert_supplier(name, address, email)
        commit()

        # deal with supplier products
        supplierID = get_supplier_id(name, address, email)

        ids_done = []

        for i in range(self.current_idx + 1):
            productID = int(self.products_vars[i].get().split()[0])

            if productID in ids_done:
                continue

            ids_done.append(productID)
            price = int(self.price_vars[i].get())

            insert_supplierProduct(productID, supplierID, price)
        commit()

        # reset
        self.name_var.set('')
        self.address_var.set('')
        self.email_var.set('')

        self.products_vars[0].set(self.product_options[0])
        self.price_vars[0].set('')

        for widget in self.choice_widgets:
            widget.destroy()

    def new_product(self):
        self.current_idx += 1

        # setup everything again
        self.products_vars.append(tk.StringVar())
        self.products_vars[self.current_idx].set(self.product_options[0])
        self.price_vars.append(tk.StringVar())

        product_menu = tk.OptionMenu(self, self.products_vars[self.current_idx], *self.product_options)
        product_price = tk.Entry(self, textvariable=self.price_vars[self.current_idx])

        product_menu.grid(row=6+self.current_idx, column=10)
        product_price.grid(row=6+self.current_idx, column=11)

        self.choice_widgets.append(product_menu)
        self.choice_widgets.append(product_price)


class SupplierViewPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        self.products = []
        self.suppliers = []
        self.supplier_options = []

        title = tk.Label(self, text="View Supplier")
        title.config(font=("Arial", 40))

        title.grid(row=0, column=0, rowspan=4, columnspan=10)

        # choose supplier
        tk.Label(self, text="Supplier:").grid(row=4, column=0)

        self.supplier_var = tk.StringVar()
        self.reload_supplier_list()

        supplier_menu = tk.OptionMenu(self, self.supplier_var, *self.supplier_options)
        supplier_menu.grid(row=4, column=1)

        # customer information labels
        tk.Label(self, text="ID:").grid(row=5, column=0)
        tk.Label(self, text="Name:").grid(row=6, column=0)
        tk.Label(self, text="Address:").grid(row=7, column=0)
        tk.Label(self, text="Email:").grid(row=8, column=0)

        # print all products the supplier provides
        self.product_widgets = []

        self.supplierID = int(self.supplier_var.get().split()[0])
        self.supplier_info = get_supplier(self.supplierID)

        self.supplierIDInfo = tk.Label(self, text=f'{self.supplier_info[0]}')
        self.supplierNameInfo = tk.Label(self, text=f'{self.supplier_info[1]}')
        self.supplierAddressInfo = tk.Label(self, text=f'{self.supplier_info[2]}')
        self.supplierEmailInfo = tk.Label(self, text=f'{self.supplier_info[3]}')

        self.supplierIDInfo.grid(row=5, column=1)
        self.supplierNameInfo.grid(row=6, column=1)
        self.supplierAddressInfo.grid(row=7, column=1)
        self.supplierEmailInfo.grid(row=8, column=1)

        self.show_products()

        # button
        sub_btn = tk.Button(self, text='View Supplier Information', command=self.submit)
        sub_btn.grid(row=201, column=0, columnspan=2)

        # delete button
        del_btn = tk.Button(self, text='Delete Supplier', command=self.delete)
        del_btn.grid(row=202, column=0, columnspan=2)

    def submit(self):
        for widget in self.product_widgets:
            widget.destroy()

        self.product_widgets = []

        self.supplierID = int(self.supplier_var.get().split()[0])
        self.supplier_info = get_supplier(self.supplierID)

        self.supplierIDInfo.config(text=f'{self.supplier_info[0]}')
        self.supplierNameInfo.config(text=f'{self.supplier_info[1]}')
        self.supplierAddressInfo.config(text=f'{self.supplier_info[2]}')
        self.supplierEmailInfo.config(text=f'{self.supplier_info[3]}')

        self.show_products()

    def delete(self):
        self.supplierID = int(self.supplier_var.get().split()[0])
        delete_supplier(self.supplierID)
        commit()
        self.reload_supplier_list()

    def show_products(self):
        self.products = get_products_from_supplier(self.supplierID)

        for i, pr in enumerate(self.products):
            name, cost = pr

            pr_name = tk.Label(self, text=name)
            pr_quan = tk.Label(self, text=cost)

            pr_name.grid(row=9 + i, column=0)
            pr_quan.grid(row=9 + i, column=1)

            self.product_widgets.append(pr_name)
            self.product_widgets.append(pr_quan)

    def reload_supplier_list(self):
        self.suppliers = list_suppliers()
        self.supplier_options = [f'{x[0]} {x[1]}' for x in self.suppliers]
        self.supplier_var.set(self.supplier_options[0])
