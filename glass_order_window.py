import tkinter
import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import ttk
from datetime import datetime
import tkinter.font as tkFont

dict_connection = {
    'host': '127.0.0.1',
    'port': '3306',
    'user': 'root',
    'password': 'Proba123+',
    'database': 'nadejda-94'
}
list_glass = ['4', '5', 'K', '4S']
tickness = [12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 42, 44]
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



# create entry window
glass_entry_window = tk.Tk()
glass_entry_window.title('Форма за въвеждане на стъклопакети')
glass_entry_window.geometry('1250x500')
def_font = tk.font.nametofont("TkDefaultFont")
def_font.config(size=20)

# radio_var = tkinter.IntVar()
glass_entry_window.option_add('*TCombobox*Listbox.font', ('Helvetica', 15))

# first_row
firm_label = ttk.Label(glass_entry_window, width=20, text=('Фирма'), anchor="c", font=('Helvetica', 20))
firm_label.grid(row=0, columnspan = 2, column=0, padx=10, pady=20)
firm_label.configure(background='Light Grey')
kind_label = ttk.Label(glass_entry_window, width=20, text=('Вид'), anchor="c", font=('Helvetica', 20))
kind_label.grid(row=0, column=4, padx=10, pady=20)
kind_label.configure(background='Light Grey')
tickness_label = ttk.Label(glass_entry_window, width=10, text=('Дебелина'), anchor="c", font=('Helvetica', 20))
tickness_label.grid(row=0, column=5, padx=20, pady=20)
tickness_label.configure(background='Light Grey')

#second row
firm_list = list_combobox()
firm_cb = ttk.Combobox(glass_entry_window, width=25, values=firm_list, font=('', 20), height=20)
firm_cb.grid(row=1, columnspan = 2, column=0, sticky="w", padx=20, pady=20)
# firm_cb.bind('<KeyRelease>', update_cb)
# firm_cb.bind('<<ComboboxSelected>>', getSelectedItem)
first_glass = ttk.Label(glass_entry_window, width=15, text=('Първо стъкло'), anchor="c", font=('Helvetica', 20))
first_glass.grid(row=1, column=2, padx=10, pady=20)
first_glass.configure(background='Light Grey')
first_glass_cb = ttk.Combobox(glass_entry_window, width=15, values=list_glass, font=('', 20), height=20)
first_glass_cb.grid(row=1, column=4, sticky="ew", padx=20, pady=20)
tickness_cb = ttk.Combobox(glass_entry_window, width=3, values=tickness, font=('', 20), height=20)
tickness_cb.grid(row=1, column=5, sticky="ew", padx=60, pady=20)

#third row
order_label = ttk.Label(glass_entry_window, width=20, text=('Поръчка'), anchor="c", font=('Helvetica', 20))
order_label.grid(row=2, columnspan = 2, column=0, padx=20, pady=20)
order_label.configure(background='Light Grey')
second_glass = ttk.Label(glass_entry_window, width=15, text=('Второ стъкло'), anchor="c", font=('Helvetica', 20))
second_glass.grid(row=2, column=2, padx=10, pady=20)
second_glass.configure(background='Light Grey')
second_glass_cb = ttk.Combobox(glass_entry_window, width=15, values=list_glass, font=('', 20), height=20)
second_glass_cb.grid(row=2, column=4, sticky="ew", padx=20, pady=20)
price_label = ttk.Label(glass_entry_window, width=10, text=('Цена'), anchor="c", font=('Helvetica', 20))
price_label.grid(row=2, column=5, padx=20, pady=20)
price_label.configure(background='Light Grey')

#fourth row

third_glass = ttk.Label(glass_entry_window, width=15, text=('Трето стъкло'), anchor="c", font=('Helvetica', 20))
third_glass.grid(row=3, column=2, padx=10, pady=20)
third_glass.configure(background='Light Grey')
third_glass_cb = ttk.Combobox(glass_entry_window, width=15, values=list_glass, font=('', 20), height=20)
third_glass_cb.grid(row=3, column=4, sticky="ew", padx=20, pady=20)
price_entry = ttk.Entry(glass_entry_window, width=3, font=('Helvetica', 20))
price_entry.grid(row=3, column=5, sticky="ew", padx=50)

#fifth row
length = ttk.Label(glass_entry_window, width=15, text=('Първи размер'), anchor="c", font=('Helvetica', 20))
length.grid(row=4, columnspan = 1, column=0, padx=10, pady=20)
length.configure(background='Light Grey')
width = ttk.Label(glass_entry_window, width=15, text=('Втори размер'), anchor="c", font=('Helvetica', 20))
width.grid(row=4, columnspan = 2, column=1, padx=10, pady=20)
width.configure(background='Light Grey')

#sixth row
length_entry = ttk.Entry(glass_entry_window, width=5, font=('Helvetica', 50))
length_entry.grid(row=5, column=0, sticky="ew", padx=100, pady=20)
width_entry = ttk.Entry(glass_entry_window, width=4, font=('Helvetica', 50))
width_entry.grid(row=5, columnspan = 1, column=2, sticky="ew", padx=40, pady=20)




# order_radio = ttk.Radiobutton(glass_entry_window, text="Поръчка", variable=radio_var, value=1, command=sel)
# order_radio.grid(row=3, column=0, sticky="w", padx=40)
# cash_radio = ttk.Radiobutton(glass_entry_window, text="Каса", variable=radio_var, value=0, command=sel)
# cash_radio.grid(row=4, column=0, sticky="w", padx=40)
# bank_radio = ttk.Radiobutton(glass_entry_window, text="Банка", variable=radio_var, value=2, command=sel)
# bank_radio.grid(row=5, column=0, sticky="w", padx=40)
#
# open_balance_label = ttk.Label(glass_entry_window, width=10, text='', font=('Helvetica', 20))
# open_balance_label.grid(row=2, column=1, sticky="e", padx=40)
# open_balance_label_text = ttk.Label(glass_entry_window, text='Hачално салдо:', font=('Helvetica', 20))
# open_balance_label_text.grid(row=2, column=1, sticky="w", padx=40)
# close_balance_label = ttk.Label(glass_entry_window, width=10, text='', font=('Helvetica', 20))
# close_balance_label.grid(row=6, column=1, sticky="e", padx=40)
# close_balance_label_text = ttk.Label(glass_entry_window, text='Крайно салдо:', font=('Helvetica', 20))
# close_balance_label_text.grid(row=6, column=1, sticky="w", padx=40)
#
# amount_entry = ttk.Entry(glass_entry_window, width=10, font=('Helvetica', 20))
# amount_entry.grid(row=4, column=1, sticky="w", padx=40)
# amount_entry.bind('<KeyRelease>', update_close_balance)
#
# note_label = ttk.Label(glass_entry_window, text='Забележка:', font=('Helvetica', 20))
# note_label.grid(row=8, column=0, padx=40, pady=20)
# note_entry = ttk.Entry(glass_entry_window, width=25, font=('Helvetica', 20))
# note_entry.grid(row=8, column=1, sticky="w", padx=40)
#
# new_firm_button = ttk.Button(glass_entry_window, width=18, text='Нова фирма', command=new_firm)
# new_firm_button.grid(row=9, columnspan=2, column=0, sticky="w", padx=45, pady=20)
# firm_report_button = ttk.Button(glass_entry_window, width=18, text='Фирмен отчет', command=firm_report)
# firm_report_button.grid(row=9, columnspan=2, column=0, sticky="e", padx=40, pady=20)
# ok_button = ttk.Button(glass_entry_window, width=8, text='OK', command=ok_button)
# ok_button.grid(row=10, columnspan=2, column=0, sticky="w", padx=192, pady=20)
# cancel_button = ttk.Button(glass_entry_window, width=8, text='Cancel', command=glass_entry_window.destroy)
# cancel_button.grid(row=10, columnspan=2, column=0, sticky="e", padx=190, pady=20)
#
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


# разгъване на комбобокс при въвеждане
# архивиране и изпращане на базата данни
# Connection db at the begining - only one and write it in the heading -close db automaticaly efter 10 hours