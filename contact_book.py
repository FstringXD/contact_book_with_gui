import tkinter as tk
from tkinter import messagebox
import sqlite3

# --- DB Setup ---
conn = sqlite3.connect("contacts.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT NOT NULL
    )
""")
conn.commit()

# --- Functions ---
def refresh_contacts():
    listbox.delete(0, tk.END)
    for row in cursor.execute("SELECT id, name, phone FROM contacts"):
        listbox.insert(tk.END, f"{row[0]}. {row[1]} - {row[2]}")

def add_contact():
    name = entry_name.get().strip()
    phone = entry_phone.get().strip()
    if name and phone:
        cursor.execute("INSERT INTO contacts (name, phone) VALUES (?, ?)", (name, phone))
        conn.commit()
        refresh_contacts()
        entry_name.delete(0, tk.END)
        entry_phone.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "Name and phone cannot be empty.")

def delete_contact():
    selected = listbox.curselection()
    if selected:
        item = listbox.get(selected[0])
        contact_id = item.split(".")[0]
        cursor.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
        conn.commit()
        refresh_contacts()
    else:
        messagebox.showwarning("Selection Error", "Please select a contact to delete.")

# --- GUI Setup ---
root = tk.Tk()
root.title("📇 Contact Book")

# Form
frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Name:").grid(row=0, column=0)
entry_name = tk.Entry(frame, width=25)
entry_name.grid(row=0, column=1)

tk.Label(frame, text="Phone:").grid(row=1, column=0)
entry_phone = tk.Entry(frame, width=25)
entry_phone.grid(row=1, column=1)

# Buttons
btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)

add_btn = tk.Button(btn_frame, text="➕ Add Contact", command=add_contact)
add_btn.pack(side=tk.LEFT, padx=5)

del_btn = tk.Button(btn_frame, text="🗑️ Delete Contact", command=delete_contact)
del_btn.pack(side=tk.LEFT, padx=5)

# Listbox
listbox = tk.Listbox(root, width=40)
listbox.pack(pady=10)

refresh_contacts()

root.mainloop()

# --- Close DB on Exit ---
conn.close()
