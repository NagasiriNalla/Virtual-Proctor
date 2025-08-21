import tkinter as tk
from tkinter import messagebox
import subprocess

# Dictionary of valid users
valid_users = {
    "StudentA": "1234",
    "StudentB": "exam2025"
}

# Function to validate login and launch monitoring
def login():
    name = username_entry.get()
    password = password_entry.get()

    if name in valid_users and valid_users[name] == password:
        messagebox.showinfo("Login Successful", f"Welcome, {name}!")
        root.destroy()
        subprocess.Popen(["python", "facemonitor.py"])  # Launch your proctoring system
    else:
        messagebox.showerror("Login Failed", "Invalid name or password")

# Create the window
root = tk.Tk()
root.title("Virtual Proctoring Login")
root.geometry("350x200")
root.configure(bg="#f0f0f0")

# Widgets
tk.Label(root, text="Student Name:", font=("Arial", 12), bg="#f0f0f0").pack(pady=(20, 5))
username_entry = tk.Entry(root, font=("Arial", 12))
username_entry.pack()

tk.Label(root, text="Password:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
password_entry = tk.Entry(root, show="*", font=("Arial", 12))
password_entry.pack()

login_btn = tk.Button(root, text="Login", command=login, font=("Arial", 12), bg="#4CAF50", fg="white")
login_btn.pack(pady=15)

root.mainloop()