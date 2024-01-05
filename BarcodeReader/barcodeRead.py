import cv2
from pyzbar.pyzbar import decode
import tkinter as tk
import mysql.connector
from tkinter import ttk
from dbFunctions import *
from tkcalendar import Calendar
from datetime import datetime
import pygame
from PIL import Image, ImageTk 

mysqllog = ["192.168.1.113", "admin", "Actimel1234", "inventory_db"]

def scan_barcode():
    delay = 500
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    barcodes = decode(gray)
    if barcodes:    
        barcode_data = barcodes[0].data.decode('utf-8')
        delay = 3000
        if check_database(mysqllog, barcode_data):
            show_window()
            fill_form(barcode_data)
            sound.play()
        else:
            show_window()
            barcode_var.set(barcode_data)
            name_var.set("")
            man_var.set("")
            catbox.set("")
            storebox.set("")
            amount_var.set("")
            unitbox.set("")
            usebox.set("")
            sound.play()
            
        print("ok")
        
    root.after(delay, scan_barcode)

def show_camera():
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (320, 240))
        photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
        label_camera.imgtk = photo
        label_camera.configure(image=photo)
    label_camera.after(10, show_camera)

def display_calendar():
    def select_date():
        selected_date = cal.get_date()
        date_entry.delete(0, tk.END)
        date_entry.insert(0, selected_date)
        top.destroy()

    top = tk.Toplevel(root)
    top.geometry("250x200")
    top.title("Select Date")

    cal = Calendar(top)
    cal.pack()

    select_button = ttk.Button(top, text="Select Date", command=select_date)
    select_button.pack()

def pipe_data():
    date = date_entry.get()
    if date != "":
        date_obj = datetime.strptime(date, '%d/%m/%Y')
        date = date_obj.strftime('%Y-%m-%d')
    else:
        date = None

    data = [
        barcode_entry.get(),
        name_entry.get(),
        man_entry.get(),
        amount_entry.get(),
        catbox.get(),
        storebox.get(),
        usebox.get(),
        date,
        unitbox.get()
    ]
    
    print("ok")
    print(data)
    insert_data(mysqllog, data)
    hide_window()


def show_window():
    root.deiconify()

def hide_window():
    #root.withdraw()
    True

def fill_form(barcode):
    form_data = select_data(mysqllog, barcode)
    barcode_var.set(form_data[0])
    name_var.set(form_data[1])
    man_var.set(form_data[2])
    catbox.set(form_data[3])
    storebox.set(form_data[4])
    amount_var.set(form_data[5])
    usebox.set(form_data[6])
    unitbox.set(form_data[7])
 
def delete_product():
    date = date_entry.get()
    if date != "":
        date_obj = datetime.strptime(date, '%d/%m/%Y')
        date = date_obj.strftime('%Y-%m-%d')
    else:
        date = None
        
    remove_product(mysqllog, barcode_entry.get(), date)
    hide_window()
    
pygame.mixer.init()
sound = pygame.mixer.Sound('ding.wav')
root = tk.Tk()
#root.overrideredirect(True)
root.attributes('-topmost', True)
root.title("Barcode Scanner")

label_camera = tk.Label(root)
label_camera.pack()

labelbarcode = tk.Label(root, text="Barcode")
labelbarcode.pack()
barcode_var = tk.StringVar()
barcode_entry = tk.Entry(root, textvariable=barcode_var)
barcode_entry.pack()

labelname = tk.Label(root, text="Name")
labelname.pack()
name_var = tk.StringVar()
name_entry = tk.Entry(root, textvariable=name_var)
name_entry.pack()

labelman = tk.Label(root, text="Manufacturer")
labelman.pack()
man_var = tk.StringVar()
man_entry = tk.Entry(root, textvariable=man_var)
man_entry.pack()

labelunit = tk.Label(root, text="Units")
labelunit.pack()
units = ['g', 'l', 'p']
unitbox = ttk.Combobox(root, values=units, state='readonly')
unitbox.pack()

labelamount = tk.Label(root, text="Amount")
labelamount.pack()
amount_var = tk.StringVar()
amount_entry = tk.Entry(root, textvariable=amount_var)
amount_entry.pack()

labelcat = tk.Label(root, text="Category")
labelcat.pack()
categories = ['Fruit','Vegetable','Baked goods','Protein','Seafood','Dairy','Eggs and Fats','Ready-made food','Oil','Spices','Grains','Drinks','Snacks']
catbox = ttk.Combobox(root, values=categories, state='readonly')
catbox.pack()

labelstore = tk.Label(root, text="Storage")
labelstore.pack()
spaces = ['Fridge', 'Freezer', 'Snack Cupboard', 'Meal Cupboard', 'Baking Drawer', 'Spice Cabinet']
storebox = ttk.Combobox(root, values=spaces, state='readonly')
storebox.pack()

labeluse = tk.Label(root, text="Expiry Type")
labeluse.pack()
uses = ['Best By', 'Use By']
usebox = ttk.Combobox(root, values=uses, state='readonly')
usebox.set('Best By')
usebox.pack()

labeldate = tk.Label(root, text="Expiry Date")
labeldate.pack()
date_entry = ttk.Entry(root)
date_entry.pack()
date_entry.bind("<Button-1>", lambda event: display_calendar())

add_button = ttk.Button(root, text="Add", command=pipe_data)
add_button.pack()

remove_button = ttk.Button(root, text="Remove", command=delete_product)
remove_button.pack()

cap = cv2.VideoCapture(0)
show_camera()
scan_barcode()

def close_window():
    cap.release()
    root.close()

root.bind('q', lambda event: close_window())
root.bind('w', lambda event: show_window())
root.mainloop()
