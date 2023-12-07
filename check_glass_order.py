import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont



def get_data():
    connection = mysql.connector.connect(**dict_connection)
    cursor = connection.cursor()
    cursor.execute("SELECT firm, order_id, length, width, count, type, price, sum_count, sum_area, sum_total, "
                   "done FROM pvc_glass_orders WHERE order_id = 'PXI-239'")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    for row in rows:
        data_dictionary['firm'] =  row[0]
        data_dictionary['order'] =  row[1]
        data_dictionary['length'] =  int(row[2])
        data_dictionary['width'] =  int(row[3])
        data_dictionary['count'] =  int(row[4])
        data_dictionary['type'] =  row[5]
        data_dictionary['price'] =  float(row[6])
        data_dictionary['sum_count'] =  int(row[7])
        data_dictionary['sum_area'] =  float(row[8])
        data_dictionary['sum_total'] =  float(row[9])
        data_dictionary['done'] =  row[10]
        order_list.append(data_dictionary.copy())
    return

def display_data(index):
    global order_list
    count_rows = len(order_list)
    firm_label.configure(text = order_list[index]['firm'])
    order_label.configure(text = order_list[index]['order'])
    kind_entry.insert(0, order_list[index]['type'])
    length_entry.insert(0, order_list[index]['length'])
    width_entry.insert(0, order_list[index]['width'])
    count_entry.insert(0, order_list[index]['count'])
    price_entry.insert(0, order_list[index]['price'])

def update_data_in_dictionary(current_index):
    order_list[index]['type'] = kind_entry.get()
    order_list[index]['length'] = length_entry.get()
    order_list[index]['width'] = width_entry.get()
    order_list[index]['count'] = count_entry.get()
    order_list[index]['price'] = price_entry.get()

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



# def update_cb(event):
#     a = event.widget.get()
#     newvalues = [i for i in lst if a.lower() in i.lower()]
#     firm_cb['values'] = newvalues
#     firm_cb.focus()
#
# def ok_button_press(event = None):
#     data_dictionary['firm'] = firm_cb.get()
#     data_dictionary['order'] = f"{order_label['text']}{order_month_cb.get()}-{order_day_cb.get()}"
#     data_dictionary['length'], data_dictionary['width'], data_dictionary['count'] = \
#         int(length_entry.get()), int(width_entry.get()), int(count_entry.get())
#     if third_glass_cb.get() == "":
#         data_dictionary['type'] = f"{first_glass_cb.get()}+{second_glass_cb.get()}={tickness_cb.get()}"
#     else:
#         data_dictionary['type'] = f"{first_glass_cb.get()}+{second_glass_cb.get()}+{third_glass_cb.get()}=" \
#                                   f"{tickness_cb.get()}"
#     data_dictionary['price'] = float(price_entry.get())
#     data_dictionary['sum_count'] += int(count_entry.get())
#     current_area = data_dictionary['length'] * data_dictionary['width'] / 1000000
#     if current_area <= 0.3:
#         current_area = 0.3
#     data_dictionary['sum_area'] += current_area * int(count_entry.get())
#     data_dictionary['sum_total'] = data_dictionary['sum_area'] * data_dictionary['price']
#     order_list.append(data_dictionary.copy())
#     length_entry.focus_set()
#     length_entry.select_range(0, 4)
#     return
#
# def finish_button():
#     connection = mysql.connector.connect(**dict_connection)
#     cursor = connection.cursor()
#     insert_orders = ("INSERT INTO pvc_glass_orders (firm, order_id, length, width, count, type, price, sum_count, "
#                      "sum_area, sum_total, done) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
#     for index in range(len(order_list)):
#         order_data = (order_list[index]['firm'], 'proba', order_list[index]['length'], order_list[index]['width'],
#                       order_list[index]['count'], order_list[index]['type'], order_list[index]['price'],
#                       order_list[index]['sum_count'], order_list[index]['sum_area'], order_list[index]['sum_total'],
#                       order_list[index]['done'])
#         cursor.execute(insert_orders, order_data)
#         connection.commit()
#     cursor.close()
#     connection.close()
#     clear_form()
#     return
#
# def tab_order():
#     widgets = [firm_cb, order_month_cb, order_day_cb, first_glass_cb, second_glass_cb, third_glass_cb,
#                tickness_cb, price_entry, length_entry, width_entry, count_entry]
#     for element in widgets:
#         element.lift()
#     return
#
# def clear_form():
#     data_dictionary = empty_dictionary.copy()
#     firm_cb.set('')
#     first_glass_cb.set('')
#     tickness_cb.set('')
#     second_glass_cb.set('')
#     order_day_cb.set('')
#     third_glass_cb.set('')
#     price_entry.delete(0, 5)
#     price_entry.insert(0, 0)
#     length_entry.delete(0, 5)
#     length_entry.insert(0, 0)
#     width_entry.delete(0, 5)
#     width_entry.insert(0, 0)
#     count_entry.delete(0, 5)
#     count_entry.insert(0, 1)
#     return
#


empty_dictionary = {'firm': '', 'order': '', 'length': 0, 'width': 0, 'count': 0, 'type': '', 'price': 0.0,
                   'sum_count': 0, 'sum_area': 0.0, 'sum_total': 0.0, 'done': False}
data_dictionary = empty_dictionary.copy()
dict_connection = {
    'host': '127.0.0.1',
    'port': '3306',
    'user': 'root',
    'password': 'Proba123+',
    'database': 'nadejda-94'
}
order_list = []
index = 0

# create entry window
check_glass_entry_window = tk.Tk()
check_glass_entry_window.title('Проверка на стъклопакетите')
check_glass_entry_window.geometry('550x350')
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
# total_label = ttk.Label(check_glass_entry_window, width=10, text=('Сума'), anchor="c", font=('Helvetica', 20))
# total_label.grid(row=0, column=2, padx=10, pady=20)
# total_label.configure(background='Light Grey')

#second row
kind_entry = ttk.Entry(check_glass_entry_window, width=15, justify='center', font=('Helvetica', 20))
kind_entry.grid(row=1, column=0, columnspan = 2, sticky="we", padx=10, pady=20)
# total_entry = ttk.Entry(check_glass_entry_window, width=5, justify='center', font=('Helvetica', 20))
# total_entry.grid(row=1, column=2, sticky="we", padx=10, pady=20)




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
ok_button = ttk.Button(check_glass_entry_window, width=8, text='OK') #, command=ok_button_press
ok_button.grid(row=3, column=2, sticky="e", padx=30, pady=20)


order_data = get_data()
print(order_data)
display_data(index)

check_glass_entry_window.mainloop()





