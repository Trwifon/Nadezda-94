import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as tkFont
from _datetime import datetime


dict_connection = {
    'host': '127.0.0.1',
    'port': '3306',
    'user': 'root',
    'password': 'Proba123+',
    'database': 'nadejda-94'
}
connection = mysql.connector.connect(**dict_connection)
cursor = connection.cursor()

glass_cutting_order = tk.Tk()

wrapper1 = tk.LabelFrame(glass_cutting_order, text = 'Поръчки PVC')
wrapper2 = tk.LabelFrame(glass_cutting_order, text = 'Поръчки Стъкла')
wrapper3 = tk.LabelFrame(glass_cutting_order, text = 'Поръчки за цех')

wrapper1.pack(side=tk.LEFT, fill='both', expand="yes", padx=20, pady=10)
wrapper2.pack(side=tk.LEFT, fill='both', expand="yes", padx=20, pady=10)
wrapper3.pack(side=tk.LEFT, fill='both', expand="yes", padx=20, pady=10)

glass_cutting_order.title = 'Файл за производство'
glass_cutting_order.geometry('1500x600')


pvc_treeview = ttk.Treeview(wrapper1, columns=(1,2,3,4,5,6), show='headings', height=20)
pvc_treeview.pack()
pvc_treeview.heading(1, text='Фирма')
pvc_treeview.heading(2, text='Поръчка')
pvc_treeview.heading(3, text='Дължина')
pvc_treeview.heading(4, text='Ширина')
pvc_treeview.heading(5, text='Брой')
pvc_treeview.heading(6, text='Вид')

cursor.execute("SELECT firm, order_id, length, width, count, type FROM pvc_glass_orders WHERE done = 0")
rows = cursor.fetchall()
for row in rows:
    pvc_treeview.insert('', 'end', values=row)

glass_cutting_order.mainloop()
