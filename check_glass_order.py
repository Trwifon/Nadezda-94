import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from _datetime import datetime

def get_data():
    connection = mysql.connector.connect(**dict_connection)
    cursor = connection.cursor()
    get_order = "SELECT firm, order_id, length, width, count, type, price, sum_count, sum_area, sum_total, " \
                "done FROM pvc_glass_orders WHERE order_id = %s AND done = 0"
    order_id = ('PXI-239',)
    cursor.execute(get_order, order_id)
    rows = cursor.fetchall()
    tree_order.insert('', 'end', values="Стара поръчка:")
    print(rows)
    for row in rows:
        tree_order.insert('', 'end', values=row)

        data_dictionary['firm'] =  row[0]
        data_dictionary['order'] =  row[1]
        data_dictionary['length'] =  int(row[2])
        data_dictionary['width'] =  int(row[3])
        data_dictionary['count'] =  int(row[4])
        data_dictionary['type'] =  row[5]
        data_dictionary['price'] =  float(row[6])
        data_dictionary['sum_count'] =  1
        data_dictionary['sum_area'] =  0.0
        data_dictionary['sum_total'] =  0.0
        data_dictionary['done'] =  row[10]
        order_list.append(data_dictionary.copy())
    record_dictionary['old_total'], record_dictionary['note'] = float(rows[-1][9]), rows[-1][1]

    get_firm_id_and_balance = "SELECT partner_id, partner_balance FROM partner WHERE partner_name = %s"
    firm = (data_dictionary['firm'],)
    cursor.execute(get_firm_id_and_balance, firm)
    partner = cursor.fetchall()
    record_dictionary['firm_id'], record_dictionary['open_balance'] = int(partner[0][0]), float(partner[0][1])
    print(record_dictionary)

    cursor.close()
    connection.close()
    return

def display_data(index):
    global order_list
    firm_label.configure(text = order_list[index]['firm'])
    order_label.configure(text = order_list[index]['order'])
    kind_entry.insert(0, order_list[index]['type'])
    length_entry.insert(0, order_list[index]['length'])
    width_entry.insert(0, order_list[index]['width'])
    count_entry.insert(0, order_list[index]['count'])
    price_entry.insert(0, order_list[index]['price'])
    return

def update_data_in_dictionary(current_index):
    order_list[index]['type'] = kind_entry.get()
    order_list[index]['length'] = int(length_entry.get())
    order_list[index]['width'] = int(width_entry.get())
    order_list[index]['count'] = int(count_entry.get())
    order_list[index]['price'] = float(price_entry.get())
    return

def clear_data():
    kind_entry.delete(0,30)
    length_entry.delete(0,30)
    width_entry.delete(0,30)
    count_entry.delete(0,30)
    price_entry.delete(0,30)
    return

def backward_button_press():
    global index, clear_data
    update_data_in_dictionary(index)
    index -= 1
    if index < 0:
        index = 0
    clear_data()
    display_data(index)
    return

def forward_button_press():
    global index
    update_data_in_dictionary(index)
    index += 1
    if index == len(order_list):
        index = len(order_list) - 1
    clear_data()
    display_data(index)
    return

def calculate_total():
    global change_flag
    for current_index in range(len(order_list)):
        current_area = order_list[current_index]['length'] * order_list[current_index]['width'] / 1000000
        if current_area <= 0.3:
            current_area = 0.3
        order_list[current_index]['sum_area'] += current_area * order_list[current_index]['count']
        order_list[current_index]['sum_count'] = order_list[current_index]['count']
        order_list[current_index]['sum_total'] = order_list[current_index]['sum_area'] * \
                                                 order_list[current_index]['price']
        if current_index > 0:
            order_list[current_index]['sum_count'] += order_list[current_index-1]['sum_count']
            order_list[current_index]['sum_total'] += order_list[current_index-1]['sum_total']
    record_dictionary['new_total'] =  order_list[-1]['sum_total']
    if record_dictionary['new_total'] != record_dictionary['old_total']:
        record_dictionary['change_amount'] = record_dictionary['new_total'] - record_dictionary['old_total']
        record_dictionary['close_balance'] = record_dictionary['open_balance'] + record_dictionary['change_amount']
        change_flag = True
    print(order_list)
    return change_flag

def update_db():
    connection = mysql.connector.connect(**dict_connection)
    cursor = connection.cursor()

    # mark order is updated
    data_update = "UPDATE pvc_glass_orders SET done = 2 WHERE order_id = %s"
    order_id = (order_list[0]['order'],)
    cursor.execute(data_update, order_id)

    #insert new order
    insert_orders = ("INSERT INTO pvc_glass_orders (firm, order_id, length, width, count, type, price, sum_count, "
                     "sum_area, sum_total, done) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    for index in range(len(order_list)):
        order_data = (
        order_list[index]['firm'], order_list[index]['order'], order_list[index]['length'], order_list[index]['width'],
        order_list[index]['count'], order_list[index]['type'], order_list[index]['price'],
        order_list[index]['sum_count'], order_list[index]['sum_area'], order_list[index]['sum_total'],
        order_list[index]['done'])
        cursor.execute(insert_orders, order_data)

    #update partner table
    update_partner = "UPDATE partner SET partner_balance = %s WHERE partner_id = %s"
    data_update_partner = (record_dictionary['close_balance'], record_dictionary['firm_id'])
    cursor.execute(update_partner, data_update_partner)

    #update records table
    insert_orders = ("INSERT INTO records (date, warehouse, partner_id, open_balance, order_type, ammount,"
                     " close_balance, note)"
                     "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
    order_data = (datetime.now().date(), 'Стъкла', record_dictionary['firm_id'], record_dictionary['open_balance'],
                  'Промяна', record_dictionary['change_amount'], record_dictionary['close_balance'],
                  record_dictionary['note'])
    cursor.execute(insert_orders, order_data)
    connection.commit()
    cursor.close()
    connection.close()

def ok_button_press():
    if calculate_total():
        update_db()
        




    return


dict_connection = {
    'host': '127.0.0.1',
    'port': '3306',
    'user': 'root',
    'password': 'Proba123+',
    'database': 'nadejda-94'
}
empty_data_dictionary = {'firm': '', 'order': '', 'length': 0, 'width': 0, 'count': 0, 'type': '', 'price': 0.0,
                   'sum_count': 0, 'sum_area': 0.0, 'sum_total': 0.0, 'done': False}
data_dictionary = empty_data_dictionary.copy()
order_list = []
empty_record_dictionary = {"firm_id": 0, "old_total": 0.0, "new_total": 0.0, "change_amount": 0.0, "open_balance": 0,
                           "close_balance": 0, "note": ''}
record_dictionary = empty_record_dictionary.copy()
index = 0
change_flag = False


# create entry window
check_glass_entry_window = tk.Tk()
check_glass_entry_window.title('Проверка на стъклопакетите')
check_glass_entry_window.geometry('1300x650')
def_font = tk.font.nametofont("TkDefaultFont")
def_font.config(size=20)
check_glass_entry_window.option_add('*TCombobox*Listbox.font', ('Helvetica', 15))

# first_row
firm_label = ttk.Label(check_glass_entry_window, width=20, anchor="c", font=('Helvetica', 20))
firm_label.grid(row=0, column=0, columnspan = 2, padx=10, pady=20)
firm_label.configure(background='Light Grey')
order_label = ttk.Label(check_glass_entry_window, width=8, anchor="c", font=('Helvetica', 20))
order_label.grid(row=0, column=2, columnspan = 2, padx=10, pady=20)
order_label.configure(background='Light Grey')

#second row
kind_entry = ttk.Entry(check_glass_entry_window, width=15, justify='center', font=('Helvetica', 20))
kind_entry.grid(row=1, column=0, columnspan = 2, sticky="we", padx=10, pady=20)

#third row
length_entry = ttk.Entry(check_glass_entry_window, width=4, justify='center', font=('Helvetica', 20))
length_entry.grid(row=2, column=0, padx=20, pady=20)
width_entry = ttk.Entry(check_glass_entry_window, width=4,justify='center', font=('Helvetica', 20))
width_entry.grid(row=2, column=1, padx=20, pady=20)
left_button = ttk.Button(check_glass_entry_window, width=4, text='<-', command=backward_button_press)
left_button.grid(row=2, column=2, sticky="w", padx=10, pady=20)
right_button = ttk.Button(check_glass_entry_window, width=4, text='->', command=forward_button_press)
right_button.grid(row=2, column=2, sticky="e", padx=10, pady=20)

#fourth row
count_entry = ttk.Entry(check_glass_entry_window, width=2, justify='center', font=('Helvetica', 20))
count_entry.grid(row=3, column=0, padx=10, pady=20)
price_entry = ttk.Entry(check_glass_entry_window, width=5,justify='center', font=('Helvetica', 20))
price_entry.grid(row=3, column=1, padx=10, pady=20)
ok_button = ttk.Button(check_glass_entry_window, width=8, text='OK', command=ok_button_press)
ok_button.grid(row=3, column=2, sticky="e", padx=30, pady=20)

# order
scrollbar = ttk.Scrollbar(check_glass_entry_window, orient=tk.VERTICAL)
tree_order = ttk.Treeview(check_glass_entry_window, height=30)
tree_order['show'] = 'headings'
scrollbar.configure(command=tree_order.yview)
tree_order.configure(yscrollcommand=scrollbar.set)
scrollbar.grid(row=0, rowspan=15, column=5, sticky="nsw")
tree_order.grid(row=0, rowspan=20, column=4, sticky='ne')
style = ttk.Style()
style.configure('Treeview', font=('Helvetica', 10))
tree_order['columns'] = ('firm', 'order', 'length', 'width', 'count', 'type', 'price', 'sum_count', 'sum_area',
                              'sum_total', 'done')
tree_order.column('firm', width=100, minwidth=50, anchor=tk.CENTER)
tree_order.column('order', width=60, minwidth=50, anchor=tk.CENTER)
tree_order.column('length', width=60, minwidth=50, anchor=tk.CENTER)
tree_order.column('width', width=60, minwidth=50, anchor=tk.CENTER)
tree_order.column('count', width=60, minwidth=50, anchor=tk.CENTER)
tree_order.column('type', width=60, minwidth=50, anchor=tk.CENTER)
tree_order.column('price', width=60, minwidth=50, anchor=tk.CENTER)
tree_order.column('sum_count', width=70, minwidth=50, anchor=tk.CENTER)
tree_order.column('sum_area', width=80, minwidth=50, anchor=tk.CENTER)
tree_order.column('sum_total', width=60, minwidth=50, anchor=tk.CENTER)
tree_order.column('done', width=80, minwidth=50, anchor=tk.CENTER)

tree_order.heading('firm', text='Фирма', anchor=tk.CENTER)
tree_order.heading('order', text='Поръчка', anchor=tk.CENTER)
tree_order.heading('length', text='Дължина', anchor=tk.CENTER)
tree_order.heading('width', text='Ширина', anchor=tk.CENTER)
tree_order.heading('count', text='Брой', anchor=tk.CENTER)
tree_order.heading('type', text='Вид', anchor=tk.CENTER)
tree_order.heading('price', text='Цена', anchor=tk.CENTER)
tree_order.heading('sum_count', text='Общ брой', anchor=tk.CENTER)
tree_order.heading('sum_area', text='Обща площ', anchor=tk.CENTER)
tree_order.heading('sum_total', text='Сума', anchor=tk.CENTER)
tree_order.heading('done', text='Изпълнено', anchor=tk.CENTER)

order_data = get_data()
display_data(index)





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


check_glass_entry_window.mainloop()





