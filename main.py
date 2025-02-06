from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from PIL import Image, ImageTk
from datetime import datetime, timedelta
import sqlite3 as sql
import os
from random import randint
from time import strftime

def sql_func():
    global conn, cursor
    conn = sql.connect("tables.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS Cars (Car_Name varchar(45) NOT NULL, Model_Year int DEFAULT NULL, Fuel_Type varchar(45) DEFAULT NULL, Brand_Name varchar(45) DEFAULT NULL, Price int DEFAULT NULL, Seating_Capacity int DEFAULT NULL, Description varchar(500) DEFAULT NULL, Air_Condition varchar(5) DEFAULT NULL, Power_Door_Lock varchar(5) DEFAULT NULL, Crash_Sensor varchar(5) DEFAULT NULL, Power_Window varchar(5) DEFAULT NULL, Leather_Seat varchar(5) DEFAULT NULL,Driver_Airbag varchar(5) DEFAULT NULL, Passenger_Airbag varchar(5) DEFAULT NULL, CD_Player varchar(5) DEFAULT NULL, Antilock varchar(5) DEFAULT NULL, Break_Assit varchar(5) DEFAULT NULL, Status varchar(45) DEFAULT NULL, PRIMARY KEY (Car_Name))")
    cursor.execute("CREATE TABLE IF NOT EXISTS Customers (ID int NOT NULL, Customer_Name varchar(45) DEFAULT NULL,Contact_No bigint DEFAULT NULL, License_No varchar(45) DEFAULT NULL, Address varchar(100) DEFAULT NULL, PRIMARY KEY (ID))")
    cursor.execute("CREATE TABLE IF NOT EXISTS Rented_Cars (Invoice bigint NOT NULL, Car_Name varchar(45) DEFAULT NULL,Contact_No bigint DEFAULT NULL, From_Date varchar(45) DEFAULT NULL, To_Date varchar(45) DEFAULT NULL, Total_Days int DEFAULT NULL, Price bigint DEFAULT NULL, Total_Price bigint DEFAULT NULL, PRIMARY KEY (Invoice))")
    conn.commit()

sql_func()

if not os.path.exists("Booked Cars Details"):
    os.mkdir("Booked Cars Details")

i = 0
def dash_func():
    global main_frame, conn, cursor
    main_frame = Frame(win, borderwidth=3, height=600, width=1049, relief=SUNKEN)
    main_frame.place(x=316, y=90)

    lbl3 = Label(main_frame, text="DASHBOARD", font=("Arial", 20, "bold"))
    lbl3.pack(anchor=NW)

    def slide():
        global i 
        img2 = Image.open(f"/Users/intra/Desktop/Project/Car Rental System/Images/Cars/{lt[i]}")
        img2 = img2.resize((700,450), Image.LANCZOS)
        img2 = ImageTk.PhotoImage(img2)
        img_label.config(image=img2)
        img_label.photo_re = img2
        i += 1
        if i == len(lt):
            i = 0
        img_label.after(3000, slide)
    lt = [f"car{i}.jpg" for i in range(1, 11)]
    img = Image.open(f"/Users/intra/Desktop/Project/Car Rental System/Images/Cars/{lt[0]}")
    img = img.resize((500,500), Image.LANCZOS)
    img = ImageTk.PhotoImage(img)
    img_label = Label(main_frame, image=img)
    img_label.pack(padx=170)
    slide()

    cursor.execute("SELECT Car_Name FROM Cars")
    total_cars = cursor.fetchall()
    totcars_btn = Button(main_frame, text=f"TOTAL CARS=>{len(total_cars)}", font=("Arial", 10, "bold"), width=30, height=5, bg="cyan")
    totcars_btn.pack(side=LEFT, padx=40, pady=10)

    cursor.execute("SELECT Customer_Name FROM Customers")
    total_cus = cursor.fetchall()
    totcus_btn = Button(main_frame, text=f"TOTAL CUSTOMERS=>{len(total_cus)}", font=("Arial", 10, "bold"), width=30, height=5, bg="yellow")
    totcus_btn.pack(side=LEFT, padx=40, pady=10)

    cursor.execute("SELECT Status FROM Cars")
    stats = [i[0] for i in cursor.fetchall()].count("Car Booked")
    totbook_btn = Button(main_frame, text=f"TOTAL CARS BOOKED=>{stats}", font=("Arial", 10, "bold"), width=30, height=5, bg="green")
    totbook_btn.pack(side=LEFT, padx=40, pady=10)

def mancars_func():
    global main_frame, conn, cursor
    main_frame.destroy()
    
    def fetch_data():
        try: 
            cursor.execute("SELECT Car_Name FROM Cars")
            select_combo["values"] = [i[0] for i in cursor.fetchall()]
        except Exception as e:
            messagebox.showerror("ERROR!", f"ERROR: {e}")

    def get_cursor(event=""):
        try:
            cursor.execute("SELECT * FROM Cars WHERE Car_Name=?", (var_select.get(),))
            data = cursor.fetchone()
            if data != None:
                var_carname.set(data[0])
                var_modyear.set(data[1])
                var_fueltype.set(data[2])
                var_brand.set(data[3])
                var_price.set(data[4])
                var_cap.set(data[5])
                desc_entry.delete(1.0, END)
                desc_entry.insert(1.0, data[6])
                var_airc.set(data[7])
                var_pdl.set(data[8])
                var_crsen.set(data[9])
                var_powin.set(data[10])
                var_seat.set(data[11])
                var_airbag.set(data[12])
                var_passbag.set(data[13])
                var_cd.set(data[14])
                var_antilock.set(data[15])
                var_assit.set(data[16])
        except Exception as e:
            messagebox.showerror("ERROR!", f"ERROR: {e}")

    def add_func():
        try:
            if carname_entry.get() == "" or modyear_entry.get() == "" or fueltype_entry.get() == "Select" or brand_entry.get() == "" or price_entry.get() == "" or cap_entry.get() == "":
                messagebox.showerror("ERROR!", "All fields are required!")
            else:
                cursor.execute("INSERT INTO Cars VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Car Not Booked')", (carname_entry.get(), modyear_entry.get(), fueltype_entry.get(), brand_entry.get(), price_entry.get(), cap_entry.get(), desc_entry.get(1.0, END), var_airc.get(), var_pdl.get(), var_crsen.get(), var_powin.get(), var_seat.get(), var_airbag.get(), var_passbag.get(), var_cd.get(), var_antilock.get(), var_assit.get()))
                conn.commit()
                fetch_data()
                reset_func()
                messagebox.showinfo("SUCCESS!", "Car Details Added!")
        except Exception as e:
            messagebox.showerror("ERROR!", f"ERROR: {e}")

    def update_func():
        try:
            if carname_entry.get() == "" or modyear_entry.get() == "" or fueltype_entry.get() == "Select" or brand_entry.get() == "" or price_entry.get() == "" or cap_entry.get() == "":
                messagebox.showerror("ERROR!", "All fields are required!")
            else:
                update = messagebox.askyesno("UPDATE!", "Do you want to update this car details?")
                if update == 1:
                    cursor.execute("UPDATE Cars SET Model_Year=?, Fuel_Type=?, Brand_Name=?, Price=?, Seating_Capacity=?, Description=?, Air_Condition=?, Power_Door_Lock=?, Crash_Sensor=?, Power_Window=?, Leather_Seat=?, Driver_Airbag=?, Passenger_Airbag=?, CD_Player=?, Antilock=?, Break_Assit=? WHERE Car_Name=?", (modyear_entry.get(), fueltype_entry.get(), brand_entry.get(), price_entry.get(), cap_entry.get(), desc_entry.get(1.0, END), var_airc.get(), var_pdl.get(), var_crsen.get(), var_powin.get(), var_seat.get(), var_airbag.get(), var_passbag.get(), var_cd.get(), var_antilock.get(), var_assit.get(), carname_entry.get()))
                    conn.commit()
                    fetch_data()
                    reset_func()
                    messagebox.showinfo("SUCCESS!", "Car Details Updated!")
                else:
                    pass
        except Exception as e:
            messagebox.showerror("ERROR!", f"ERROR: {e}")

    def del_func():
        try:
            if carname_entry.get() == "":
                messagebox.showerror("ERROR!", "Car Name must be required!")
            else:
                delete = messagebox.askyesno("DELETE!", "Do you want to delete this car details?")
                if delete == 1:
                    cursor.execute("DELETE FROM Cars WHERE Car_Name=?", (carname_entry.get(),))
                    conn.commit()
                    fetch_data()
                    reset_func()
                    messagebox.showinfo("SUCCESS!", "Cars Details Deleted!")
                else:
                    pass
        except Exception as e:
            messagebox.showerror("ERROR!", f"ERROR: {e}")

    def reset_func():
        var_select.set("")
        var_carname.set("")
        var_modyear.set("")
        var_fueltype.set("Select")
        var_brand.set("")
        var_price.set("")
        var_cap.set("")
        desc_entry.delete(1.0, END)
        var_airc.set("No")
        var_pdl.set("No")
        var_crsen.set("No")
        var_powin.set("No")
        var_seat.set("No")
        var_airbag.set("No")
        var_passbag.set("No")
        var_cd.set("No")
        var_antilock.set("No")
        var_assit.set("No")

    main_frame = Frame(win, borderwidth=3, height=607, width=1049, relief=SUNKEN)
    main_frame.place(x=316, y=90)

    lbl4 = Label(main_frame, text="MANAGE CAR DETAILS", font=("Arial", 20, "bold"))
    lbl4.place(x=0, y=0)

    var_select = StringVar()
    select_combo = ttk.Combobox(main_frame, font=("Arial", 15, "bold"), textvariable=var_select, state="readonly")
    fetch_data()
    select_combo.place(x=30, y=40)
    select_combo.bind("<<ComboboxSelected>>", get_cursor)

    lbl5 = Label(main_frame, text="To Update, please Select the Car Name from the Listbox", font=("Arial", 15, "bold"))
    lbl5.place(x=300, y=40)

    m_frame = LabelFrame(main_frame, borderwidth=1, height=500, width=900, relief=RIDGE)
    m_frame.place(x=80, y=90)

    var_carname = StringVar()
    carname_lbl = Label(m_frame, text="Car Name", font=("Arial", 15, "bold"))
    carname_lbl.grid(row=0, column=0, padx=10, pady=10, sticky=W)
    carname_entry = Entry(m_frame, textvariable=var_carname, font=("Arial", 15, "bold"))
    carname_entry.grid(row=0, column=1, padx=10, pady=10, sticky=W)
    carname_entry.focus()

    var_modyear = StringVar()
    modyear_lbl = Label(m_frame, text="Model Year", font=("Arial", 15, "bold"))
    modyear_lbl.grid(row=1, column=0, padx=10, pady=10, sticky=W)
    modyear_entry = Entry(m_frame, textvariable=var_modyear, font=("Arial", 15, "bold"))
    modyear_entry.grid(row=1, column=1, padx=10, pady=10, sticky=W)

    var_fueltype = StringVar()
    fueltype_lbl = Label(m_frame, text="Fuel Type", font=("Arial", 15, "bold"))
    fueltype_lbl.grid(row=2, column=0, padx=10, pady=10, sticky=W)
    fueltype_entry = ttk.Combobox(m_frame, textvariable=var_fueltype, font=("Arial", 15, "bold"), state="readonly")
    fueltype_entry["values"] = ("Select", "Petrol", "Diesel")
    fueltype_entry.current(0)
    fueltype_entry.grid(row=2, column=1, padx=10, pady=10, sticky=W)

    var_brand = StringVar()
    brand_lbl = Label(m_frame, text="Brand Name", font=("Arial", 15, "bold"))
    brand_lbl.grid(row=0, column=2, padx=10, pady=10, sticky=W)
    brand_entry = Entry(m_frame, textvariable=var_brand, font=("Arial", 15, "bold"))
    brand_entry.grid(row=0, column=3, padx=10, pady=10, sticky=W)

    var_price = StringVar()
    price_lbl = Label(m_frame, text="Price Per Day (in INR)", font=("Arial", 15, "bold"))
    price_lbl.grid(row=1, column=2, padx=10, pady=10, sticky=W)
    price_entry = Entry(m_frame, textvariable=var_price, font=("Arial", 15, "bold"))
    price_entry.grid(row=1, column=3, padx=10, pady=10, sticky=W)

    var_cap = StringVar()
    cap_lbl = Label(m_frame, text="Seating Capacity", font=("Arial", 15, "bold"))
    cap_lbl.grid(row=2, column=2, padx=10, pady=10, sticky=W)
    cap_entry = Entry(m_frame, textvariable=var_cap, font=("Arial", 15, "bold"))
    cap_entry.grid(row=2, column=3, padx=10, pady=10, sticky=W)

    desc_lbl = Label(m_frame, text="Description", font=("Arial", 15, "bold"))
    desc_lbl.grid(row=3, column=0, padx=10, pady=10, sticky=N)
    desc_entry = Text(m_frame, width=65, height=7, font=("Arial", 15, "bold"))
    desc_entry.grid(row=3, column=1, padx=10, pady=10, sticky=W, columnspan=3)

    acc_lbl = Label(m_frame, text="Accessories", font=("Arial", 15, "bold"))
    acc_lbl.grid(row=4, column=0, padx=10, pady=10, sticky=N)
    acc_frame = LabelFrame(m_frame, borderwidth=1, height=200, width=720, relief=RIDGE)
    acc_frame.grid(row=4, column=1, padx=10, pady=10, sticky=W, columnspan=3)

    var_airc = StringVar()
    airc_btn = Checkbutton(acc_frame, text="Air Conditioner", variable=var_airc, font=("Arial", 12, "bold"), onvalue="Yes", offvalue="No")
    airc_btn.grid(row=0, column=0, sticky=W)
    var_airc.set("No")

    var_pdl = StringVar()
    pdl_btn = Checkbutton(acc_frame, text="Power Door Lock", variable=var_pdl, font=("Arial", 12, "bold"), onvalue="Yes", offvalue="No")
    pdl_btn.grid(row=0, column=1, sticky=W)
    var_pdl.set("No")

    var_crsen = StringVar()
    crsen_btn = Checkbutton(acc_frame, text="Crash Sensor", variable=var_crsen, font=("Arial", 12, "bold"), onvalue="Yes", offvalue="No")
    crsen_btn.grid(row=0, column=2, sticky=W)
    var_crsen.set("No")

    var_powin = StringVar()
    powin_btn = Checkbutton(acc_frame, text="Power Window", variable=var_powin, font=("Arial", 12, "bold"), onvalue="Yes", offvalue="No")
    powin_btn.grid(row=0, column=3, sticky=W)
    var_powin.set("No")

    var_seat = StringVar()
    seat_btn = Checkbutton(acc_frame, text="Leather Seat", variable=var_seat, font=("Arial", 12, "bold"), onvalue="Yes", offvalue="No")
    seat_btn.grid(row=0, column=4, sticky=W)
    var_seat.set("No")

    var_airbag = StringVar()
    airbag_btn = Checkbutton(acc_frame, text="Driver Airbag", variable=var_airbag, font=("Arial", 12, "bold"), onvalue="Yes", offvalue="No")
    airbag_btn.grid(row=1, column=0, sticky=W)
    var_airbag.set("No")

    var_passbag = StringVar()
    passbag_btn = Checkbutton(acc_frame, text="Passsenger Airbag", variable=var_passbag, font=("Arial", 12, "bold"), onvalue="Yes", offvalue="No")
    passbag_btn.grid(row=1, column=1, sticky=W)
    var_passbag.set("No")

    var_cd = StringVar()
    cd_btn = Checkbutton(acc_frame, text="CD Player", variable=var_cd, font=("Arial", 12, "bold"), onvalue="Yes", offvalue="No")
    cd_btn.grid(row=1, column=2, sticky=W)
    var_cd.set("No")

    var_antilock = StringVar()
    antilock_btn = Checkbutton(acc_frame, text="Antilock", variable=var_antilock, font=("Arial", 12, "bold"), onvalue="Yes", offvalue="No")
    antilock_btn.grid(row=1, column=3, sticky=W)
    var_antilock.set("No")

    var_assit = StringVar()
    assit_btn = Checkbutton(acc_frame, text="Break Assit", variable=var_assit, font=("Arial", 12, "bold"), onvalue="Yes", offvalue="No")
    assit_btn.grid(row=1, column=4, sticky=W)
    var_assit.set("No")

    btn_frame = LabelFrame(m_frame, borderwidth=1, height=100, width=720, relief=RIDGE, bg="purple")
    btn_frame.grid(row=5, column=1, padx=120, pady=10, sticky=W, columnspan=4)

    add_btn = Button(btn_frame, text="ADD", font=("Arial", 15, "bold"), command=add_func, bg="blue")
    add_btn.grid(row=0, column=0, padx=10, pady=10, sticky=W)

    update_btn = Button(btn_frame, text="UPDATE", font=("Arial", 15, "bold"), command=update_func, bg="green")
    update_btn.grid(row=0, column=1, padx=10, pady=10, sticky=W)

    del_btn = Button(btn_frame, text="DELETE", font=("Arial", 15, "bold"), command=del_func, bg="red")
    del_btn.grid(row=0, column=2, padx=10, pady=10, sticky=W)

    clear_btn = Button(btn_frame, text="CLEAR", font=("Arial", 15, "bold"), command=reset_func, bg="cyan")
    clear_btn.grid(row=0, column=3, padx=10, pady=10, sticky=W)

def mancus_func():
    global main_frame, conn, cursor 
    main_frame.destroy()

    def fetch_data():
        try:
            cursor.execute("SELECT * FROM Customers")
            data = cursor.fetchall()
            if len(data) != 0:
                customer_table.delete(*customer_table.get_children())
                for n, i in enumerate(data):
                    if n % 2 == 0:
                        customer_table.insert("", END, values=i, tags=("evenrow", ))
                    else:
                        customer_table.insert("", END, values=i, tags=("oddrow", ))
                conn.commit()
            else:
                for item in customer_table.get_children():
                    customer_table.delete(item) 
        except Exception as e:
            messagebox.showerror("ERROR!", f"ERROR: {e}")

    def get_cursor(event=""):
        try:
            cursor_focus = customer_table.focus()
            content = customer_table.item(cursor_focus)
            data = content["values"]
            if len(data) > 0:
                var_id.set(data[0])
                var_cusname.set(data[1]) 
                var_contact.set(data[2]) 
                var_lic.set(data[3]) 
                address_entry.delete(1.0, END)
                address_entry.insert(1.0, data[4])
        except Exception as e:
            messagebox.showerror("ERROR!", f"ERROR: {e}")

    def add_func():
        try:
            if var_cusname.get() == "" or var_contact.get() == "" or var_lic.get() == "" or len(address_entry.get(1.0, END)) <= 1:
                messagebox.showerror("ERROR!", "All fields are required!")
            else:
                if int(address_entry.index(END).split('.')[0]) - 1 <= 3:
                    cursor.execute("INSERT INTO Customers VALUES(?, ?, ?, ?, ?)", (var_id.get(), var_cusname.get(), var_contact.get(), var_lic.get(), address_entry.get(1.0, END)))
                    conn.commit()
                    fetch_data()
                    reset_func()
                    messagebox.showinfo("SUCCESS!", "Customer Details Added!")
                else:  
                    messagebox.showerror("ERROR!", "Only 3 Lines Required For Address!")  
        except Exception as e:
            messagebox.showerror("ERROR!", f"ERROR: {e}")

    def update_func():
        try:
            if var_cusname.get() == "" or var_contact.get() == "" or var_lic.get() == "" or len(address_entry.get(1.0, END)) <=1:
                messagebox.showerror("ERROR!", "All fields are required!")
            else:
                update = messagebox.askyesno("UPDATE!", "Do you want to update customer car details?")
                if update == 1:
                    if int(address_entry.index(END).split('.')[0]) - 1 <= 3:
                        cursor.execute("UPDATE Customers SET Customer_Name=?, Contact_No=?, License_No=?, Address=? WHERE ID=?", (var_cusname.get(), var_contact.get(), var_lic.get(), address_entry.get(1.0, END), var_id.get()))
                        conn.commit()
                        fetch_data()
                        reset_func()
                        messagebox.showinfo("SUCCESS!", "Customer Details Updated!")
                    else:
                        messagebox.showerror("ERROR!", "Only 3 Lines Required For Address!")
                else:
                    pass
        except Exception as e:
            messagebox.showerror("ERROR!", f"ERROR: {e}")

    def del_func():
        try:
            if var_id.get() == "":
                messagebox.showerror("ERROR!", "Customer ID must be required!")
            else:
                delete = messagebox.askyesno("DELETE!", "Do you want to delete this customer details?")
                if delete == 1:
                    cursor.execute("DELETE FROM Customers WHERE ID=?", (var_id.get(),))
                    conn.commit()
                    fetch_data()
                    reset_func()
                    messagebox.showinfo("SUCCESS!", "Customer Details Deleted!")
                else:
                    pass
        except Exception as e:
            messagebox.showerror("ERROR!", f"ERROR: {e}")

    def reset_func():
        var_id.set("")
        var_cusname.set("")
        var_contact.set("")
        var_lic.set("")
        address_entry.delete(1.0, END)

    def search_data():
        try:
            if var_by.get() == "Select" or box_entry.get() == "":
                messagebox.showerror("ERROR!", "Entry Field Required!")
            else:
                cursor.execute(f'SELECT * FROM Customers WHERE {var_by.get()}="{box_entry.get()}"')
                data = cursor.fetchall()
                if len(data) != 0:
                    customer_table.delete(*customer_table.get_children())
                    for n, i in enumerate(data):
                        if n % 2 == 0:
                            customer_table.insert("", END, values=i, tags=("evenrow", ))
                        else:
                            customer_table.insert("", END, values=i, tags=("oddrow", ))
                else:
                    for item in customer_table.get_children():
                        customer_table.delete(item) 
                conn.commit()
        except Exception as e:
            messagebox.showerror("ERROR!", f"ERROR: {e}")

    main_frame = Frame(win, borderwidth=3, height=607, width=1049, relief=SUNKEN)
    main_frame.place(x=316, y=90)

    lbl5 = Label(main_frame, text="MANAGE CUSTOMER DETAILS", font=("Arial", 20, "bold"))
    lbl5.place(x=0, y=0)

    m_frame = LabelFrame(main_frame, borderwidth=1, height=400, width=900, relief=RIDGE)
    m_frame.place(x=0, y=50)

    var_id = StringVar()
    id_lbl = Label(m_frame, text="ID", font=("Arial", 15, "bold"))
    id_lbl.grid(row=0, column=0, padx=10, pady=10, sticky=W)
    id_entry = Entry(m_frame, font=("Arial", 15, "bold"), textvariable=var_id, width=25)
    id_entry.grid(row=0, column=1, padx=10, pady=10, sticky=W)
    id_entry.focus()

    var_cusname = StringVar()
    cusname_lbl = Label(m_frame, text="Customer Name", font=("Arial", 15, "bold"))
    cusname_lbl.grid(row=1, column=0, padx=10, pady=10, sticky=W)
    cusname_entry = Entry(m_frame, font=("Arial", 15, "bold"), textvariable=var_cusname, width=25)
    cusname_entry.grid(row=1, column=1, padx=10, pady=10, sticky=W)

    var_contact = StringVar()
    contact_lbl = Label(m_frame, text="Contact No.", font=("Arial", 15, "bold"))
    contact_lbl.grid(row=2, column=0, padx=10, pady=10, sticky=W)
    contact_entry = Entry(m_frame, font=("Arial", 15, "bold"), textvariable=var_contact, width=25)
    contact_entry.grid(row=2, column=1, padx=10, pady=10, sticky=W)

    var_lic = StringVar()
    lic_lbl = Label(m_frame, text="Driving License No.", font=("Arial", 15, "bold"))
    lic_lbl.grid(row=3, column=0, padx=10, pady=10, sticky=W)
    lic_entry = Entry(m_frame, font=("Arial", 15, "bold"), textvariable=var_lic, width=25)
    lic_entry.grid(row=3, column=1, padx=10, pady=10, sticky=W)

    address_lbl = Label(m_frame, text="Address", font=("Arial", 15, "bold"))
    address_lbl.grid(row=0, column=2, padx=10, pady=10, sticky=N)
    address_entry = Text(m_frame, width=37, height=3, font=("Arial", 15, "bold"))
    address_entry.grid(row=0, column=3, padx=10, pady=10, sticky=W, rowspan=2)

    btn_frame = LabelFrame(m_frame, borderwidth=1, height=100, width=720, relief=RIDGE, bg="purple")
    btn_frame.grid(row=5, column=1, padx=60, pady=(0, 4), sticky=W, columnspan=4)

    add_btn = Button(btn_frame, text="ADD", font=("Arial", 15, "bold"), command=add_func, bg="blue")
    add_btn.grid(row=0, column=0, padx=10, pady=10, sticky=W)

    update_btn = Button(btn_frame, text="UPDATE", font=("Arial", 15, "bold"), command=update_func, bg="green")
    update_btn.grid(row=0, column=1, padx=10, pady=10, sticky=W)

    del_btn = Button(btn_frame, text="DELETE", font=("Arial", 15, "bold"), command=del_func, bg="red")
    del_btn.grid(row=0, column=2, padx=10, pady=10, sticky=W)

    clear_btn = Button(btn_frame, text="CLEAR", font=("Arial", 15, "bold"), command=reset_func, bg="cyan")
    clear_btn.grid(row=0, column=3, padx=10, pady=10, sticky=W)

    search_frame = Frame(main_frame, borderwidth=1, relief=RIDGE)
    search_frame.place(x=0, y=320, height=50, width=1049)

    searchby_lbl = Label(search_frame, text="Search By:", font=("Arial", 15, "bold"))
    searchby_lbl.grid(row=0, column=0, padx=2, pady=10, sticky=N)

    var_by = StringVar()
    select_combo = ttk.Combobox(search_frame, font=("Arial", 15, "bold"), textvariable=var_by, state="readonly")
    select_combo["values"] = ("Select", "Customer_Name", "License_No")
    select_combo.current(0)
    select_combo.grid(row=0, column=1)

    box_entry = Entry(search_frame, font=("Arial", 15, "bold"))
    box_entry.grid(row=0, column=2, padx=10, pady=10, sticky=W)

    search_btn = Button(search_frame, text="SEARCH", font=("Arial", 10, "bold"), command=search_data, width=15)
    search_btn.grid(row=0, column=3, padx=10, pady=10, sticky=W)

    showall_btn = Button(search_frame, text="SHOW ALL", font=("Arial", 10, "bold"), width=15, command=fetch_data)
    showall_btn.grid(row=0, column=4, padx=10, pady=10, sticky=W)

    table_frame = Frame(main_frame, bd=2, relief=SUNKEN)
    table_frame.place(x=0, y=370, height=232, width=1045)
    scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
    scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)
    customer_table = ttk.Treeview(table_frame, columns=("id", "name", "contact", "license", "address"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
    scroll_x.pack(side=BOTTOM, fill=X)
    scroll_y.pack(side=RIGHT, fill=Y)
    scroll_x.config(command=customer_table.xview)
    scroll_y.config(command=customer_table.yview)
    customer_table.heading("id", text="ID")
    customer_table.heading("name", text="Name")
    customer_table.heading("contact", text="Contact No.")
    customer_table.heading("license", text="License No.")
    customer_table.heading("address", text="Address")
    customer_table["show"] = "headings"
    customer_table.column("id", anchor=CENTER)
    customer_table.column("name", anchor=CENTER)
    customer_table.column("contact", anchor=CENTER)
    customer_table.column("license", anchor=CENTER)
    customer_table.column("address", anchor=CENTER)
    customer_table.pack(fill=BOTH, expand=1)
    customer_table.bind("<ButtonRelease>", get_cursor)
    customer_table.tag_configure("oddrow", background="white")
    customer_table.tag_configure("evenrow", background="cyan")
    fetch_data()

def rent_func():
    global main_frame, conn, cursor
    main_frame.destroy()

    def fetch_data():
        cursor.execute("SELECT Car_Name from Cars WHERE Status='Car Not Booked'")
        car_combo["values"] = [i[0] for i in cursor.fetchall()]

    def calc_func():
        if to_entry.get_date() > from_entry.get_date():
            try:
                total_days = (to_entry.get_date() - from_entry.get_date()).days
                var_days.set(total_days)
                cursor.execute("SELECT Price FROM Cars WHERE Car_Name=?", (var_car.get(), ))
                price = cursor.fetchone()
                var_price.set(price[0])
                var_totprice.set(int(price[0])*total_days)
            except Exception as e:
                messagebox.showerror("ERROR!", f"ERROR: {e}")
        else:
            messagebox.showerror("ERROR!", "Invalid Dates!")

    def book_func():
        try:
            if var_car.get() == "" or var_cusno.get() == "":
                messagebox.showerror("ERROR!", "All fields are required!")
            else:
                while True:
                    num = randint(100000000000, 999999999999)
                    if not os.path.exists(f"Booked Cars Details/{num}.txt"):
                        break
                cursor.execute("INSERT INTO Rented_Cars VALUES(?, ?, ?, ?, ?, ?, ?, ?)", (num, var_car.get(), var_cusno.get(), from_entry.get(), to_entry.get(), var_days.get(), var_price.get(), var_totprice.get()))
                cursor.execute("UPDATE Cars SET Status='Car Booked' WHERE Car_Name=?", (var_car.get(),))
                conn.commit()
                cursor.execute("SELECT * FROM Customers WHERE Contact_No=?", (var_cusno.get(),))
                data = cursor.fetchone()
                with open(f'Booked Cars Details/{num}.txt', "w") as f:
                    f.write("CAR RENTAL MANAGEMENT SYSTEM\n")
                    f.write(f"{data[4]}\n")
                    f.write(f"Invoice                   :   {num}\n")
                    f.write(f'Date                      :   {datetime.now().strftime("%Y/%m/%d")}\n')
                    f.write(f"Customer Name             :   {data[1]}\n")
                    f.write(f"Car Name                  :   {var_car.get()}\n")
                    f.write(f"From Date                 :   {from_entry.get()}\n")
                    f.write(f"To Date                   :   {to_entry.get()}\n")
                    f.write(f"Total Days                :   {var_days.get()}\n")
                    f.write(f"Price Per Days (in INR)   :   {var_price.get()}\n")
                    f.write(f"Total Price (Rs)          :   {var_totprice.get()}\n")
                fetch_data()
                reset_func()
                messagebox.showinfo("SUCCESS!", "CAR BOOKED!")
        except Exception as e:
            messagebox.showerror("ERROR!", f"ERROR: {e}")

    def reset_func():
        var_car.set("")
        var_cusno.set("")
        var_days.set("")
        var_price.set("")
        var_totprice.set("")

    main_frame = Frame(win, borderwidth=3, height=607, width=1049, relief=SUNKEN)
    main_frame.place(x=316, y=90)

    lbl4 = Label(main_frame, text="RENT CAR", font=("Arial", 20, "bold"))
    lbl4.place(x=0, y=0)

    m_frame = LabelFrame(main_frame, borderwidth=1, height=500, width=900, relief=RIDGE)
    m_frame.place(x=80, y=90)

    var_car = StringVar()
    car_lbl = Label(m_frame, text="Available Cars", font=("Arial", 15, "bold"))
    car_lbl.grid(row=0, column=0, padx=10, sticky=W)
    car_combo = ttk.Combobox(m_frame, textvariable=var_car, font=("Arial", 15, "bold"), width=23, state="readonly")
    fetch_data()
    car_combo.grid(row=0, column=1, padx=10, pady=10, sticky=W)

    var_cusno = StringVar()
    cusno_lbl = Label(m_frame, text="Contact No.", font=("Arial", 15, "bold"))
    cusno_lbl.grid(row=1, column=0, padx=10, sticky=W)
    cusno_combo = ttk.Combobox(m_frame, textvariable=var_cusno, font=("Arial", 15, "bold"), width=23, state="readonly")
    cursor.execute("SELECT Contact_No FROM Customers")
    cusno_combo["values"] = [i[0] for i in cursor.fetchall()]
    cusno_combo.grid(row=1, column=1, padx=10, pady=10, sticky=W)

    from_lbl = Label(m_frame, text="From", font=("Arial", 15, "bold"))
    from_lbl.grid(row=2, column=0, padx=10, pady=10, sticky=W)
    from_entry = DateEntry(m_frame, mindate=datetime.now().date(), date_pattern="yyyy/mm/dd", font=("Arial", 15, "bold"), state="readonly")
    from_entry.grid(row=2, column=1, padx=10, pady=10, sticky=W)

    to_lbl = Label(m_frame, text="To", font=("Arial", 15, "bold"))
    to_lbl.grid(row=3, column=0, padx=10, pady=10, sticky=W)
    display_date = datetime.now().date() + timedelta(days=1)
    to_entry = DateEntry(m_frame, mindate=display_date, date_pattern="yyyy/mm/dd", font=("Arial", 15, "bold"), state="readonly")
    to_entry.grid(row=3, column=1, padx=10, pady=10, sticky=W)

    var_days = StringVar()
    days_lbl = Label(m_frame, text="Total Days", font=("Arial", 15, "bold"))
    days_lbl.grid(row=4, column=0, padx=10, pady=10, sticky=W)
    days_entry = Entry(m_frame, font=("Arial", 15, "bold"), textvariable=var_days, width=25, state="readonly")
    days_entry.grid(row=4, column=1, padx=10, sticky=W)

    var_price = StringVar()
    price_lbl = Label(m_frame, text="Price Per Day (in INR)", font=("Arial", 15, "bold"))
    price_lbl.grid(row=5, column=0, padx=10, pady=10, sticky=W)
    price_entry = Entry(m_frame, font=("Arial", 15, "bold"), textvariable=var_price, width=25, state="readonly")
    price_entry.grid(row=5, column=1, padx=10, sticky=W)

    var_totprice = StringVar()
    totprice_lbl = Label(m_frame, text="Total Price", font=("Arial", 15, "bold"))
    totprice_lbl.grid(row=6, column=0, padx=10, pady=10, sticky=W)
    totprice_entry = Entry(m_frame, font=("Arial", 15, "bold"), textvariable=var_totprice, width=25, state="readonly")
    totprice_entry.grid(row=6, column=1, padx=10, sticky=W)
    
    btn_frame = LabelFrame(m_frame, borderwidth=1, height=60, width=400, relief=RIDGE, bg="purple")
    btn_frame.grid(row=7, column=0, padx=120, pady=10, sticky=W, columnspan=2)

    calc_btn = Button(btn_frame, text="CALCULATE", font=("Arial", 15, "bold"), command=calc_func, bg="blue")
    calc_btn.grid(row=0, column=0, padx=10, pady=10, sticky=W)

    book_btn = Button(btn_frame, text="BOOK CAR", font=("Arial", 15, "bold"), command=book_func, bg="green")
    book_btn.grid(row=0, column=1, padx=10, pady=10, sticky=W)

    clear_btn = Button(btn_frame, text="CLEAR", font=("Arial", 15, "bold"), command=reset_func, bg="red")
    clear_btn.grid(row=0, column=2, padx=10, pady=10, sticky=W)
    
def return_func():
    global main_frame, conn, cursor
    main_frame.destroy()

    def ret_func():
        try:
            if var_inv.get() == "":
                messagebox.showerror("ERROR!", "Invoice Number is required!")
            else:
                cursor.execute("SELECT Car_Name FROM Rented_Cars WHERE Invoice=?", (var_inv.get(),))
                invs = cursor.fetchone()
                if invs != None:
                    cursor.execute("DELETE FROM Rented_Cars WHERE Invoice=?", (var_inv.get(), ))
                    cursor.execute("UPDATE Cars SET Status='Car Not Booked' WHERE Car_Name=?", (invs[0],))
                    messagebox.showinfo("SUCCESS!", "CAR RETURNED!")
                    var_inv.set("")
                else:
                    messagebox.showerror("ERROR!", "Wrong Invoice Number!")
                conn.commit()
        except Exception as e:
            messagebox.showerror("ERROR!", f"ERROR: {e}")

    main_frame = Frame(win, borderwidth=3, height=607, width=1049, relief=SUNKEN)
    main_frame.place(x=316, y=90)

    lbl4 = Label(main_frame, text="RETURN CAR", font=("Arial", 20, "bold"))
    lbl4.place(x=0, y=0)

    def slide():
        global i 
        img2 = Image.open(f"/Users/intra/Desktop/Project/Car Rental System/Images/Cars/{lt[i]}")
        img2 = img2.resize((700,450), Image.LANCZOS)
        img2 = ImageTk.PhotoImage(img2)
        img_label.config(image=img2)
        img_label.photo_re = img2
        i += 1
        if i == len(lt):
            i = 0
        img_label.after(3000, slide)
    lt = [f"car{i}.jpg" for i in range(1, 11)]
    img = Image.open(f"/Users/intra/Desktop/Project/Car Rental System/Images/Cars/{lt[0]}")
    img = img.resize((500,500), Image.LANCZOS)
    img = ImageTk.PhotoImage(img)
    img_label = Label(main_frame, image=img)
    img_label.pack(padx=170, pady=(35, 0))
    slide()

    var_inv = StringVar()
    inv_lbl = Label(main_frame, text="Enter the Invoice No.", font=("Arial", 15, "bold"))
    inv_lbl.pack(pady=5)
    inv_entry = Entry(main_frame, textvariable=var_inv, font=("Arial", 15, "bold"))
    inv_entry.pack()
    inv_entry.focus()
    
    ret_btn = Button(main_frame, text="RETURN", font=("Arial", 15, "bold"), command=ret_func, bg="green")
    ret_btn.pack(pady=5)

def viewall_func():
    global main_frame, conn, cursor
    main_frame.destroy()

    def fetch_data():
        try:
            cursor.execute("SELECT * FROM Cars")
            data = cursor.fetchall()
            if len(data) != 0:
                cars_table.delete(*cars_table.get_children())
                for n, i in enumerate(data):
                    if n % 2 == 0:
                        cars_table.insert("", END, values=i, tags=("evenrow", ))
                    else:
                        cars_table.insert("", END, values=i, tags=("oddrow", ))
                conn.commit()
            else:
                for item in cars_table.get_children():
                    cars_table.delete(item) 
        except Exception as e:
            messagebox.showerror("ERROR!", f"ERROR: {e}")

    def slide():
        global i 
        img2 = Image.open(f"/Users/intra/Desktop/Project/Car Rental System/Images/Cars/{lt[i]}")
        img2 = img2.resize((300,300), Image.LANCZOS)
        img2 = ImageTk.PhotoImage(img2)
        img_label.config(image=img2)
        img_label.photo_re = img2
        i += 1
        if i == len(lt):
            i = 0
        img_label.after(3000, slide)

    main_frame = Frame(win, borderwidth=3, height=607, width=1049, relief=SUNKEN)
    main_frame.place(x=316, y=90)

    lbl4 = Label(main_frame, text="CARS", font=("Arial", 20, "bold"))
    lbl4.place(x=0, y=0)

    lt = [f"car{i}.jpg" for i in range(1, 11)]
    img = Image.open(f"/Users/intra/Desktop/Project/Car Rental System/Images/Cars/{lt[0]}")
    img = img.resize((300,300), Image.LANCZOS)
    img = ImageTk.PhotoImage(img)
    img_label = Label(main_frame, image=img)
    img_label.place(x=350, y=30)
    slide()

    table_frame = Frame(main_frame, bd=2, relief=RIDGE)
    table_frame.place(x=0, y=340, height=260, width=1049)
    scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
    scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)
    cars_table = ttk.Treeview(table_frame, columns=("car", "mod", "fuel", "brand", "price", "seat", "desc", "air", "pdl", "cra", "powin", "lseat", "dair", "pair", "cd", "anti", "break", "stat"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
    scroll_x.pack(side=BOTTOM, fill=X)
    scroll_y.pack(side=RIGHT, fill=Y)
    scroll_x.config(command=cars_table.xview)
    scroll_y.config(command=cars_table.yview)
    cars_table.heading("car", text="Car Name")
    cars_table.heading("mod", text="Model Year")
    cars_table.heading("fuel", text="Fuel Type")
    cars_table.heading("brand", text="Brand Name")
    cars_table.heading("price", text="Price")
    cars_table.heading("seat", text="Seating Capacity")
    cars_table.heading("desc", text="Description")
    cars_table.heading("air", text="Air Condition")
    cars_table.heading("pdl", text="Power Door Lock")
    cars_table.heading("cra", text="Crash Sensor")
    cars_table.heading("powin", text="Power Window")
    cars_table.heading("lseat", text="Leather Seat")
    cars_table.heading("dair", text="Driver Airbag")
    cars_table.heading("pair", text="Passenger Airbag")
    cars_table.heading("cd", text="CD Player")
    cars_table.heading("anti", text="Antilock")
    cars_table.heading("break", text="Break Assit")
    cars_table.heading("stat", text="Status")
    cars_table["show"] = "headings"

    cars_table.column("car", anchor=CENTER)
    cars_table.column("mod", anchor=CENTER)
    cars_table.column("fuel", anchor=CENTER)
    cars_table.column("brand", anchor=CENTER)
    cars_table.column("price", anchor=CENTER)
    cars_table.column("seat", anchor=CENTER)
    cars_table.column("desc", anchor=CENTER)
    cars_table.column("air", anchor=CENTER)
    cars_table.column("pdl", anchor=CENTER)
    cars_table.column("cra", anchor=CENTER)
    cars_table.column("powin", anchor=CENTER)
    cars_table.column("lseat", anchor=CENTER)
    cars_table.column("dair", anchor=CENTER)
    cars_table.column("pair", anchor=CENTER)
    cars_table.column("cd", anchor=CENTER)
    cars_table.column("anti", anchor=CENTER)
    cars_table.column("break", anchor=CENTER)
    cars_table.column("stat", anchor=CENTER)
    cars_table.pack(fill=BOTH, expand=1)
    cars_table.tag_configure("oddrow", background="white")
    cars_table.tag_configure("evenrow", background="cyan")
    fetch_data()

def main_win():
    global win
    win = Tk()
    win.state("zoomed")
    win.title("CAR RENTAL MANAGEMENT SYSTEM")
    win.iconbitmap("/Users/intra/Desktop/Project/Car Rental System/Images/logo.ico")

    def check_func():
        today = datetime.now().strftime("%Y/%m/%d")
        cursor.execute("SELECT Car_Name FROM Rented_Cars WHERE To_Date=?", (today, ))
        cars = ", ".join([i[0] for i in cursor.fetchall()])
        if len(cars) > 0:
            messagebox.showinfo("RETURN!", f"The following cars should be returned:\n{cars}")

    def exit_func():
        y_n = messagebox.askyesno("EXIT!", "Are you sure you want to exit?")
        if y_n == 1:
            win.destroy()
        else:
            pass

    style = ttk.Style()
    style.theme_use("clam")
    style.configure('Treeview.Heading', background="green3")
    style.configure("Treeview", background="silver", foreground="black", rowheight=45, fieldbackgroud="silver")
    style.map("Treeview", background=[("selected", "grey")])
        
    top_frame = Frame(win, borderwidth=3, relief=SUNKEN)
    top_frame.pack(fill=BOTH)

    logo = Image.open(f"/Users/intra/Desktop/Project/Car Rental System/Images/image.jpg")
    logo = logo.resize((70,70), Image.LANCZOS)
    logo = ImageTk.PhotoImage(logo)
    logo_label = Label(top_frame, image=logo)
    logo_label.place(x=80, y=5)

    lbl2 = Label(top_frame, text="CAR RENTAL SYSTEM", font=("Arial", 50, "bold"), fg="#a83232")
    lbl2.pack()

    def time():
        string = strftime("%I:%M:%S %p")
        time_lbl.config(text=string)
        time_lbl.after(1000, time)
        
    time_lbl = Label(top_frame, font=("Arial", 15, "bold"), fg="purple")
    time_lbl.place(x=1200, y=20, width=130, height=50)
    time()

    dash_btn = Button(win, text="DASHBOARD", height=2, width=18, command=dash_func, font=("Arial", 20, "bold"), bg="orange")
    dash_btn.place(x=0, y=90)

    mancars_btn = Button(win, text="MANAGE CARS", width=18, height=2, command=mancars_func, font=("Arial", 20, "bold"), bg="blue")
    mancars_btn.place(x=0, y=178)

    mancus_btn = Button(win, text="MANAGE CUSTOMERS", width=18, height=2, command=mancus_func, font=("Arial", 20, "bold"), bg="yellow")
    mancus_btn.place(x=0, y=266)

    rent_btn = Button(win, text="RENT CAR", height=2, width=18, command=rent_func, font=("Arial", 20, "bold"), bg="purple")
    rent_btn.place(x=0, y=355)

    return_btn = Button(win, text="RETURN CAR", height=2, width=18, command=return_func, font=("Arial", 20, "bold"), bg="orange")
    return_btn.place(x=0, y=443)

    viewall_btn = Button(win, text="VIEW ALL CARS", height=2, width=18, command=viewall_func, font=("Arial", 20, "bold"), bg="green")
    viewall_btn.place(x=0, y=532)

    exit_btn = Button(win, text="EXIT", height=2, width=18, command=exit_func, font=("Arial", 20, "bold"), bg="red")
    exit_btn.place(x=0, y=620)

    win.protocol("WM_DELETE_WINDOW", exit_func)

    dash_func()
    check_func()

    win.mainloop()

def login(event=""):
    if user_entry.get() == "root" and pass_entry.get() == "admin":
        messagebox.showinfo("ACCESS!", "ACCESS GRANTED!")
        root.destroy()
        main_win()
    else:
        messagebox.showerror("DENIED!", "WRONG CREDENTIALS!")  

root = Tk()
root.state("zoomed")
root.title("RENT CAR")
root.iconbitmap("/Users/intra/Desktop/Project/Car Rental System/Images/logo.ico")
bg_img = Image.open("/Users/intra/Desktop/Project/Car Rental System/Images/rent.jpg")
bg_img =  bg_img.resize((1366, 768), Image.LANCZOS)
photoimg1 = ImageTk.PhotoImage(bg_img)
lbl1 = Label(root, image=photoimg1)
lbl1.pack()
user_lbl = Label(root, text="Username:", font=("Arial", 25, "bold"))
user_lbl.place(x=900, y=150)
user_entry = Entry(root, font=("Arial", 25, "bold"))
user_entry.place(x=900, y=200)
user_entry.focus()
pass_lbl = Label(root, text="Password:", font=("Arial", 25, "bold"))
pass_lbl.place(x=900, y=250)
pass_entry = Entry(root, font=("Arial", 25, "bold"), show="*")
pass_entry.place(x=900, y=300)
log_btn = Button(root, text="LOGIN", command=login, font=("Arial", 25, "bold"))
log_btn.place(x=1000, y=350, height=40)
root.bind("<Return>", login)
root.mainloop()
