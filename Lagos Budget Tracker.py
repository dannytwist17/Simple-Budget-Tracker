import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime
import os

transactions = []
filename = 'transactions.json'

# Load existing transactions if file exists
if os.path.exists(filename):
    with open(filename, 'r') as file:
        transactions = json.load(file)

def save_to_file():
    with open(filename, 'w') as file:
        json.dump(transactions, file, indent=4)

def update_balance_label():
    balance = sum(
        t['amount'] if t['type'] == 'income' else -t['amount']
        for t in transactions
    )
    balance_label.config(text=f'Current Balance: #{balance:.2f}')

def add_transaction(transaction_type):
    try:
        amount_text = amount_entry.get().strip()
        description = desc_entry.get().strip()

        if not amount_text:
            messagebox.showerror('Error', 'Please enter an amount.')
            return

        amount = float(amount_text)

        if amount <= 0:
            messagebox.showerror('Error', 'Amount must be greater than zero.')
            return

        if not description:
            messagebox.showerror('Error', 'Please enter a description.')
            return

        transaction = {
            'type': transaction_type,
            'amount': amount,
            'description': description,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        transactions.append(transaction)
        save_to_file()
        update_balance_label()
        messagebox.showinfo('Success', f'{transaction_type.title()} Added!')

        amount_entry.delete(0, tk.END)
        desc_entry.delete(0, tk.END)

    except ValueError:
        messagebox.showerror('Error', 'Please enter a valid number.')

def add_income():
    add_transaction('income')

def add_expense():
    add_transaction('expense')

def show_all_transactions():
    if not transactions:
        messagebox.showinfo('Transactions', 'No transactions yet.')
        return

    win = tk.Toplevel(root)
    win.title('All Transactions')
    win.geometry('600x400')

    text = tk.Text(win, wrap=tk.WORD)
    text.pack(expand=True, fill='both')

    text.insert(tk.END, 'Date\t\tType\tAmount\tDescription\n')
    text.insert(tk.END, '-' * 70 + '\n')

    for t in transactions:
        line = f'{t["date"]}\t{t["type"].title():<7}\t#{t["amount"]:.2f}\t{t["description"]}\n'
        text.insert(tk.END, line)

def reset_data():
    global transactions
    confirm = messagebox.askyesno("Confirm Reset", "Are you sure you want to reset all data?")
    if confirm:
        transactions = []
        if os.path.exists(filename):
            os.remove(filename)
        update_balance_label()
        messagebox.showinfo("Reset Complete", "All transactions have been cleared.")

root = tk.Tk()
root.title('Lagos Budget Tracker')
root.geometry('400x350')

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

tk.Label(frame, text='Amount:').grid(row=0, column=0, sticky='w', pady=5)
amount_entry = tk.Entry(frame, width=25)
amount_entry.grid(row=0, column=1, pady=5)

tk.Label(frame, text='Description:').grid(row=1, column=0, sticky='w', pady=5)
desc_entry = tk.Entry(frame, width=25)
desc_entry.grid(row=1, column=1, pady=5)

balance_label = tk.Label(frame, text='Current Balance: #0.00', font=('Arial', 12, 'bold'))
balance_label.grid(row=2, column=0, columnspan=2, pady=10)

add_income_button = tk.Button(frame, text="Add Income", width=20, command=add_income)
add_income_button.grid(row=3, column=0, pady=5, padx=5)

add_expense_button = tk.Button(frame, text="Add Expense", width=20, command=add_expense)
add_expense_button.grid(row=3, column=1, pady=5, padx=5)

balance_button = tk.Button(frame, text="View Balance", width=20, command=lambda: messagebox.showinfo('Balance', balance_label['text']))
balance_button.grid(row=4, column=0, pady=5, padx=5)

transactions_button = tk.Button(frame, text="Show All Transactions", width=20, command=show_all_transactions)
transactions_button.grid(row=4, column=1, pady=5, padx=5)

reset_button = tk.Button(frame, text="Reset Data", width=20, command=reset_data)
reset_button.grid(row=5, column=0, columnspan=2, pady=10)

update_balance_label()

root.mainloop()