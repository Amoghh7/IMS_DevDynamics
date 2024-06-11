import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

root = tk.Tk()
root.title("Inventory Management System")

width = 1024
height = 520
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)
root.config(bg="grey")


# Variables
USERNAME = tk.StringVar()
PASSWORD = tk.StringVar()
PRODUCT_NAME = tk.StringVar()
PRODUCT_PRICE = tk.IntVar()
PRODUCT_QTY = tk.IntVar()
SEARCH = tk.StringVar()

# Inventory data structures
inventory = {}
cart = {}
discount_coupons = {
    1: {"percentage": 20, "max_cap": 150},
    2: {"percentage": 10, "max_cap": 50}
}

# Methods
def Database():
    global conn, cursor
    conn = sqlite3.connect("pythontut.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `admin` (admin_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT, password TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS `product` (product_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, product_name TEXT, product_qty TEXT, product_price TEXT)")
    cursor.execute("SELECT * FROM `admin` WHERE `username` = 'admin' AND `password` = 'admin'")
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO `admin` (username, password) VALUES('admin', 'admin')")
        conn.commit()

def Exit():
    result = messagebox.askquestion('Inventory Management System', 'Are you sure you want to exit?', icon="warning")
    if result == 'yes':
        root.destroy()
        exit()

def Exit2():
    result = messagebox.askquestion('Inventory Management System', 'Are you sure you want to exit?', icon="warning")
    if result == 'yes':
        Home.destroy()
        exit()

def ShowLoginForm():
    global loginform
    loginform = tk.Toplevel()
    loginform.title("Simple Inventory System/Account Login")
    width = 600
    height = 500
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    loginform.resizable(0, 0)
    loginform.geometry("%dx%d+%d+%d" % (width, height, x, y))
    LoginForm()

def LoginForm():
    global lbl_result
    TopLoginForm = tk.Frame(loginform, width=600, height=100, bd=1, relief=tk.SOLID)
    TopLoginForm.pack(side=tk.TOP, pady=20)
    lbl_text = tk.Label(TopLoginForm, text="Administrator Login", font=('arial', 18), width=600)
    lbl_text.pack(fill=tk.X)
    MidLoginForm = tk.Frame(loginform, width=600)
    MidLoginForm.pack(side=tk.TOP, pady=50)
    lbl_username = tk.Label(MidLoginForm, text="Username:", font=('arial', 25), bd=18)
    lbl_username.grid(row=0)
    lbl_password = tk.Label(MidLoginForm, text="Password:", font=('arial', 25), bd=18)
    lbl_password.grid(row=1)
    lbl_result = tk.Label(MidLoginForm, text="", font=('arial', 18))
    lbl_result.grid(row=3, columnspan=2)
    username = tk.Entry(MidLoginForm, textvariable=USERNAME, font=('arial', 25), width=15)
    username.grid(row=0, column=1)
    password = tk.Entry(MidLoginForm, textvariable=PASSWORD, font=('arial', 25), width=15, show="*")
    password.grid(row=1, column=1)
    btn_login = tk.Button(MidLoginForm, text="Login", font=('arial', 18), width=30, command=Login)
    btn_login.grid(row=2, columnspan=2, pady=20)
    btn_login.bind('<Return>', Login)

def Home():
    global Home
    Home = tk.Tk()
    Home.title("Inventory Management System/Home")
    width = 1024
    height = 520
    screen_width = Home.winfo_screenwidth()
    screen_height = Home.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    Home.geometry("%dx%d+%d+%d" % (width, height, x, y))
    Home.resizable(0, 0)
    Title = tk.Frame(Home, bd=1, relief=tk.SOLID)
    Title.pack(pady=10)
    lbl_display = tk.Label(Title, text="Inventory Management System", font=('arial', 45))
    lbl_display.pack()
    menubar = tk.Menu(Home)
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu2 = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="Logout", command=Logout)
    filemenu.add_command(label="Exit", command=Exit2)
    filemenu2.add_command(label="Add new", command=ShowAddNew)
    filemenu2.add_command(label="View", command=ShowView)
    menubar.add_cascade(label="Account", menu=filemenu)
    menubar.add_cascade(label="Inventory", menu=filemenu2)
    Home.config(menu=menubar)
    Home.config(bg="#6666ff")

def ShowAddNew():
    global addnewform
    addnewform = tk.Toplevel()
    addnewform.title("Simple Inventory System/Add new")
    width = 600
    height = 500
    screen_width = Home.winfo_screenwidth()
    screen_height = Home.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    addnewform.geometry("%dx%d+%d+%d" % (width, height, x, y))
    addnewform.resizable(0, 0)
    AddNewForm()

def AddNewForm():
    TopAddNew = tk.Frame(addnewform, width=600, height=100, bd=1, relief=tk.SOLID)
    TopAddNew.pack(side=tk.TOP, pady=20)
    lbl_text = tk.Label(TopAddNew, text="Add New Product", font=('arial', 18), width=600)
    lbl_text.pack(fill=tk.X)
    MidAddNew = tk.Frame(addnewform, width=600)
    MidAddNew.pack(side=tk.TOP, pady=50)
    lbl_productname = tk.Label(MidAddNew, text="Product Name:", font=('arial', 25), bd=10)
    lbl_productname.grid(row=0, sticky=tk.W)
    lbl_qty = tk.Label(MidAddNew, text="Product Quantity:", font=('arial', 25), bd=10)
    lbl_qty.grid(row=1, sticky=tk.W)
    lbl_price = tk.Label(MidAddNew, text="Product Price:", font=('arial', 25), bd=10)
    lbl_price.grid(row=2, sticky=tk.W)
    productname = tk.Entry(MidAddNew, textvariable=PRODUCT_NAME, font=('arial', 25), width=15)
    productname.grid(row=0, column=1)
    productqty = tk.Entry(MidAddNew, textvariable=PRODUCT_QTY, font=('arial', 25), width=15)
    productqty.grid(row=1, column=1)
    productprice = tk.Entry(MidAddNew, textvariable=PRODUCT_PRICE, font=('arial', 25), width=15)
    productprice.grid(row=2, column=1)
    btn_add = tk.Button(MidAddNew, text="Save", font=('arial', 18), width=30, bg="#009ACD", command=AddNew)
    btn_add.grid(row=3, columnspan=2, pady=20)

def AddNew():
    Database()
    cursor.execute("INSERT INTO `product` (product_name, product_qty, product_price) VALUES(?, ?, ?)", (str(PRODUCT_NAME.get()), int(PRODUCT_QTY.get()), int(PRODUCT_PRICE.get())))
    conn.commit()
    cursor.close()
    conn.close()
    PRODUCT_NAME.set("")
    PRODUCT_PRICE.set("")
    PRODUCT_QTY.set("")

def ViewForm():
    global tree
    TopViewForm = tk.Frame(viewform, width=600, bd=1, relief=tk.SOLID)
    TopViewForm.pack(side=tk.TOP, fill=tk.X)
    LeftViewForm = tk.Frame(viewform, width=600)
    LeftViewForm.pack(side=tk.LEFT, fill=tk.Y)
    MidViewForm = tk.Frame(viewform, width=600)
    MidViewForm.pack(side=tk.RIGHT)
    lbl_text = tk.Label(TopViewForm, text="View Products", font=('arial', 18), width=600)
    lbl_text.pack(fill=tk.X)
    lbl_txtsearch = tk.Label(LeftViewForm, text="Search", font=('arial', 15))
    lbl_txtsearch.pack(side=tk.TOP, anchor=tk.W)
    search = tk.Entry(LeftViewForm, textvariable=SEARCH, font=('arial', 15), width=10)
    search.pack(side=tk.TOP,  padx=10, fill=tk.X)
    btn_search = tk.Button(LeftViewForm, text="Search", command=Search)
    btn_search.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X)
    btn_reset = tk.Button(LeftViewForm, text="Reset", command=Reset)
    btn_reset.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X)
    btn_delete = tk.Button(LeftViewForm, text="Delete", command=Delete)
    btn_delete.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X)
    scrollbarx = tk.Scrollbar(MidViewForm, orient=tk.HORIZONTAL)
    scrollbary = tk.Scrollbar(MidViewForm, orient=tk.VERTICAL)
    tree = ttk.Treeview(MidViewForm, columns=("ProductID", "Product Name", "Product Qty", "Product Price"), selectmode="extended", height=100, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=tk.RIGHT, fill=tk.Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=tk.BOTTOM, fill=tk.X)
    tree.heading('ProductID', text="ProductID", anchor=tk.W)
    tree.heading('Product Name', text="Product Name", anchor=tk.W)
    tree.heading('Product Qty', text="Product Qty", anchor=tk.W)
    tree.heading('Product Price', text="Product Price", anchor=tk.W)
    tree.column('#0', stretch=tk.NO, minwidth=0, width=0)
    tree.column('#1', stretch=tk.NO, minwidth=0, width=0)
    tree.column('#2', stretch=tk.NO, minwidth=0, width=200)
    tree.column('#3', stretch=tk.NO, minwidth=0, width=120)
    tree.column('#4', stretch=tk.NO, minwidth=0, width=120)
    tree.pack()
    DisplayData()

def DisplayData():
    Database()
    cursor.execute("SELECT * FROM `product`")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()

def Search():
    if SEARCH.get() != "":
        tree.delete(*tree.get_children())
        Database()
        cursor.execute("SELECT * FROM `product` WHERE `product_name` LIKE ?", ('%'+str(SEARCH.get())+'%',))
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()

def Reset():
    tree.delete(*tree.get_children())
    DisplayData()
    SEARCH.set("")

def Delete():
    if not tree.selection():
        messagebox.showerror("Error", "Please select an item to delete")
    else:
        result = messagebox.askquestion('Simple Inventory System', 'Are you sure you want to delete this record?', icon="warning")
        if result == 'yes':
            curItem = tree.focus()
            contents = (tree.item(curItem))
            selecteditem = contents['values']
            tree.delete(curItem)
            Database()
            cursor.execute("DELETE FROM `product` WHERE `product_id` = ?", (selecteditem[0],))
            conn.commit()
            cursor.close()
            conn.close()

def ShowView():
    global viewform
    viewform = tk.Toplevel()
    viewform.title("Simple Inventory System/View Product")
    width = 600
    height = 400
    screen_width = Home.winfo_screenwidth()
    screen_height = Home.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    viewform.geometry("%dx%d+%d+%d" % (width, height, x, y))
    viewform.resizable(0, 0)
    ViewForm()

def Logout():
    result = messagebox.askquestion('Simple Inventory System', 'Are you sure you want to logout?', icon="warning")
    if result == 'yes':
        global admin_id
        admin_id = ""
        root.deiconify()
        Home.destroy()

def Login(event=None):
    global admin_id
    Database()
    if USERNAME.get() == "" or PASSWORD.get() == "":
        lbl_result.config(text="Please complete the required field!", fg="red")
    else:
        cursor.execute("SELECT * FROM `admin` WHERE `username` = ? AND `password` = ?", (USERNAME.get(), PASSWORD.get()))
        if cursor.fetchone() is not None:
            cursor.execute("SELECT * FROM `admin` WHERE `username` = ? AND `password` = ?", (USERNAME.get(), PASSWORD.get()))
            data = cursor.fetchone()
            admin_id = data[0]
            USERNAME.set("")
            PASSWORD.set("")
            lbl_result.config(text="")
            ShowHome()
        else:
            lbl_result.config(text="Invalid username or password", fg="red")
            USERNAME.set("")
            PASSWORD.set("")
    cursor.close()
    conn.close()

def ShowHome():
    root.withdraw()
    Home()
    loginform.destroy()

# Inventory Management Functions
def AddItemToInventory(productId, quantity):
    if productId in inventory:
        inventory[productId] += quantity
    else:
        inventory[productId] = quantity
    print(f"Added {quantity} of product {productId} to inventory. Total: {inventory[productId]}")

def RemoveItemFromInventory(productId, quantity):
    if productId in inventory and inventory[productId] >= quantity:
        inventory[productId] -= quantity
        print(f"Removed {quantity} of product {productId} from inventory. Remaining: {inventory[productId]}")
    else:
        print(f"Insufficient inventory to remove {quantity} of product {productId}.")

def AddItemToCart(customerId, productId, quantity):
    if productId in inventory and inventory[productId] >= quantity:
        if customerId not in cart:
            cart[customerId] = {}
        if productId in cart[customerId]:
            cart[customerId][productId] += quantity
        else:
            cart[customerId][productId] = quantity
        inventory[productId] -= quantity
        print(f"Added {quantity} of product {productId} to cart for customer {customerId}.")
    else:
        print(f"Insufficient inventory for product {productId}.")

def ApplyDiscountCoupon(cartValue, discountId):
    if discountId in discount_coupons:
        discount = discount_coupons[discountId]
        discount_amount = (discount["percentage"] / 100) * cartValue
        if discount_amount > discount["max_cap"]:
            discount_amount = discount["max_cap"]
        final_price = cartValue - discount_amount
        print(f"Cart value after applying discount: {final_price}")
        return final_price
    else:
        print("Invalid discount coupon.")
        return cartValue

# Driver Function
def main():
    # Demonstrate the flow of the application
    AddItemToInventory(1, 100)
    AddItemToInventory(2, 50)
    AddItemToCart(1, 1, 10)
    AddItemToCart(1, 2, 5)
    cart_value = 1000  # Assume cart value is 1000
    ApplyDiscountCoupon(cart_value, 1)

if __name__ == "__main__":
    main()

# Menubar widgets
menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Account", command=ShowLoginForm)
filemenu.add_command(label="Exit", command=Exit)
menubar.add_cascade(label="File", menu=filemenu)
root.config(menu=menubar)

# Frame
Title = tk.Frame(root, bd=1, relief=tk.SOLID)
Title.pack(pady=10)

# Label widgets
lbl_display = tk.Label(Title, text="Simple Inventory System", font=('arial', 45))
lbl_display.pack()

# Initialization
if __name__ == '__main__':
    root.mainloop()
