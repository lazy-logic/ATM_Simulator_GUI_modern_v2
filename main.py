# An ATM Simulator GUI using python, tkinter, ttkbootstrap
# Code by Michael Abraham alias Lazy.Logic
#########################################################################################
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox, Querybox
from PIL import Image, ImageTk
from datetime import datetime

# ---------- Dummy Accounts ----------
accounts = {"112211": 1000.0, "223322": 2500.0, "334455": 3000.0}

# ---------- Transaction Log ----------
transactions = []


# ---------- Functions ----------
def log_transaction(action, detail):
    """Save each transaction with timestamp"""
    time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    transactions.append(f"[{time_str}] {action}: {detail}")


def get_account_number():
    return account_number_entry.get().strip()


def check_balance():
    acc = get_account_number()
    if acc in accounts:
        Messagebox.show_info(f"Balance: ${accounts[acc]:.2f}", "ATM Simulator")
        log_transaction("Balance Check", f"Account {acc} balance ${accounts[acc]:.2f}")
    else:
        Messagebox.show_warning("Account not found.", "ATM Simulator")


def deposit():
    acc = get_account_number()
    if acc in accounts:
        amount = Querybox.get_float("Deposit", "Enter amount to deposit:")
        if amount and amount > 0:
            accounts[acc] += amount
            Messagebox.show_info(
                f"Deposited ${amount:.2f}\nNew Balance: ${accounts[acc]:.2f}",
                "ATM Simulator"
            )
            log_transaction("Deposit", f"Account {acc} deposited ${amount:.2f}")
        else:
            Messagebox.show_warning("Invalid amount.", "ATM Simulator")
    else:
        Messagebox.show_warning("Account not found.", "ATM Simulator")


def withdraw():
    acc = get_account_number()
    if acc in accounts:
        amount = Querybox.get_float("Withdraw", "Enter amount to withdraw:")
        if amount and amount > 0:
            if accounts[acc] >= amount:
                accounts[acc] -= amount
                Messagebox.show_info(
                    f"Withdrew ${amount:.2f}\nNew Balance: ${accounts[acc]:.2f}",
                    "ATM Simulator"
                )
                log_transaction("Withdraw", f"Account {acc} withdrew ${amount:.2f}")
            else:
                Messagebox.show_warning("Insufficient funds.", "ATM Simulator")
        else:
            Messagebox.show_warning("Invalid amount.", "ATM Simulator")
    else:
        Messagebox.show_warning("Account not found.", "ATM Simulator")


def transfer():
    acc = get_account_number()
    if acc in accounts:
        receiver = Querybox.get_string("Transfer", "Enter receiver account number (10 digits):")
        if receiver and receiver.isdigit() and len(receiver) == 10:
            amount = Querybox.get_float("Transfer", "Enter amount to transfer:")
            if amount and amount > 0:
                if accounts[acc] >= amount:
                    accounts[acc] -= amount
                    accounts[receiver] = accounts.get(receiver, 0) + amount
                    Messagebox.show_info(
                        f"Transferred ${amount:.2f} to {receiver}\n"
                        f"Your New Balance: ${accounts[acc]:.2f}\n"
                        f"Receiver's Balance: ${accounts[receiver]:.2f}",
                        "ATM Simulator"
                    )
                    log_transaction("Transfer", f"From {acc} to {receiver}: ${amount:.2f}")
                else:
                    Messagebox.show_warning("Insufficient funds.", "ATM Simulator")
            else:
                Messagebox.show_warning("Invalid amount.", "ATM Simulator")
        else:
            Messagebox.show_warning("Invalid receiver account number.", "ATM Simulator")
    else:
        Messagebox.show_warning("Account not found.", "ATM Simulator")

def quit_and_print_receipt():
    """Save and show receipt before quitting with fancy ATM slip formatting"""
    if not transactions:
        Messagebox.show_info("No transactions made.", "ATM Simulator")
    else:
        # ATM Slip Header
        receipt_lines = [
            "===============================",
            "        ATM RECEIPT SLIP       ",
            "===============================",
            f"DATE: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "-------------------------------",
            "TRANSACTIONS:"
        ]

        # Add each transaction neatly
        for t in transactions:
            receipt_lines.append(f"  {t}")

        receipt_lines.append("-------------------------------")
        receipt_lines.append("FINAL BALANCES:")

        # Align balances nicely
        for acc, bal in accounts.items():
            receipt_lines.append(f"  Account {acc:<12} | ${bal:>8.2f}")

        receipt_lines.append("===============================")
        receipt_lines.append("  THANK YOU FOR USING OUR ATM  ")
        receipt_lines.append("===============================")

        # Convert list into one string
        receipt_text = "\n".join(receipt_lines)

        # Save to file
        with open("atm_receipt.txt", "w") as f:
            f.write(receipt_text)

        # Show preview
        Messagebox.show_info(receipt_text, "ATM Receipt")

    root.quit()



# ---------- GUI ----------
root = ttk.Window(themename="cosmo")
root.title("ATM Simulator")
root.geometry("800x600")
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

# --- Background Image ---
try:
    image_path = r"ATM_Simulator_GUI/atm-bg.jpg"
    bg_image = Image.open(image_path)
    bg_image = bg_image.resize((900, 600))
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = ttk.Label(root, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)
except Exception:
    root.config(bg="#b9cef5")

# --- Frame ---
frame = ttk.Frame(root, padding=20, bootstyle="light")
frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8, relheight=0.8)

# Title
title_label = ttk.Label(frame, text="ATM Simulator", font=("Arial", 14, "bold"))
title_label.pack(pady=10)

# Account Entry
entry_frame = ttk.Frame(frame)
entry_frame.pack(pady=10)
ttk.Label(entry_frame, text="Enter Account Number:").pack(side="left", padx=5)
account_number_entry = ttk.Entry(entry_frame, width=25)
account_number_entry.pack(side="left", padx=5)

# Buttons
btn_frame = ttk.Frame(frame)
btn_frame.pack(pady=20, fill="both", expand=True)

check_btn = ttk.Button(btn_frame, text="Check Balance", command=check_balance, bootstyle="primary-outline")
deposit_btn = ttk.Button(btn_frame, text="Deposit", command=deposit, bootstyle="success-outline")
withdraw_btn = ttk.Button(btn_frame, text="Withdraw", command=withdraw, bootstyle="warning-outline")
transfer_btn = ttk.Button(btn_frame, text="Transfer", command=transfer, bootstyle="info-outline")
quit_btn = ttk.Button(frame, text="Logout & Print Receipt", command=quit_and_print_receipt, bootstyle="danger")

# Arrange buttons in grid
btns = [check_btn, deposit_btn, withdraw_btn, transfer_btn]
for i, btn in enumerate(btns):
    btn.grid(row=i // 2, column=i % 2, padx=15, pady=15, sticky="nsew")
    btn_frame.grid_rowconfigure(i // 2, weight=1)
    btn_frame.grid_columnconfigure(i % 2, weight=1)

quit_btn.pack(pady=10, ipadx=10, ipady=5)

root.mainloop()
