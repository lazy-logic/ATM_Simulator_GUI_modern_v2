from tkinter import Tk, Button, Label, messagebox
import csv
from tkinter import messagebox

from pymongo import MongoClient
from datetime import datetime

# Connect to local MongoDB (default port 27017)
client = MongoClient("mongodb://localhost:27017/")

# Use database "ATMdb" and collection "transactions"
db = client["ATMdb"]
transactions_collection = db["transactions"]



# ✅ All functions now accept accounts and account_number as arguments
def check_balance(accounts, account_number):
    if account_number in accounts:
        balance = accounts[account_number]
        messagebox.showinfo("ATM Simulator", f"Account Number: {account_number}\nBalance: ${balance:.2f}")
    else:
        messagebox.showwarning("ATM Simulator", "Account not found.")

def deposit(accounts, account_number, amount=100):  # demo: default deposit 100
    if account_number in accounts:
        accounts[account_number] += amount
        messagebox.showinfo("ATM Simulator", f"Deposited ${amount:.2f} into account {account_number}\nNew Balance: ${accounts[account_number]:.2f}")
    else:
        messagebox.showwarning("ATM Simulator", "Account not found.")

def withdraw(accounts, account_number, amount=50):  # demo: default withdraw 50
    if account_number in accounts:
        if accounts[account_number] >= amount:
            accounts[account_number] -= amount
            messagebox.showinfo("ATM Simulator", f"Withdrew ${amount:.2f} from account {account_number}\nNew Balance: ${accounts[account_number]:.2f}")
        else:
            messagebox.showwarning("ATM Simulator", "Insufficient funds.")
    else:
        messagebox.showwarning("ATM Simulator", "Account not found.")

def transfer(accounts, from_account, to_account, amount):
    if from_account not in accounts:
        messagebox.showwarning("ATM Simulator", "Source account not found.")
        return
    if to_account not in accounts:
        messagebox.showwarning("ATM Simulator", "Target account not found.")
        return
    if accounts[from_account] < amount:
        messagebox.showwarning("ATM Simulator", "Insufficient funds.")
        return
    
    # process transfer
    accounts[from_account] -= amount
    accounts[to_account] += amount
    messagebox.showinfo("ATM Simulator", 
        f"Transferred ${amount:.2f} from {from_account} to {to_account}\n"
        f"New Balance: ${accounts[from_account]:.2f}"
    )
# Load accounts from CSV file
