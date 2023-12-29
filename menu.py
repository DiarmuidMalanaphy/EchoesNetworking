import socket
import tkinter as tk
import subprocess
from tkinter import messagebox
from tkinter import simpledialog
import sys

import socket
import tkinter as tk
import subprocess
from tkinter import messagebox
from tkinter import simpledialog
import sys

from Networking import networking

def create_main_menu(root):
    root.title("Mine Goblin - Game Mode Selection")
    root.geometry('500x300')
    root.configure(bg='#2B2B2B')  # Dark background color

    label = tk.Label(root, text="Select Game Mode", font=("Arial", 18, 'bold'), fg='white', bg='#2B2B2B')
    label.pack(pady=20)

    internet_button = tk.Button(root, text="Internet Multiplayer", command=lambda: on_internet_multiplayer(root), bg='#4CAF50', fg='white', font=("Arial", 14), pady=10)
    internet_button.pack(fill='x', padx=50, pady=5)

    local_button = tk.Button(root, text="Local Multiplayer", command=lambda: on_local_multiplayer(root), bg='#2196F3', fg='white', font=("Arial", 14), pady=10)
    local_button.pack(fill='x', padx=50, pady=20)

    root.mainloop()

def on_internet_multiplayer(root):
    root.geometry('500x350')
    update_window_for_setup(root, "Select Setup Type")
    for widget in root.winfo_children():
        widget.destroy()

    # Setup the internet multiplayer setup interface
    label = tk.Label(root, text="Select Setup Type", font=("Arial", 18, 'bold'), fg='white', bg='#2B2B2B')
    label.pack(pady=20)

    basic_button = tk.Button(root, text="Basic Setup", command=lambda: on_basic_setup(root), bg='#4CAF50', fg='white', font=("Arial", 14), pady=10)
    basic_button.pack(fill='x', padx=50, pady=5)

    advanced_button = tk.Button(root, text="Advanced Setup", command=lambda: on_advanced_setup(root), bg='#2196F3', fg='white', font=("Arial", 14), pady=10)
    advanced_button.pack(fill='x', padx=50, pady=20)

    return_button = tk.Button(root, text="Return to Main Menu", command=lambda: return_to_main_menu(root), bg='#FF5722', fg='white', font=("Arial", 14), pady=10)
    return_button.pack(fill='x', padx=50, pady=5)

def on_basic_setup(root):
    domain_name = simpledialog.askstring("Input", "Enter a domain name:", parent=root)
    if domain_name:
        try:
            ip_address = socket.gethostbyname(domain_name)
            confirm_and_use_ip(ip_address)
        except socket.gaierror:
            messagebox.showerror("Error", "Failed to get IP Address")









def on_advanced_setup(root):
    # Clear the existing window
    for widget in root.winfo_children():
        widget.destroy()

    # Setup the advanced setup interface
    root.configure(bg='#2B2B2B')  # Consistent dark background color
    label = tk.Label(root, text="Advanced Setup", font=("Arial", 18, 'bold'), fg='white', bg='#2B2B2B')
    label.pack(pady=20)

    # Entry for IP Address
    ip_label = tk.Label(root, text="Enter IP Address:", font=("Arial", 12), fg='white', bg='#2B2B2B')
    ip_label.pack(pady=5)

    ip_entry = tk.Entry(root, font=("Arial", 12), width=30)
    ip_entry.pack(pady=5)

    # Confirm Button
    confirm_button = tk.Button(root, text="Confirm IP", command=lambda: confirm_and_use_ip(ip_entry.get()), bg='#4CAF50', fg='white', font=("Arial", 14), pady=10)
    confirm_button.pack(fill='x', padx=50, pady=5)

    # Return to Main Menu Button
    return_button = tk.Button(root, text="Return to Main Menu", command=lambda: return_to_main_menu(root), bg='#FF5722', fg='white', font=("Arial", 14), pady=10)
    return_button.pack(fill='x', padx=50, pady=20)

def confirm_and_use_ip(ip_address):
    if ip_address is not None:
        networkTool = networking.Networking(ip_address)

        if networkTool.send_validate_server_request():
            root.destroy()
            script_path = 'minegoblinggame.py'
            process = subprocess.Popen([sys.executable, script_path,ip_address], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate() 
        else:
            messagebox.showerror("Error", "Failed to validate server. Please check the IP address.", parent=root)
    else:
        messagebox.showerror("Error", "No IP address entered.", parent=root)

def on_local_multiplayer(root):
    print("Local Multiplayer selected.")
    root.destroy()  # Close the Tkinter window
    # Run minegoblin_game.py with '127.0.0.1' as the argument
    script_path = 'minegoblinggame.py'  # Update this path
    



    # try:
    # subprocess.Popen([sys.executable, script_path, '127.0.0.1'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process = subprocess.Popen([sys.executable, script_path, '127.0.0.1'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate() 
    # If i get rid of the process.communicate it stops working

    
    #subprocess.Popen(['python', script_path, '127.0.0.1'])

def return_to_main_menu(root):
    # Clear the existing window
    for widget in root.winfo_children():
        widget.destroy()

    # Recreate the initial main menu interface
    create_main_menu(root)

def update_window_for_setup(root, title):
    # Clear the existing window and setup new interface
    for widget in root.winfo_children():
        widget.destroy()

    label = tk.Label(root, text=title, font=("Arial", 18, 'bold'), fg='white', bg='#2B2B2B')
    label.pack(pady=20)

    # Add more widgets as per the setup type (Basic or Advanced)

    return_button = tk.Button(root, text="Return to Main Menu", command=lambda: return_to_main_menu(root), bg='#FF5722', fg='white', font=("Arial", 14), pady=10)
    return_button.pack(fill='x', padx=50, pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    create_main_menu(root)