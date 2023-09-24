import tkinter
import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import ttk
from datetime import datetime
import tkinter.font as tkFont

total_sum = 0.0
dict_connection = {
    'host': '127.0.0.1',
    'port': '3306',
    'user': 'root',
    'password': '++++',
    'database': 'nadejda-94'
}

# get balance of firms from database
def get_open_balance():
    firm = (firm_cb.get(),)
    if firm == 'Клиент' or firm == 'Доставчик':
        open_balance = 0
    else:
        connection = mysql.connector.connect(**dict_connection)
        cursor = connection.cursor()
        sql = "SELECT partner_balance FROM partner WHERE partner_name = %s"
        cursor.execute(sql, firm)
        open_balance = cursor.fetchone()
        cursor.close()
        connection.close()
    return open_balance

# get id of firms from database
def get_id():
    connection = mysql.connector.connect(**dict_connection)
    cursor = connection.cursor()
    partner_number = "SELECT partner_id FROM partner WHERE partner_name = %s"
    firm = (firm_cb.get(),)
    cursor.execute(partner_number, firm)
    p_id = cursor.fetchone()
    cursor.close()
    connection.close()
    return p_id

# get order type
def get_order_type():
    global order_type
    selection = radio_var.get()
    if selection == 1:
        order_type = 'Поръчка'
    elif selection == 0:
        order_type = 'Каса'
    elif selection == 2:
        order_type = 'Банка'
    return order_type

# get pvc order
def get_pvc_order():
    date = datetime.now().month
    month_dict = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V", 6: "VI", 7: "VII", 8: "VIII", 9: "IX", 10: "X", 11: "XI",
                  12: "XII"}
    current_month = month_dict[date]
    connection = mysql.connector.connect(**dict_connection)
    cursor = connection.cursor()
    cursor.execute("SELECT month, pvc_counter FROM orders")
    record = cursor.fetchone()
    month = record[0]
    pvc_counter = record[1]
    if current_month != month:
        insert_month = ("UPDATE orders SET month = %s, pvc_counter = %s")
        curr_month = (current_month, 1,)
        cursor.execute(insert_month, curr_month)
        pvc_counter = 1
    connection.commit()
    cursor.close()
    connection.close()
    pvc_order = (f"P-{current_month}-{pvc_counter}")
    return pvc_order

# convert tuple to float number
def tuple_to_float(tpl):
    str_balance = str(tpl)
    length = len(str_balance)
    float_balance = ''
    for i in range(0, length):
        if 47 < ord(str_balance[i]) < 58 or 44 < ord(str_balance[i]) < 47:
            float_balance = float_balance + str_balance[i]
    return float(float_balance)

# filter list of combobox when writing
def update_cb(event):
    a = event.widget.get()
    newvalues = []
    # newvalues = [i for i in lst if a in i]
    for i in lst:
        if a.lower() in i.lower():
            newvalues.append(i)
    firm_cb['values'] = newvalues
    firm_cb.focus()

# get name of firms from database for combobox
def list_combobox():
    connection = mysql.connector.connect(**dict_connection)
    cursor = connection.cursor()
    cursor.execute("SELECT partner_name FROM partner")
    rows = cursor.fetchall()
    lst = [i[0] for i in rows]
    lst.sort()
    cursor.close()
    connection.close()
    return lst

# input open balance of selected firm in balance label
def getSelectedItem(event):
    open_balance = get_open_balance()
    close_balance_label['text'] = ''
    ammount_entry.delete(0, 'end')
    open_balance_label['text'] = open_balance

# change selected radio button
def sel():
    selection = radio_var.get()
    ammount_entry.delete(0, 'end')
    close_balance_label['text'] = ''
    if selection == 1:
        note_entry.insert(0, get_pvc_order())
    else:
        note_entry.delete(0, 'end')
    return selection

# calculate close balance depending of radio button slection
def update_close_balance(event):
    firm = firm_cb.get()
    if firm == 'Клиент' or firm == 'Доставчик':
        close_balance_label['text'] = 0.0
    else:
        if open_balance_label.cget('text') != '' and ammount_entry.get() != '':
            float_open_balance = tuple_to_float(get_open_balance())
            ammount = ammount_entry.get()
            float_ammount = tuple_to_float(ammount)
            if radio_var.get() == 1:
                close_balance = float_open_balance - float_ammount
                close_balance_label['text'] = close_balance
            else:
                close_balance = float_open_balance + float_ammount
                close_balance_label['text'] = close_balance
        else:
            close_balance_label['text'] = ''

# show firm report
def firm_report():
    connection = mysql.connector.connect(**dict_connection)
    cursor = connection.cursor()

    partner_number = "SELECT partner_id FROM partner WHERE partner_name = %s"
    firm = (firm_cb.get(),)
    cursor.execute(partner_number, firm)
    p_id = cursor.fetchone()
    f_report = ("SELECT records.date, records.warehouse, partner.partner_name, records.open_balance,"
                " records.order_type, records.ammount, records.close_balance, records.note FROM records INNER"
                " JOIN partner ON records.partner_id = partner.partner_id"
                " WHERE records.partner_id = %s")
    cursor.execute(f_report, p_id)
    firm_report = cursor.fetchall()
    cursor.close()
    connection.close()

    firm_report_window = tk.Tk()
    firm_report_window.title('Справка за фирма')
    firm_report_window.geometry('750x630')
    def_font = tk.font.nametofont("TkDefaultFont")
    def_font.config(size=20)
    scrollbar = ttk.Scrollbar(firm_report_window, orient=tk.VERTICAL)
    tree_firm_report = ttk.Treeview(firm_report_window, height=25)
    scrollbar.configure(command=tree_firm_report.yview)
    tree_firm_report.configure(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=0, rowspan=10, column=5, sticky="nsw")
    tree_firm_report.grid(row=0, rowspan=20, column=0, sticky='nw')
    style = ttk.Style()
    style.configure('Treeview', font=('Helvetica', 9))
    tree_firm_report['columns'] = ('date', 'warehouse', 'firm', 'open_balance', 'order_type', 'ammount', 'close_balance', 'note')
    tree_firm_report.column('#0', width=0)
    tree_firm_report.column('date', width=100, minwidth=20, anchor=tk.CENTER)
    tree_firm_report.column('warehouse', width=50, minwidth=50, anchor=tk.CENTER)
    tree_firm_report.column('firm', width=120, minwidth=50, anchor=tk.CENTER)
    tree_firm_report.column('open_balance', width=20, minwidth=50, anchor=tk.CENTER)
    tree_firm_report.column('order_type', width=80, minwidth=50, anchor=tk.CENTER)
    tree_firm_report.column('ammount', width=50, minwidth=50, anchor=tk.CENTER)
    tree_firm_report.column('close_balance', width=50, minwidth=50, anchor=tk.CENTER)
    tree_firm_report.column('note', width=250, minwidth=50, anchor=tk.CENTER)

    tree_firm_report.heading('date', text='Дата', anchor=tk.CENTER)
    tree_firm_report.heading('warehouse', text='Склад', anchor=tk.CENTER)
    tree_firm_report.heading('firm', text='Фирма', anchor=tk.CENTER)
    tree_firm_report.heading('open_balance', text='Преди', anchor=tk.CENTER)
    tree_firm_report.heading('order_type', text='Вид запис', anchor=tk.CENTER)
    tree_firm_report.heading('ammount', text='Сума', anchor=tk.CENTER)
    tree_firm_report.heading('close_balance', text='След', anchor=tk.CENTER)
    tree_firm_report.heading('note', text='Забележка', anchor=tk.CENTER)
    total_sum = 0.0
    for row in firm_report:
        tree_firm_report.insert('', 'end', values=row)
        total_sum = float(row[6])
    tree_firm_report.insert('', 0, values=())
    tree_firm_report.insert('', 1, values=('', 'Крайно салдо:', total_sum))
    tree_firm_report.insert('', 2, values=())
    tree_firm_report.mainloop()

# write in database end close entry_window
def ok_button():
    global total_sum
    insert_orders = ("INSERT INTO records (date, warehouse, partner_id, open_balance, order_type, ammount,"
                     " close_balance, note)"
                     "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
    partner_id = int(tuple_to_float(get_id()))
    if partner_id == 1:
        partner_open_balance = 0.0
        partner_close_balance = 0.0
    else:
        partner_open_balance = tuple_to_float(open_balance_label.cget('text'))
        partner_close_balance = close_balance_label.cget('text')
    order_type = get_order_type()
    partner_ammount = ammount_entry.get()

    note = note_entry.get()
    order_data = (current_date, 1, partner_id, partner_open_balance, order_type, partner_ammount,
                  partner_close_balance, note)

    insert_partner = "UPDATE partner SET partner_balance = %s WHERE partner_id = %s"
    partner_data = (partner_close_balance, partner_id,)

    connection = mysql.connector.connect(host='127.0.0.1', port='3306', user='root', password='jabbour',
                                         database='nadejda-94')
    cursor = connection.cursor()
    cursor.execute(insert_orders, order_data)
    cursor.execute(insert_partner, partner_data)

    if order_type == 'Поръчка':
        cursor.execute("SELECT pvc_counter FROM orders")
        pvc_counter = tuple_to_float(cursor.fetchone())
        pvc_counter += 1
        insert_pvc_count = "UPDATE orders SET pvc_counter = %s"
        current_counter = (pvc_counter,)
        cursor.execute(insert_pvc_count, current_counter)
    connection.commit()
    cursor.close()
    connection.close()

    tree_day_report.insert('', 'end', values=(firm_cb.get(), order_type, partner_ammount, note))
    if order_type == 'Каса':
        total_sum += float(partner_ammount)
        selected_item = tree_day_report.get_children()[1]
        tree_day_report.delete(selected_item)
        tree_day_report.insert('', 1, values=('', 'Наличност каса:', total_sum))

    firm_cb.set('')
    open_balance_label['text'] = ''
    ammount_entry.delete(0, 'end')
    close_balance_label['text'] = ''
    note_entry.delete(0, 'end')

# create entry window
entry_window = tk.Tk()
entry_window.title('Форма за въвеждане')
entry_window.geometry('1500x630')
def_font = tk.font.nametofont("TkDefaultFont")
def_font.config(size=20)

radio_var = tkinter.IntVar()

warehouse = 'Склад 1'
warehouse_label = ttk.Label(entry_window, width=10, text=warehouse, anchor="c", font=('Helvetica', 20))
warehouse_label.grid(row=0, column=0, padx=40, pady=20)
warehouse_label.configure(background='Light Grey')

current_date = datetime.now()
current_date_str = str(current_date.date())
date_label = ttk.Label(entry_window, width=20, text=(current_date_str), anchor="c", font=('Helvetica', 20))
date_label.grid(row=0, column=1)

date_label.configure(background='Light Grey')

firm_label = ttk.Label(entry_window, text='Фирма', font=('Helvetica', 20))
firm_label.grid(row=1, column=0, padx=40, pady=5)

lst = list_combobox()
firm_cb = ttk.Combobox(entry_window, width=25, values=lst, font=('', 20))
firm_cb.grid(row=1, column=1, sticky="w", padx=40, pady=20)
entry_window.option_add('*TCombobox*Listbox.font', ('Helvetica', 15))
firm_cb.bind('<KeyRelease>', update_cb)
firm_cb.bind('<<ComboboxSelected>>', getSelectedItem)

order_radio = ttk.Radiobutton(entry_window, text="Поръчка", variable=radio_var, value=1, command=sel)
order_radio.grid(row=3, column=0, sticky="w", padx=40)
cash_radio = ttk.Radiobutton(entry_window, text="Каса", variable=radio_var, value=0, command=sel)
cash_radio.grid(row=4, column=0, sticky="w", padx=40)
bank_radio = ttk.Radiobutton(entry_window, text="Банка", variable=radio_var, value=2, command=sel)
bank_radio.grid(row=5, column=0, sticky="w", padx=40)

open_balance_label = ttk.Label(entry_window, width=10, text='', font=('Helvetica', 20))
open_balance_label.grid(row=2, column=1, sticky="e", padx=40)
open_balance_label_text = ttk.Label(entry_window, text='Hачално салдо:', font=('Helvetica', 20))
open_balance_label_text.grid(row=2, column=1, sticky="w", padx=40)
close_balance_label = ttk.Label(entry_window, width=10, text='', font=('Helvetica', 20))
close_balance_label.grid(row=6, column=1, sticky="e", padx=40)
close_balance_label_text = ttk.Label(entry_window, text='Крайно салдо:', font=('Helvetica', 20))
close_balance_label_text.grid(row=6, column=1, sticky="w", padx=40)

ammount_entry = ttk.Entry(entry_window, width=10, font=('Helvetica', 20))
ammount_entry.grid(row=4, column=1, sticky="w", padx=40)
ammount_entry.bind('<KeyRelease>', update_close_balance)

note_label = ttk.Label(entry_window, text='Забележка:', font=('Helvetica', 20))
note_label.grid(row=8, column=0, padx=40, pady=20)
note_entry = ttk.Entry(entry_window, width=25, font=('Helvetica', 20))
note_entry.grid(row=8, column=1, sticky="w", padx=40)

firm_report_button = ttk.Button(entry_window, width=18, text='Фирмен отчет', command=firm_report)
firm_report_button.grid(row=9, columnspan=2, column=0, sticky="e", padx=40, pady=20)
ok_button = ttk.Button(entry_window, width=8, text='OK', command=ok_button)
ok_button.grid(row=10, columnspan=2, column=0, sticky="w", padx=200, pady=20)
cancel_button = ttk.Button(entry_window, width=8, text='Cancel', command=entry_window.destroy)
cancel_button.grid(row=10, columnspan=2, column=0, sticky="e", padx=200, pady=20)

# day_report
scrollbar = ttk.Scrollbar(entry_window, orient=tk.VERTICAL)
tree_day_report = ttk.Treeview(entry_window, height=30)
tree_day_report['show'] = 'headings'
scrollbar.configure(command=tree_day_report.yview)
tree_day_report.configure(yscrollcommand=scrollbar.set)
scrollbar.grid(row=0, rowspan=15, column=5, sticky="nsw")
tree_day_report.grid(row=0, rowspan=20, column=4, sticky='ne')
style = ttk.Style()
style.configure('Treeview', font=('Helvetica', 10))
tree_day_report['columns'] = ('firm', 'action', 'ammount', 'note')
tree_day_report.column('firm', width=150, minwidth=50, anchor=tk.CENTER)
tree_day_report.column('action', width=100, minwidth=50, anchor=tk.CENTER)
tree_day_report.column('ammount', width=80, minwidth=50, anchor=tk.CENTER)
tree_day_report.column('note', width=420, minwidth=50, anchor=tk.CENTER)
tree_day_report.heading('firm', text='Фирма', anchor=tk.CENTER)
tree_day_report.heading('action', text='Действие', anchor=tk.CENTER)
tree_day_report.heading('ammount', text='Сума', anchor=tk.CENTER)
tree_day_report.heading('note', text='Забележка', anchor=tk.CENTER)
connection = mysql.connector.connect(**dict_connection)
cursor = connection.cursor()
cursor.execute("SELECT partner.partner_name, records.order_type, records.ammount, records.note FROM records INNER"
               " JOIN partner ON records.partner_id = partner.partner_id"
               " WHERE warehouse = 1 and date = current_date")
today_orders = cursor.fetchall()
cursor.close()
connection.close()
for row in today_orders:
    tree_day_report.insert('', 'end', values=row)
    if row[1] == 'Каса':
        total_sum += float(row[2])
tree_day_report.insert('', 0, values=())
tree_day_report.insert('', 1, values=('', 'Наличност каса:', total_sum))
tree_day_report.insert('', 2, values=())

entry_window.mainloop()


# Да се отдели фирмен отчет в нов прозорец
# Да се отделят аргументите на connection на едно място
