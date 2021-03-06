import tkinter as tk

from page import Page
from interact import insert_customer, commit, list_customers, get_customer, delete_customer, update_customer


class MainCustomerPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        p1 = CustomerPage(self)
        p2 = CustomerViewPage(self)

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="bottom", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = tk.Button(buttonframe, text="Add New Customer", command=p1.show)
        b2 = tk.Button(buttonframe, text="View Customer Information", command=p2.show)

        b1.pack(side="left")
        b2.pack(side="left")

        p1.show()


class CustomerPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        title = tk.Label(self, text="Add New Customer")
        title.config(font=("Arial", 40))
        title.grid(row=0, column=0, rowspan=4, columnspan=10)

        # input
        self.name_var = tk.StringVar()
        self.address_var = tk.StringVar()
        self.telephone_var = tk.StringVar()
        self.email_var = tk.StringVar()

        tk.Label(self, text='Name').grid(row=5, column=0)
        tk.Label(self, text='Address').grid(row=6, column=0)
        tk.Label(self, text='Telephone No.').grid(row=7, column=0)
        tk.Label(self, text='Email').grid(row=8, column=0)

        name_entry = tk.Entry(self, textvariable=self.name_var)
        address_entry = tk.Entry(self, textvariable=self.address_var)
        telephone_entry = tk.Entry(self, textvariable=self.telephone_var)
        email_entry = tk.Entry(self, textvariable=self.email_var)

        name_entry.grid(row=5, column=1)
        address_entry.grid(row=6, column=1)
        telephone_entry.grid(row=7, column=1)
        email_entry.grid(row=8, column=1)

        # button
        sub_btn = tk.Button(self, text='Submit', command=self.submit)
        sub_btn.grid(row=9, column=0, columnspan=2)

    def submit(self):
        forename, surname = self.name_var.get(), ''
        address = self.address_var.get()
        telephone = self.telephone_var.get()
        email = self.email_var.get()

        name_split = forename.split()
        if len(name_split) > 1:
            forename, surname = ' '.join(name_split[:-1]), name_split[-1]

        insert_customer(surname, forename, address, telephone, email)
        commit()

        # cleanup
        self.name_var.set('')
        self.address_var.set('')
        self.telephone_var.set('')
        self.email_var.set('')


class CustomerViewPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        self.customers = []
        self.customer_options = []

        title = tk.Label(self, text="View Customer")
        title.config(font=("Arial", 40))

        title.grid(row=0, column=0, rowspan=4, columnspan=10)

        # choose customer
        tk.Label(self, text="Customer:").grid(row=4, column=0)

        self.customer_var = tk.StringVar()
        self.reload_customer_list()

        customer_menu = tk.OptionMenu(self, self.customer_var, *self.customer_options)
        customer_menu.grid(row=4, column=1)

        # customer information labels
        tk.Label(self, text="ID:").grid(row=5, column=0)
        tk.Label(self, text="Name:").grid(row=6, column=0)
        tk.Label(self, text="Address:").grid(row=7, column=0)
        tk.Label(self, text="Telephone:").grid(row=8, column=0)
        tk.Label(self, text="Email:").grid(row=9, column=0)

        # grab the customer
        self.customerID = int(self.customer_var.get().split()[0])
        self.customer_info = get_customer(self.customerID)

        self.customer_id_info = tk.Label(self, text=f'{self.customer_info[0]}')

        self.customer_name_var = tk.StringVar()
        self.customer_address_var = tk.StringVar()
        self.customer_phone_var = tk.StringVar()
        self.customer_email_var = tk.StringVar()

        customer_name_info = tk.Entry(self, textvariable=self.customer_name_var)
        self.customer_name_var.set(f'{self.customer_info[2]} {self.customer_info[1]}')
        customer_address_info = tk.Entry(self, textvariable=self.customer_address_var)
        self.customer_address_var.set(f'{self.customer_info[3]}')
        customer_phone_info = tk.Entry(self, textvariable=self.customer_phone_var)
        self.customer_phone_var.set(f'{self.customer_info[4]}')
        customer_email_info = tk.Entry(self, textvariable=self.customer_email_var)
        self.customer_email_var.set(f'{self.customer_info[5]}')

        self.customer_id_info.grid(row=5, column=1)
        customer_name_info.grid(row=6, column=1)
        customer_address_info.grid(row=7, column=1)
        customer_phone_info.grid(row=8, column=1)
        customer_email_info.grid(row=9, column=1)

        # view button
        view_btn = tk.Button(self, text='View Customer Information', command=self.submit)
        view_btn.grid(row=201, column=0, columnspan=2)

        # update button
        upd_btn = tk.Button(self, text='Update Customer', command=self.update)
        upd_btn.grid(row=202, column=0, columnspan=2)

        # delete button
        del_btn = tk.Button(self, text='Delete Customer', command=self.delete)
        del_btn.grid(row=203, column=0, columnspan=2)

    def submit(self):
        self.customerID = int(self.customer_var.get().split()[0])
        self.customer_info = get_customer(self.customerID)

        self.customer_id_info.config(text=f'{self.customer_info[0]}')
        self.customer_name_var.set(f'{self.customer_info[2]} {self.customer_info[1]}')
        self.customer_address_var.set(f'{self.customer_info[3]}')
        self.customer_phone_var.set(f'{self.customer_info[4]}')
        self.customer_email_var.set(f'{self.customer_info[5]}')

    def update(self):
        self.customerID = int(self.customer_var.get().split()[0])

        surname, forename = self.customer_name_var.get().split()
        update_customer(self.customerID, surname, forename, self.customer_address_var.get(), self.customer_phone_var.get(), self.customer_email_var.get())
        commit()

    def delete(self):
        self.customerID = int(self.customer_var.get().split()[0])
        delete_customer(self.customerID)
        commit()

        self.reload_customer_list()

    def reload_customer_list(self):
        self.customers = list_customers()
        self.customer_options = [f'{x[0]} {x[1]}, {x[2]}' for x in self.customers]
        self.customer_var.set(self.customer_options[0])
