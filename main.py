import tkinter as tk

from customerpage import MainCustomerPage
from orderpage import MainOrderPage
from productpage import MainProductPage
from supplierpage import MainSupplierPage


class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        p1 = MainCustomerPage(self)
        p2 = MainOrderPage(self)
        p3 = MainProductPage(self)
        p4 = MainSupplierPage(self)

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p4.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = tk.Button(buttonframe, text="Customers", command=p1.show)
        b2 = tk.Button(buttonframe, text="Orders", command=p2.show)
        b3 = tk.Button(buttonframe, text="Products", command=p3.show)
        b4 = tk.Button(buttonframe, text="Suppliers", command=p4.show)

        b1.pack(side="left")
        b2.pack(side="left")
        b3.pack(side="left")
        b4.pack(side="left")

        p1.show()


if __name__ == "__main__":
    root = tk.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("1920x1080")
    root.mainloop()
