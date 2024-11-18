import tkinter as tk
from tkinter import messagebox, ttk
import subprocess
import config
import random

def nav_create_button(text, command, row, column):
    button = tk.Button(frame_nav,
                       text=text,
                       command=command,
                       width=20,
                       font=("Segoe UI", 10),
                       bg=config.color_nav_bg,
                       fg="white",
                       relief="flat",
                       activebackground=config.color_nav_click_bg,
                       activeforeground=config.color_nav_click_text,
                       bd=0)

    button.grid(row=row, column=column, padx=10, pady=4)

    button.bind("<Enter>", lambda event, btn=button: btn.config(bg=config.color_nav_hover))
    button.bind("<Leave>", lambda event, btn=button: btn.config(bg=config.color_nav_bg))

    return button

def main_create_button(text, command, row, column):
    button = tk.Button(frame_main,
                       text=text,
                       command=command,
                       font=("Segoe UI", 12),
                       height=2,
                       width=20,
                       bg=config.color_main_button_bg,
                       fg=config.color_main_button_text,
                       relief="flat",
                       activebackground=config.color_main_button_click_bg,
                       activeforeground=config.color_main_button_click_text,
                       bd=0)

    button.grid(row=row, column=column, padx=10, pady=10, sticky="ew")

    button.bind("<Enter>", lambda event, btn=button: btn.config(bg=config.color_main_button_hover))
    button.bind("<Leave>", lambda event, btn=button: btn.config(bg=config.color_main_button_bg))

    return button

def main_clear():
    for widget in frame_main.winfo_children():
        widget.destroy()

def main_title(text):
    label = tk.Label(frame_main,
                     text=text,
                     font=("Segoe UI", 14),
                     fg=config.color_label_text,
                     bg=config.color_label_bg,
                     padx=10, pady=10)
    label.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

def users_menu():
    main_clear()

    main_title("Manage Users")

    frame_main.grid_columnconfigure(0, weight=1)
    frame_main.grid_columnconfigure(1, weight=1)
    frame_main.grid_columnconfigure(2, weight=1)

    main_create_button(text="Add User", command=users_add_user, row=1, column=1)
    main_create_button(text="Edit User", command=lambda: test("Edit User"), row=2, column=1)
    main_create_button(text="Delete User", command=users_delete_user, row=3, column=1)

def users_add_user():
    names = ["Ithallo", "Cesar", "Nelson", "Pele", "Zeca Pagodinho", "Tim Maia", "Raul Seixas", "Cazuza", "Chacrinha", "Chico Buarque"]

    def create_user():
        username = entry_username.get().strip()
        if not username:
            messagebox.showerror("Error", "Username cannot be empty!")
            return

        try:
            result = subprocess.run(
                ["sudo", "useradd", username],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                messagebox.showinfo("Success", f"User '{username}' created successfully!")
                entry_username.delete(0, tk.END)  # Limpa a caixa de input após sucesso
            else:
                messagebox.showerror("Error", f"Failed to create user:\n{result.stderr}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred:\n{e}")

    def generate_random_username():
        # Gerar um nome real aleatório em português (somente primeiro nome)
        random_username = random.choice(names).lower()
        entry_username.delete(0, tk.END)
        entry_username.insert(0, random_username)

    main_clear()
    main_title("Manage Users")

    label = tk.Label(frame_main,
                     text="Enter new username:",
                     font=("Segoe UI", 12),
                     fg=config.color_label_text,
                     bg=config.color_label_bg)
    label.grid(row=1, column=1, padx=10, pady=10)

    entry_username = tk.Entry(frame_main, font=("Segoe UI", 12), width=20)
    entry_username.grid(row=2, column=1, padx=10, pady=10)

    main_create_button(text="Random Username", command=generate_random_username, row=3, column=1)
    main_create_button(text="Create User", command=create_user, row=4, column=1)
    main_create_button(text="Back", command=users_menu, row=5, column=1)

def users_delete_user():
    def get_system_users():
        try:
            result = subprocess.run(
                ["getent", "passwd"],
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                messagebox.showerror("Error", "Failed to retrieve system users.")
                return []

            users = [
                line.split(":")[0]
                for line in result.stdout.splitlines()
                if int(line.split(":")[2]) >= 1000 and line.split(":")[0] != "nobody"
            ]
            return users
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while fetching users: {e}")
            return []

    def delete_user():
        username = combobox_users.get()
        if not username:
            messagebox.showerror("Error", "You must select a user to delete!")
            return

        try:
            result_check = subprocess.run(
                ["id", username],
                capture_output=True,
                text=True
            )

            if result_check.returncode != 0:
                messagebox.showerror("Error", f"User '{username}' does not exist!")
                return

            result_delete = subprocess.run(
                ["sudo", "userdel", username],
                capture_output=True,
                text=True
            )

            if result_delete.returncode == 0:
                messagebox.showinfo("Success", f"User '{username}' deleted successfully!")
                update_user_list()
            else:
                messagebox.showerror("Error", f"Failed to delete user:\n{result_delete.stderr}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred:\n{e}")

    def update_user_list():
        users = get_system_users()
        if users:
            combobox_users['values'] = users
            combobox_users.set('')

    main_clear()
    main_title("Delete User")

    users = get_system_users()
    if not users:
        return

    label = tk.Label(frame_main,
                     text="Select or Type a user to delete:",
                     font=("Segoe UI", 12),
                     fg=config.color_label_text,
                     bg=config.color_label_bg)
    label.grid(row=1, column=1, padx=10, pady=10)

    combobox_users = ttk.Combobox(frame_main, font=("Segoe UI", 12), width=20, values=users)
    combobox_users.grid(row=2, column=1, padx=10, pady=10)
    combobox_users.set('')

    main_create_button(text="Delete User", command=delete_user, row=3, column=1)
    main_create_button(text="Back", command=users_menu, row=4, column=1)

def test(btn):
    print(f"{btn}")

""" ROOT """
root = tk.Tk()
root.configure(bg=config.color_root)
root.title("Painel Administrativo")

""" FRAMES """
frame_nav = tk.Frame(root, bg=config.color_nav_bg)
frame_nav.grid(row=0, column=0, sticky="ew")

frame_main = tk.Frame(root, height=500, bg=config.color_main)
frame_main.grid(row=1, column=0, sticky="ew")
frame_main.grid_propagate(False)

""" NAV """
nav_create_button(text="Users", command=users_menu, row=0, column=0)
nav_create_button(text="System", command=lambda: test("System"), row=0, column=1)
nav_create_button(text="Services", command=lambda: test("Services"), row=0, column=2)
nav_create_button(text="Files", command=lambda: test("Files"), row=0, column=3)
nav_create_button(text="Automations", command=lambda: test("Automations"), row=0, column=4)

""" MAIN """
root.mainloop()
