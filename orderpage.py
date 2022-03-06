import tkinter as tk

from interact import decrease_stock, list_customers, list_products, list_orders, check_customer_order, check_order_product, insert_order, insert_productOrderLink, commit, increase_product_quantity, get_order_customer, get_products_in_order
from page import Page


class MainOrderPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        p1 = OrderPage(self)
        p2 = OrderViewPage(self)

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="bottom", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = tk.Button(buttonframe, text="Add New Order", command=p1.show)
        b2 = tk.Button(buttonframe, text="View Order Information", command=p2.show)

        b1.pack(side="left")
        b2.pack(side="left")

        p1.show()


class OrderPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        label = tk.Label(self, text="Add New Order")
        label.config(font=("Arial", 40))
        label.grid(row=0, column=0, rowspan=4, columnspan=10)

        tk.Label(self, text="Customer:").grid(row=5, column=0)
        tk.Label(self, text="Product:").grid(row=6, column=0)

        # choose customer
        customers = list_customers()
        self.customer_options = [f'{x[0]} {x[1]} {x[2]}' for x in customers]

        self.customer_var = tk.StringVar()
        self.customer_var.set(self.customer_options[0])

        customer_menu = tk.OptionMenu(self, self.customer_var, *self.customer_options)

        # choose product
        products = list_products()
        self.product_options = [f'{x[0]} {x[1]}' for x in products]

        self.products_vars = []
        self.products_vars.append(tk.StringVar())
        self.products_vars[0].set(self.product_options[0])

        self.quantity_vars = []
        self.quantity_vars.append(tk.StringVar())
        self.quantity_vars[0].set('1')

        # list for all further duplicated widgets to destroy them
        self.choice_widgets = []

        product_menu = tk.OptionMenu(self, self.products_vars[0], *self.product_options)
        product_quantity = tk.Entry(self, textvariable=self.quantity_vars[0])

        # pack it all up
        customer_menu.grid(row=5, column=1)
        product_menu.grid(row=6, column=1)
        product_quantity.grid(row=6, column=2)

        self.current_idx = 0

        # new product button
        pro_btn = tk.Button(self, text='New Product', command=self.new_product)
        pro_btn.grid(row=200, column=0, columnspan=2)

        # button
        sub_btn = tk.Button(self, text='Submit', command=self.submit)
        sub_btn.grid(row=201, column=0, columnspan=2)

    def new_product(self):
        self.current_idx += 1

        # setup everything again
        self.products_vars.append(tk.StringVar())
        self.products_vars[self.current_idx].set(self.product_options[0])
        self.quantity_vars.append(tk.StringVar())
        self.quantity_vars[self.current_idx].set('1')

        product_menu = tk.OptionMenu(self, self.products_vars[self.current_idx], *self.product_options)
        product_quantity = tk.Entry(self, textvariable=self.quantity_vars[self.current_idx])

        product_menu.grid(row=6+self.current_idx, column=1)
        product_quantity.grid(row=6+self.current_idx, column=2)

        self.choice_widgets.append(product_menu)
        self.choice_widgets.append(product_quantity)

    def submit(self):
        customerID = int(self.customer_var.get().split()[0])

        for i in range(self.current_idx + 1):
            productID = int(self.products_vars[i].get().split()[0])
            quantity = int(self.quantity_vars[i].get())

            self.submit_product(customerID, productID, quantity)

        # reset
        self.customer_var.set(self.customer_options[0])
        self.products_vars[0].set(self.product_options[0])
        self.quantity_vars[0].set('1')

        for widget in self.choice_widgets:
            widget.destroy()

    def submit_product(self, customerID, productID, quantity):
        orders = check_customer_order(customerID)

        # if there are no orders, add a new one
        if len(orders) == 0:
            insert_order(customerID)

        cus_order = check_customer_order(customerID)[0][0]

        # check if the product is already in the order
        products = check_order_product(cus_order, productID)

        if len(products) == 0:
            insert_productOrderLink(cus_order, productID, quantity)
        else:
            increase_product_quantity(cus_order, productID, quantity)

        decrease_stock(productID, quantity)
        commit()


class OrderViewPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        title = tk.Label(self, text="View Order")
        title.config(font=("Arial", 40))

        title.grid(row=0, column=0, rowspan=4, columnspan=10)

        # select order
        tk.Label(self, text="Order:").grid(row=4, column=0)
        orders = list_orders()
        self.order_options = [f'{x[0]}' for x in orders]

        self.order_var = tk.StringVar()
        self.order_var.set(self.order_options[0])

        order_menu = tk.OptionMenu(self, self.order_var, *self.order_options)
        order_menu.grid(row=4, column=1)

        self.orderID = int(self.order_var.get())

        # print customer
        tk.Label(self, text="Customer ID:").grid(row=5, column=0)

        customerID = get_order_customer(self.orderID)
        self.customerIDInfo = tk.Label(self, text=customerID)
        self.customerIDInfo.grid(row=5, column=1)

        # print all products in order
        self.product_widgets = []
        self.load_products()

        # button
        sub_btn = tk.Button(self, text='View Customer Information', command=self.submit)
        sub_btn.grid(row=201, column=0, columnspan=2)

    def submit(self):
        for widget in self.product_widgets:
            widget.destroy()

        self.orderID = int(self.order_var.get())
        customerID = get_order_customer(self.orderID)
        self.customerIDInfo.config(text=customerID)

        # print all products in order

        self.load_products()

    def load_products(self):
        self.product_widgets = []

        products = get_products_in_order(self.orderID)

        for i, pr in enumerate(products):
            product, quantity = pr

            pr_name = tk.Label(self, text=product)
            pr_quan = tk.Label(self, text=quantity)

            pr_name.grid(row=6 + i, column=0)
            pr_quan.grid(row=6 + i, column=1)

            self.product_widgets.append(pr_name)
            self.product_widgets.append(pr_quan)