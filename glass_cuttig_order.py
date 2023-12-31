import mysql.connector
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox, filedialog
import csv
import os

def select(treeview):
    selected_item = treeview.focus()
    details = treeview.item(selected_item)
    order = details.get('values')[1]
    return order

def move_pvc():
    order_to_move = (select(pvc_treeview),)
    get_order = "SELECT firm, order_id, length, width, count, type FROM pvc_glass_orders WHERE order_id = %s " \
                "AND done = 0"
    cursor.execute(get_order, order_to_move)
    rows = cursor.fetchall()
    for row in rows:
        result_treeview.insert('', 'end', values=row)
    data_update = "UPDATE pvc_glass_orders SET done = 0 WHERE order_id = %s AND done = 0"
    order_id = (select(pvc_treeview),)
    cursor.execute(data_update, order_id)
    connection.commit()
    pvc_treeview.delete(*pvc_treeview.get_children())
    cursor.execute("SELECT firm, order_id, length, width, count, type FROM pvc_glass_orders WHERE done = 0")
    rows = cursor.fetchall()
    for row in rows:
        pvc_treeview.insert('', 'end', values=row)
    return

def move_glass():
    order_to_move = (select(glass_treeview),)
    get_order = "SELECT firm, order_id, length, width, count, type FROM glass_glass_orders WHERE order_id = %s " \
                "AND done = 0"
    cursor.execute(get_order, order_to_move)
    rows = cursor.fetchall()
    for row in rows:
        result_treeview.insert('', 'end', values=row)
    data_update = "UPDATE pvc_glass_orders SET done = 0 WHERE order_id = %s AND done = 0"
    order_id = (select(glass_treeview),)
    cursor.execute(data_update, order_id)
    connection.commit()
    glass_treeview.delete(*glass_treeview.get_children())
    cursor.execute("SELECT firm, order_id, length, width, count, type FROM glass_glass_orders WHERE done = 0")
    rows = cursor.fetchall()
    for row in rows:
        glass_treeview.insert('', 'end', values=row)
    return

def export_result():
    file_name = filedialog.asksaveasfilename(initialdir=os.getcwd(), title='Save CSV', filetypes=(('CSV File', '*.csv'), ('all Files', '*.*')))
    print(file_name)
    with open(file_name, mode='w', newline='') as myfile:
        exp_writer = csv.writer(myfile, delimiter=',')
        for i in result_treeview.get_children():
            row = result_treeview.item(i)['values']
            row.insert(4, 'R')
            row.insert(6, row[5])
            print(row)
            exp_writer.writerow(row)


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

wrapper1.pack(side=tk.LEFT, fill='both', expand="yes", padx=5, pady=10)
wrapper2.pack(side=tk.LEFT, fill='both', expand="yes", padx=5, pady=10)
wrapper3.pack(side=tk.LEFT, fill='both', expand="yes", padx=5, pady=10)

glass_cutting_order.title = 'Файл за производство'
glass_cutting_order.geometry('1500x750')

cursor.execute("SELECT firm, order_id, length, width, count, type FROM pvc_glass_orders WHERE done = 0")
rows_pvc = cursor.fetchall()
cursor.execute("SELECT firm, order_id, length, width, count, type FROM glass_glass_orders WHERE done = 0")
rows_glass = cursor.fetchall()

pvc_treeview = ttk.Treeview(wrapper1, columns=(1,2,3,4,5,6), show='headings', height=30)
pvc_treeview.pack()
# pvc_treeview.place(x=0, y=0)
# yscrollbar = ttk.Scrollbar(wrapper1, orient='vertical', command=pvc_treeview.yview())
# yscrollbar.pack(side=RIGHT,fill='y')
# pvc_treeview.configure(yscrollcommand=yscrollbar.set)

pvc_treeview.heading(1, text='Фирма')
pvc_treeview.heading(2, text='Поръчка')
pvc_treeview.heading(3, text='Дължина')
pvc_treeview.heading(4, text='Ширина')
pvc_treeview.heading(5, text='Брой')
pvc_treeview.heading(6, text='Вид')
pvc_treeview.column(1, width=120)
pvc_treeview.column(2, width=60)
pvc_treeview.column(3, width=60)
pvc_treeview.column(4, width=60)
pvc_treeview.column(5, width=50)
pvc_treeview.column(6, width=80)

glass_treeview = ttk.Treeview(wrapper2, columns=(1,2,3,4,5,6), show='headings', height=30)
glass_treeview.pack()
glass_treeview.heading(1, text='Фирма')
glass_treeview.heading(2, text='Поръчка')
glass_treeview.heading(3, text='Дължина')
glass_treeview.heading(4, text='Ширина')
glass_treeview.heading(5, text='Брой')
glass_treeview.heading(6, text='Вид')
glass_treeview.column(1, width=120)
glass_treeview.column(2, width=60)
glass_treeview.column(3, width=60)
glass_treeview.column(4, width=60)
glass_treeview.column(5, width=50)
glass_treeview.column(6, width=80)

for row in rows_pvc:
    pvc_treeview.insert('', 'end', values=row)
for row in rows_glass:
    glass_treeview.insert('', 'end', values=row)

result_treeview = ttk.Treeview(wrapper3, columns=(1,2,3,4,5,6), show='headings', height=30)
result_treeview.pack()
result_treeview.heading(1, text='Фирма')
result_treeview.heading(2, text='Поръчка')
result_treeview.heading(3, text='Дължина')
result_treeview.heading(4, text='Ширина')
result_treeview.heading(5, text='Брой')
result_treeview.heading(6, text='Вид')
result_treeview.column(1, width=120)
result_treeview.column(2, width=60)
result_treeview.column(3, width=60)
result_treeview.column(4, width=60)
result_treeview.column(5, width=50)
result_treeview.column(6, width=80)

move_pvc_button = tk.Button(wrapper1, text='Прехвърли', height=2, command=move_pvc)
move_pvc_button.pack(pady=5)
move_glass_button = tk.Button(wrapper2, text='Прехвърли', height=2, command=move_glass)
move_glass_button.pack(pady=5)
export_button = tk.Button(wrapper3, text='Експорт', height=2, command=export_result)
export_button.pack(pady=5)

glass_cutting_order.mainloop()

#from 0 to 1