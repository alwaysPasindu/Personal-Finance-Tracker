import tkinter as tk
from tkinter import ttk
import json
from datetime import datetime

# Global variable to store transactions
transactions = {}

# File handling functions
filename = "json_data.json"


# Function to load transactions from JSON
def load_transactions():
    global transactions
    try:
        with open(filename, "r") as file:
            transactions = json.load(file)  # Open a JSON file and load the transactions.
    except FileNotFoundError:
        print("No transactions found.")


# Function to save transactions to JSON
def save_transactions():
    with open(filename, "w") as file:
        json.dump(transactions, file, indent=4, default=str)  # Store transactions with indentation in a JSON file.
        print("Transaction Saved Successfully.!")


# Function to read bulk transactions from file
def read_bulk_transactions_from_file(filename):
    global transactions
    try:
        with open(filename, 'r') as file:
            data = json.load(file)  # Load information from the given file
            for transaction in data:
                try:
                    expense_type = transaction.get("type")
                    if expense_type is None:
                        print("Skipping transaction without type information:", transaction)
                        continue
                    transactions.setdefault(expense_type, []).append(transaction)
                except AttributeError:
                    print("Error parsing transaction:", transaction)
    except FileNotFoundError:
        print("File can not found.")  # Take action if the file is missing.


# Function to add a transaction
def add_transaction():
    while True:
        expense_type = input("Enter expense type: ")
        try:
            amount = float(input("Enter amount: "))
            break  # Exit the loop if the amount input is successfully converted to float
        except ValueError:
            print("Please Enter a Valid Amount.!")
            continue
    while True:
        date_str = input("Enter date (YYYY-MM-DD): ")
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            break
        except ValueError:
            print("Please Enter a Valid Date in YYYY-MM-DD format.!")
            continue
    transaction = {"amount": amount, "date": date}
    transactions.setdefault(expense_type, []).append(transaction)  # Append a new transaction to the dictionary
    print("Transaction added successfully.")


# Function to view all transactions
def view_transactions():
    global transactions  # Call the global variable using the global function
    for expense_type, expense_list in transactions.items():
        print(expense_type)
        for expense in expense_list:
            print(f"  Amount: {expense['amount']}, Date: {expense['date']}")  # Print each transaction


# Function to update a transaction
def update_transaction():
    view_transactions()
    global transactions
    # Display the current transactions using a user-defined function
    expense_type = input("Enter expense type to update: ")
    if expense_type in transactions:
        index = int(
            input("Enter index of transaction to update: ")) - 1  # Python uses zero indexing & we use -1 for user input
        if 0 <= index < len(transactions[expense_type]):
            amount = float(input("Enter new amount: "))
            while True:
                date_str = input("Enter new date (YYYY-MM-DD): ")
                try:
                    date = datetime.strptime(date_str, "%Y-%m-%d").date()
                    break
                except ValueError:
                    print("Please Enter a Valid Date in YYYY-MM-DD format.!")
                    continue
            transactions[expense_type][index] = {"amount": amount, "date": date}
            print("Transaction updated successfully.")
        else:
            print("Invalid index.")
    else:
        print("Expense type not found.")


# Function to delete a transaction
def delete_transaction():
    # Display the current dictionary of the transaction
    view_transactions()  # Display current transactions

    # Check if the transaction dictionary is empty
    global transactions
    expense_type = input("Enter expense type to delete: ")
    if expense_type in transactions:
        index = int(
            input("Enter index of transaction to delete: ")) - 1  # Python uses zero indexing & we use -1 for user input
        if 0 <= index < len(transactions[expense_type]):
            del transactions[expense_type][index]
            print("Transaction deleted successfully.")
        else:
            print("Invalid index.")
    else:
        print("Expense type not found.")


# Function to calculate and display the summary
def display_summary():
    total = 0
    for expense_list in transactions.values():
        for expense in expense_list:
            total += expense["amount"]
    print(f"Total expenses: LKR.{total}")


# Main menu from Part B
def main_menu():
    global filename  # Declare filename as global
    load_transactions()  # Load transactions initially
    while True:
        # Main menu options
        print("\n|| Financial Tracker || ")
        print("-----------------------")

        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Update Transaction")
        print("4. Delete Transaction")
        print("5. Display Summary")
        print("6. Bulk Read Transactions from File")
        print("7. Save Transactions")
        print("8. Switch to GUI")
        print("9. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_transaction()
        elif choice == '2':
            view_transactions()
        elif choice == '3':
            update_transaction()
        elif choice == '4':
            delete_transaction()
        elif choice == '5':
            display_summary()
        elif choice == '6':
            filename = input("Enter filename to read transactions from: ")
            read_bulk_transactions_from_file(filename)
        elif choice == '7':
            save_transactions()
        elif choice == '8':
            start_gui()
        elif choice == '9':
            save_transactions()
            print("Exiting the program..!!")
            break
        else:
            print("Invalid choice. Please try again.")


# GUI part (Part C)
class FinanceTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Tracker")
        self.create_widgets()
        self.transactions = self.load_transactions(filename)
        self.display_transactions(self.transactions)

    def create_widgets(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Launch CLI Menu", command=self.launch_cli_menu)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # Frame for searching transactions
        search_frame = tk.LabelFrame(self.root, text="Search Transactions", )
        search_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Search entry
        ttk.Label(search_frame, text="Search:").grid(row=0, column=0, padx=5, pady=5)
        self.search_var = tk.StringVar()  # Variable to hold search query
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5)

        # Search criteria dropdown
        ttk.Label(search_frame, text="Search by:").grid(row=0, column=2, padx=5, pady=5)
        self.search_criteria = ttk.Combobox(search_frame,
                                             values=["Date",
                                                 "Amount"])  # Dropdown for search criteria
        self.search_criteria.current(0)  # Set default selection to first option
        self.search_criteria.grid(row=0, column=3, padx=5, pady=5)  # Placing dropdown in the search frame

        # Search button
        search_button = ttk.Button(search_frame, text="Search",
                                   command=self.search_transactions)  # Button to trigger search
        search_button.grid(row=0, column=4, padx=5, pady=5)

        # Frame for displaying transactions
        display_frame = ttk.LabelFrame(self.root, text="Transactions")
        display_frame.pack(padx=10, pady=10, fill=tk.BOTH,
                           expand=True)  # Packing the display_frame with some padding, filling both horizontally and vertically, and expanding it

        # Treeview for displaying transactions
        self.tree = ttk.Treeview(display_frame, columns=("Date", "Description", "Amount"), show='headings')
        # Setting headings for other columns and linking them to sorting functions
        self.tree.heading("Date", text="Date", command=lambda: self.sort_column("Date", False))
        self.tree.heading("Description", text="Description", command=lambda: self.sort_column("Description", False))
        self.tree.heading("Amount", text="Amount", command=lambda: self.sort_column("Amount", False))
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH,
                       expand=True)  # Packing the Treeview to the left, filling both horizontally and vertically

        # Scrollbar for the Treeview
        scrollbar = ttk.Scrollbar(display_frame, orient="vertical",
                                  command=self.tree.yview)  # Creating a vertical scrollbar
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  # Packing the scrollbar to the right, filling vertically
        self.tree.configure(
            yscrollcommand=scrollbar.set)  # Configuring the Treeview to use the scrollbar for vertical scrolling

        #  Variable to keep track of sorting order for different columns
        self.sort_order = {"Date": False, "Description": False, "Amount": False}

    def load_transactions(self, filename):
        try:
            with open(filename, "r") as file:
                transactions = json.load(file)
            return transactions
        except FileNotFoundError:
            return {}

    def display_transactions(self, transactions):
        # Remove existing entries
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Add transactions to the treeview
        for category, entries in transactions.items():
            for i, entry in enumerate(entries, 1):
                self.tree.insert("", "end", text=f"{category}-{i}", values=(
                    entry["date"],
                    entry.get("description", category),  # Fetch description if available, else empty string
                    entry["amount"]))

    def search_transactions(self):
        query = self.search_var.get().lower()
        criteria = self.search_criteria.get()
        results = {}
        for category, transaction_list in self.transactions.items():
            for i, transaction in enumerate(transaction_list, 1):
                # Convert all fields to lowercase for case-insensitive search
                date_str = str(transaction["date"]).lower()
                description = transaction.get("description", "").lower()
                amount_str = str(transaction["amount"]).lower()

                if criteria == "Date" and query in date_str:
                    results.setdefault(category, []).append(transaction)
                elif criteria == "Description" and query in description:
                    results.setdefault(category, []).append(transaction)
                elif criteria == "Amount" and query in amount_str:
                    results.setdefault(category, []).append(transaction)
        self.display_transactions(results)

    def sort_column(self, column, reverse):
        data = [(self.tree.set(child, column), child) for child in self.tree.get_children('')]
        data.sort(reverse=reverse)
        for index, (val, child) in enumerate(data):
            self.tree.move(child, '', index)
        # Toggle the sort order
        self.sort_order[column] = not self.sort_order[column]

    def save_transactions(self):
        with open(filename, "w") as file:
            json.dump(self.transactions, file, indent=4, default=str)
        print("Transactions saved successfully!")

    def launch_cli_menu(self):
        self.save_transactions()
        self.root.destroy()  # Close the GUI window
        main_menu()  # Switch back to the CLI


def start_gui():
    root = tk.Tk()
    app = FinanceTrackerGUI(root)
    root.mainloop()


def main():
    main_menu()


if __name__ == "__main__":
    main()
