import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont

data_dictionary = {'firm': '', 'order': '', 'length': 0, 'width': 0, 'count': 0, 'type': '', 'price': 0.0,
                   'sum_count': 0, 'sum_area': 0.0, 'sum_total': 0.0}
dict_connection = {
    'host': '127.0.0.1',
    'port': '3306',
    'user': 'root',
    'password': 'Proba123+',
    'database': 'nadejda-94'
}
list_glass = ['4', '5', 'K', '4S']
tickness = [12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 42, 44]
list_month = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']
list_number = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
order_list = []

def list_combobox():
    connection = mysql.connector.connect(**dict_connection)
    cursor = connection.cursor()
    cursor.execute("SELECT partner_name FROM partner")
    rows = cursor.fetchall()
    firm_list = [i[0] for i in rows]
    firm_list.sort()
    cursor.close()
    connection.close()
    return firm_list

def ok_button_press(event): #?
    event.widget.config() #?
    data_dictionary['firm'] = firm_cb.get()
    data_dictionary['order'] = f"{order_label['text']}{order_month_cb.get()}-{order_day_cb.get()}"
    data_dictionary['length'], data_dictionary['width'], data_dictionary['count'] = \
        int(length_entry.get()), int(width_entry.get()), int(count_entry.get())
    if third_glass_cb.get() == "":
        data_dictionary['type'] = f"{first_glass_cb.get()}+{second_glass_cb.get()}={tickness_cb.get()}"
    else:
        data_dictionary['type'] = f"{first_glass_cb.get()}+{second_glass_cb.get()}+{third_glass_cb.get()}=" \
                                  f"{tickness_cb.get()}"
    data_dictionary['price'] = float(price_entry.get())
    data_dictionary['sum_count'] += int(count_entry.get())
    current_area = data_dictionary['length'] * data_dictionary['width'] / 1000000
    if current_area <= 0.3:
        current_area = 0.3
    data_dictionary['sum_area'] += current_area * int(count_entry.get())
    data_dictionary['sum_total'] = data_dictionary['sum_area'] * data_dictionary['price']
    order_list.append(data_dictionary.copy())
    length_entry.focus_set()
    length_entry.select_range(0, 4)
    event.widget.invoke() #?
    return

def finish_button():
    connection = mysql.connector.connect(**dict_connection)
    cursor = connection.cursor()
    insert_orders = ("INSERT INTO pvc_glass_orders (firm, order_id, length, width, count, type, price, sum_count, "
                     "sum_area, sum_total) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    for index in range(len(order_list)):
        order_data = (order_list[index]['firm'], 'proba', order_list[index]['length'], order_list[index]['width'],
                      order_list[index]['count'], order_list[index]['type'], order_list[index]['price'],
                      order_list[index]['sum_count'], order_list[index]['sum_area'], order_list[index]['sum_total'])
        cursor.execute(insert_orders, order_data)
        connection.commit()
    cursor.close()
    connection.close()
    return

def tab_order():
    widgets = [firm_cb, order_month_cb, order_day_cb, first_glass_cb, second_glass_cb, third_glass_cb,
               tickness_cb, price_entry, length_entry, width_entry, count_entry]
    for element in widgets:
        element.lift()
    return


# create entry window
glass_entry_window = tk.Tk()
glass_entry_window.title('Форма за въвеждане на стъклопакети')
glass_entry_window.geometry('1080x500')
def_font = tk.font.nametofont("TkDefaultFont")
def_font.config(size=20)

# radio_var = tkinter.IntVar()
glass_entry_window.option_add('*TCombobox*Listbox.font', ('Helvetica', 15))

# first_row
firm_label = ttk.Label(glass_entry_window, width=10, text=('Фирма'), anchor="c", font=('Helvetica', 20))
firm_label.grid(row=0, columnspan = 3, column=0, padx=10, pady=20)
firm_label.configure(background='Light Grey')
kind_label = ttk.Label(glass_entry_window, width=20, text=('Вид'), anchor="c", font=('Helvetica', 20))
kind_label.grid(row=0, column=4, padx=10, pady=20)
kind_label.configure(background='Light Grey')
tickness_label = ttk.Label(glass_entry_window, width=10, text=('Дебелина'), anchor="c", font=('Helvetica', 20))
tickness_label.grid(row=0, column=5, padx=20, pady=20)
tickness_label.configure(background='Light Grey')

#second row
firm_list = list_combobox()
firm_cb = ttk.Combobox(glass_entry_window, width=20, values=firm_list, font=('', 20), height=20)
firm_cb.grid(row=1, columnspan = 3, column=0, sticky="we", padx=10, pady=20)
firm_cb.focus_set()
# firm_cb.bind('<KeyRelease>', update_cb)
# firm_cb.bind('<<ComboboxSelected>>', getSelectedItem)
first_glass = ttk.Label(glass_entry_window, width=13, text=('Първо стъкло'), anchor="c", font=('Helvetica', 20))
first_glass.grid(row=1, column=3, padx=10, pady=20)
first_glass.configure(background='Light Grey')
first_glass_cb = ttk.Combobox(glass_entry_window, width=15, values=list_glass, font=('', 20), height=20)
first_glass_cb.grid(row=1, column=4, sticky="ew", padx=20, pady=20)
tickness_cb = ttk.Combobox(glass_entry_window, width=3, values=tickness, font=('', 20), height=20)
tickness_cb.grid(row=1, column=5, sticky="ew", padx=60, pady=20)

#third row
order_label = ttk.Label(glass_entry_window, width=10, text=('Поръчка'), anchor="c", font=('Helvetica', 20))
order_label.grid(row=2, columnspan = 3, column=0, padx=2, pady=20)
order_label.configure(background='Light Grey')
second_glass = ttk.Label(glass_entry_window, width=13, text=('Второ стъкло'), anchor="c", font=('Helvetica', 20))
second_glass.grid(row=2, column=3, padx=10, pady=20)
second_glass.configure(background='Light Grey')
second_glass_cb = ttk.Combobox(glass_entry_window, width=15, values=list_glass, font=('', 20), height=20)
second_glass_cb.grid(row=2, column=4, sticky="ew", padx=20, pady=20)
price_label = ttk.Label(glass_entry_window, width=10, text=('Цена'), anchor="c", font=('Helvetica', 20))
price_label.grid(row=2, column=5, padx=20, pady=20)
price_label.configure(background='Light Grey')

#fourth row
order_label = ttk.Label(glass_entry_window, width=3, text=('P'), anchor="c", font=('Helvetica', 20))
order_label.grid(row=3, column=0, sticky="e", padx=2, pady=20)
order_label.configure(background='Light Grey')
order_month_cb = ttk.Combobox(glass_entry_window, width=3, values=list_month, font=('', 20), height=20)
order_month_cb.grid(row=3, column=1, sticky="ew", padx=30, pady=20)
order_day_cb = ttk.Combobox(glass_entry_window, width=3, values=list_number, font=('', 20), height=20)
order_day_cb.grid(row=3, column=2, sticky="w", padx=2, pady=20)
third_glass = ttk.Label(glass_entry_window, width=13, text=('Трето стъкло'), anchor="c", font=('Helvetica', 20))
third_glass.grid(row=3, column=3, padx=10, pady=20)
third_glass.configure(background='Light Grey')
third_glass_cb = ttk.Combobox(glass_entry_window, width=15, values=list_glass, font=('', 20), height=20)
third_glass_cb.grid(row=3, column=4, sticky="ew", padx=20, pady=20)
price_entry = ttk.Entry(glass_entry_window, width=3, justify='center', font=('Helvetica', 20))
price_entry.insert(0, 55)
price_entry.grid(row=3, column=5, sticky="ew", padx=50)

# #fifth row
length_label = ttk.Label(glass_entry_window, width=13, text=('Първи размер'), anchor="c", font=('Helvetica', 20))
length_label.grid(row=4, columnspan = 2, column=0, padx=10, pady=20)
length_label.configure(background='Light Grey')
width_label = ttk.Label(glass_entry_window, width=13, text=('Втори размер'), anchor="c", font=('Helvetica', 20))
width_label.grid(row=4, columnspan = 2, column=2, padx=10, pady=20)
width_label.configure(background='Light Grey')
count_label = ttk.Label(glass_entry_window, width=8, text=('Брой'), anchor="c", font=('Helvetica', 20))
count_label.grid(row=4, column=4, padx=10, pady=20, sticky="w")
count_label.configure(background='Light Grey')

# #sixth row
length_entry = ttk.Entry(glass_entry_window, width=4, justify='center', font=('Helvetica', 50))
length_entry.insert(0, 0)
length_entry.grid(row=5, columnspan = 2, column=0, sticky="e", padx=40, pady=20)
width_entry = ttk.Entry(glass_entry_window, width=3,justify='center', font=('Helvetica', 50))
width_entry.insert(0, 0)
width_entry.grid(row=5, columnspan = 2, column=2, sticky="we", padx=80, pady=20)
count_entry = ttk.Entry(glass_entry_window, width=3, justify='center', font=('Helvetica', 50))
count_entry.insert(2, 1)
count_entry.grid(row=5, column=4, sticky="w", padx=10, pady=20)
ok_button = ttk.Button(glass_entry_window, width=8, text='OK') #, command=ok_button_press
ok_button.grid(row=5, column=4, sticky="e", padx=10, pady=20)
ok_button.bind("<KeyRelease-Return>", ok_button_press) #?

finish_button = ttk.Button(glass_entry_window, width=8, text='Край', command=finish_button)
finish_button.grid(row=5, column=5, padx=10, pady=20)
tab_order()



# # day_report
# scrollbar = ttk.Scrollbar(glass_entry_window, orient=tk.VERTICAL)
# tree_day_report = ttk.Treeview(glass_entry_window, height=30)
# tree_day_report['show'] = 'headings'
# scrollbar.configure(command=tree_day_report.yview)
# tree_day_report.configure(yscrollcommand=scrollbar.set)
# scrollbar.grid(row=0, rowspan=15, column=5, sticky="nsw")
# tree_day_report.grid(row=0, rowspan=20, column=4, sticky='ne')
# style = ttk.Style()
# style.configure('Treeview', font=('Helvetica', 10))
# tree_day_report['columns'] = ('firm', 'action', 'ammount', 'note')
# tree_day_report.column('firm', width=150, minwidth=50, anchor=tk.CENTER)
# tree_day_report.column('action', width=100, minwidth=50, anchor=tk.CENTER)
# tree_day_report.column('ammount', width=80, minwidth=50, anchor=tk.CENTER)
# tree_day_report.column('note', width=420, minwidth=50, anchor=tk.CENTER)
# tree_day_report.heading('firm', text='Фирма', anchor=tk.CENTER)
# tree_day_report.heading('action', text='Действие', anchor=tk.CENTER)
# tree_day_report.heading('ammount', text='Сума', anchor=tk.CENTER)
# tree_day_report.heading('note', text='Забележка', anchor=tk.CENTER)
# connection = mysql.connector.connect(**dict_connection)
# cursor = connection.cursor()
# cursor.execute("SELECT partner.partner_name, records.order_type, records.ammount, records.note FROM records INNER"
#                " JOIN partner ON records.partner_id = partner.partner_id"
#                " WHERE warehouse = 'PVC' and date = current_date")
# today_orders = cursor.fetchall()
# cursor.close()
# connection.close()
# for row in today_orders:
#     tree_day_report.insert('', 'end', values=row)
#     if row[1] == 'Каса':
#         day_total_sum += float(row[2])
# tree_day_report.insert('', 0, values=())
# tree_day_report.insert('', 1, values=('', 'Наличност каса:', day_total_sum))
# tree_day_report.insert('', 2, values=())

glass_entry_window.mainloop()

