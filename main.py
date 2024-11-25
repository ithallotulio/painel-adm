import psutil
import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import subprocess
import config
import random
import os

current_path = os.getcwd()

def check_sudo_permission():
    """Verifica se o usuário tem permissão para usar sudo sem pedir a senha."""
    try:
        result = subprocess.run(
            ["sudo", "-n", "true"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("Sudo permission granted!")
            return True
        else:
            print("No sudo permission or password required.")
            return False
    except FileNotFoundError:
        messagebox.showerror("Error", "sudo command not found. Are you on a Linux/Unix system?")
        return False
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred while checking sudo permission: {e}")
        return False

def request_sudo_password(callback):
    """Solicita a senha do sudo via interface gráfica tkinter e chama a função de callback após autenticação bem-sucedida."""
    def authenticate_sudo_password():
        """Autentica a senha fornecida para o sudo e chama a função de callback após sucesso."""
        password = password_entry.get()
        if not password:
            messagebox.showerror("Error", "Password cannot be empty!")
            return

        try:
            result = subprocess.run(
                ["sudo", "-S", "echo", "Sudo authentication successful"],
                input=password + "\n",
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                messagebox.showinfo("Success", "Sudo authentication successful!")
                auth_window.destroy()
                callback()  # Chama a função original após autenticação bem-sucedida
            else:
                messagebox.showerror("Error", "Incorrect sudo password!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    auth_window = tk.Toplevel(root)
    auth_window.title("Sudo Authentication")

    label = tk.Label(auth_window, text="Enter your sudo password:")
    label.pack(padx=20, pady=10)

    password_entry = tk.Entry(auth_window, show="*", font=("Segoe UI", 12))
    password_entry.pack(padx=20, pady=10)

    auth_button = tk.Button(auth_window, text="Authenticate", command=authenticate_sudo_password)
    auth_button.pack(pady=10)

    auth_window.mainloop()

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
    
    main_title("Welcome to Linux Controller!")

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

    main_create_button(text="Add User", command=users_add_user, row=1, column=1)
    main_create_button(text="Edit User", command=users_edit_user, row=2, column=1)
    main_create_button(text="Delete User", command=users_delete_user, row=3, column=1)
    main_create_button(text="Close", command=main_clear, row=4, column=1)

def users_add_user():
    names = ["Ithallo", "Cesar", "Nelson", "Pele", "ZecaPagodinho", "TimMaia", "RaulSeixas", "Cazuza", "Chacrinha", "ChicoBuarque"]

    def create_user():
        """Função para criar um usuário, que será chamada após a autenticação sudo."""
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
        """Função para gerar um nome de usuário aleatório."""
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
    
    # Quando o botão "Create User" for clicado, verifica permissão sudo e solicita a senha se necessário
    main_create_button(text="Create User", command=lambda: check_and_create_user(create_user), row=4, column=1)
    
    main_create_button(text="Back", command=users_menu, row=5, column=1)

def check_and_create_user(create_user_callback):
    """Verifica se o usuário tem permissão sudo e chama a função de criação de usuário após a autenticação"""
    if not check_sudo_permission():
        # Se o usuário não tem permissão sudo, solicita a senha
        request_sudo_password(create_user_callback)
    else:
        # Se já tem permissão sudo, chama a função de criação de usuário diretamente
        create_user_callback()

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

def users_edit_user():
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

    def update_user_list():
        users = get_system_users()
        if users:
            combobox_users['values'] = users
            combobox_users.set('')

    def edit_user():
        username = combobox_users.get()
        new_username = entry_new_username.get().strip()
        
        if not username:
            messagebox.showerror("Error", "You must select a user to edit!")
            return
        if not new_username:
            messagebox.showerror("Error", "New username cannot be empty!")
            return
        
        try:
            # Verificar se o usuário existe
            result_check = subprocess.run(
                ["id", username],
                capture_output=True,
                text=True
            )

            if result_check.returncode != 0:
                messagebox.showerror("Error", f"User '{username}' does not exist!")
                return

            # Renomear o usuário
            result_rename_user = subprocess.run(
                ["sudo", "usermod", "-l", new_username, username],
                capture_output=True,
                text=True
            )

            # Renomear o grupo do usuário
            result_rename_group = subprocess.run(
                ["sudo", "groupmod", "-n", new_username, username],
                capture_output=True,
                text=True
            )

            # Alterar o grupo primário do usuário
            result_change_group = subprocess.run(
                ["sudo", "usermod", "-g", new_username, new_username],
                capture_output=True,
                text=True
            )

            if result_rename_user.returncode == 0 and result_rename_group.returncode == 0 and result_change_group.returncode == 0:
                messagebox.showinfo("Success", f"User '{username}' renamed to '{new_username}' successfully!")
                update_user_list()  # Atualiza a lista de usuários após a alteração
                
                # Limpar o campo de novo nome de usuário após o sucesso
                entry_new_username.delete(0, tk.END)

            else:
                messagebox.showerror("Error", f"Failed to rename user or group:\n"
                                            f"{result_rename_user.stderr}\n"
                                            f"{result_rename_group.stderr}\n"
                                            f"{result_change_group.stderr}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred:\n{e}")



    main_clear()
    main_title("Edit User")

    users = get_system_users()
    if not users:
        return

    label_select = tk.Label(frame_main,
                            text="Select or Type a user to edit:",
                            font=("Segoe UI", 12),
                            fg=config.color_label_text,
                            bg=config.color_label_bg)
    label_select.grid(row=1, column=1, padx=10, pady=10)

    combobox_users = ttk.Combobox(frame_main, font=("Segoe UI", 12), width=20, values=users)
    combobox_users.grid(row=2, column=1, padx=10, pady=10)
    combobox_users.set('')

    label_new_username = tk.Label(frame_main,
                                  text="Enter new user:",
                                  font=("Segoe UI", 12),
                                  fg=config.color_label_text,
                                  bg=config.color_label_bg)
    label_new_username.grid(row=3, column=1, padx=10, pady=10)

    entry_new_username = tk.Entry(frame_main, font=("Segoe UI", 12), width=20)
    entry_new_username.grid(row=4, column=1, padx=10, pady=10)

    main_create_button(text="Rename User", command=edit_user, row=5, column=1)
    main_create_button(text="Back", command=users_menu, row=6, column=1)

def system():
    """Monitora o uso de CPU, memória e disco e exibe na interface."""

    def get_system_info():
        """Retorna informações do sistema como CPU, memória e disco."""
        return {
            "CPU Usage": f"{psutil.cpu_percent()}%",
            "Memory Usage": f"{psutil.virtual_memory().percent}%",
            "Disk Usage": f"{psutil.disk_usage('/').percent}%"
        }

    def update_system_info():
        """Atualiza os rótulos com informações do sistema."""
        if not frame_main.winfo_exists():  # Verifica se o frame ainda existe
            return  # Encerra a função se o frame foi destruído

        # Coleta informações do sistema
        system_info = get_system_info()

        # Atualiza os rótulos
        for key, label in labels.items():
            if label.winfo_exists():  # Verifica se o rótulo ainda existe
                label.config(text=f"{key}: {system_info[key]}")

        # Agenda a próxima atualização
        root.after(1000, update_system_info)


    # Limpa a interface principal
    main_clear()
    main_title("System Monitoring")

    # Cria rótulos dinamicamente
    labels = {}
    row = 1
    for key in ["CPU Usage", "Memory Usage", "Disk Usage"]:
        label = tk.Label(
            frame_main,
            text=f"{key}: 0%",
            font=("Segoe UI", 12),
            fg=config.color_label_text,
            bg=config.color_label_bg
        )
        label.grid(row=row, column=1, padx=10, pady=10, sticky="ew")
        labels[key] = label
        row += 1

    # Botão para fechar
    main_create_button(text="Close", command=main_clear, row=row, column=1)

    # Inicia a atualização
    update_system_info()

def services():
    """Monitora e gerencia os serviços do sistema."""

    def get_system_services():
        """Obtém a lista de serviços disponíveis utilizando systemctl."""
        try:
            result = subprocess.run(
                ["systemctl", "list-units", "--type=service", "--state=running"],
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                messagebox.showerror("Error", "Failed to retrieve services.")
                return []

            # Filtra os nomes dos serviços, removendo qualquer linha de cabeçalho ou vazia,
            # e seleciona apenas os serviços que terminam com '.service'
            services = [
                line.split()[0] for line in result.stdout.splitlines()[1:]
                if line.strip() and line.split()[0].endswith('.service')  # Filtra serviços .service
            ]

            # Remove a extensão '.service' de cada nome de serviço
            services = [service.replace('.service', '') for service in services]

            # Verifica se a lista de serviços está vazia
            if not services:
                messagebox.showwarning("No Services", "No running services found.")
            return services
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while fetching services: {e}")
            return []

    def update_service_list():
        """Atualiza a lista de serviços disponíveis."""
        services = get_system_services()
        if services:
            combobox_services['values'] = services
            combobox_services.set('')  # Limpa o combobox após atualização

    def start_service():
        """Inicia o serviço selecionado."""
        service = combobox_services.get()
        if not service:
            messagebox.showerror("Error", "You must select a service to start!")
            return

        try:
            result = subprocess.run(
                ["sudo", "systemctl", "start", service],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                messagebox.showinfo("Success", f"Service '{service}' started successfully!")
                update_service_list()  # Atualiza a lista de serviços após a execução
            else:
                messagebox.showerror("Error", f"Failed to start service '{service}':\n{result.stderr}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def stop_service():
        """Para o serviço selecionado."""
        service = combobox_services.get()
        if not service:
            messagebox.showerror("Error", "You must select a service to stop!")
            return

        try:
            result = subprocess.run(
                ["sudo", "systemctl", "stop", service],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                messagebox.showinfo("Success", f"Service '{service}' stopped successfully!")
                update_service_list()
            else:
                messagebox.showerror("Error", f"Failed to stop service '{service}':\n{result.stderr}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def restart_service():
        """Reinicia o serviço selecionado."""
        service = combobox_services.get()
        if not service:
            messagebox.showerror("Error", "You must select a service to restart!")
            return

        try:
            result = subprocess.run(
                ["sudo", "systemctl", "restart", service],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                messagebox.showinfo("Success", f"Service '{service}' restarted successfully!")
                update_service_list()
            else:
                messagebox.showerror("Error", f"Failed to restart service '{service}':\n{result.stderr}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    # Limpa a interface principal
    main_clear()
    main_title("System Services")

    # Obtém a lista de serviços disponíveis
    services = get_system_services()
    if not services:
        return

    # Rótulo para selecionar o serviço
    label_select_service = tk.Label(frame_main,
                                    text="Select a service to manage:",
                                    font=("Segoe UI", 12),
                                    fg=config.color_label_text,
                                    bg=config.color_label_bg)
    label_select_service.grid(row=1, column=1, padx=10, pady=10)

    # Combobox para selecionar o serviço
    combobox_services = ttk.Combobox(frame_main, font=("Segoe UI", 12), width=20, values=services)
    combobox_services.grid(row=2, column=1, padx=10, pady=10)
    combobox_services.set('')

    # Botões para gerenciar os serviços
    main_create_button(text="Start Service", command=start_service, row=3, column=1)
    main_create_button(text="Stop Service", command=stop_service, row=4, column=1)
    main_create_button(text="Restart Service", command=restart_service, row=5, column=1)

    # Botão para voltar ao menu anterior
    main_create_button(text="Close", command=main_clear, row=6, column=1)

def create_label(text, row, column):
    label = tk.Label(
        frame_main,
        text=text,
        font=("Segoe UI", 12),
        fg=config.color_label_text,
        bg=config.color_label_bg,
    )
    label.grid(row=row, column=column, padx=10, pady=10)
    return label

def update_combobox_items(path, combobox):
    try:
        items = os.listdir(path)
        combobox["values"] = items
    except Exception as e:
        combobox["values"] = []
        messagebox.showerror("Error", f"Failed to list items: {e}")

def create_combobox(path):
    combobox = ttk.Combobox(frame_main, font=("Segoe UI", 12), width=39, state="readonly")
    combobox.grid(row=3, column=1, padx=10, pady=10)
    combobox.set(path)
    update_combobox_items(path, combobox)
    return combobox

def files_menu():
    global current_path
    main_clear()

    main_title("File Management")

    # Label para instrução
    tk.Label(frame_main, text="Current Path:", font=("Segoe UI", 12), fg=config.color_label_text, bg=config.color_label_bg).grid(row=1, column=1, padx=10, pady=10)

    # Combobox única
    combobox_items = ttk.Combobox(frame_main, font=("Segoe UI", 12), width=39, state="readonly")
    combobox_items.grid(row=2, column=1, padx=10, pady=10)
    combobox_items.set(current_path)

    def update_combobox_items(path):
        try:
            combobox_items["values"] = os.listdir(path)
        except Exception as e:
            combobox_items["values"] = []
            messagebox.showerror("Error", f"Failed to list items: {e}")

    update_combobox_items(current_path)

    # Botões
    main_create_button(text="Edit Path", command=lambda: files_edit_path(current_path), row=3, column=1)
    main_create_button(text="Create File", command=lambda: files_create(current_path), row=4, column=1)
    main_create_button(text="Delete File", command=lambda: files_delete(current_path), row=5, column=1)
    main_create_button(text="Move File", command=lambda: files_move(current_path), row=6, column=1)
    main_create_button(text="Close", command=main_clear, row=7, column=1)

def files_edit_path(previous_path):
    global current_path
    main_clear()

    main_title("File Management")

    # Label para o caminho
    tk.Label(frame_main, text="Current Path:", font=("Segoe UI", 12), fg=config.color_label_text, bg=config.color_label_bg).grid(row=1, column=1, padx=10, pady=10)

    # Caixa de entrada para edição do caminho
    entry_path = tk.Entry(frame_main, font=("Segoe UI", 12), width=40)
    entry_path.insert(0, previous_path)
    entry_path.grid(row=2, column=1, padx=10, pady=10)

    # Título para a Combobox
    tk.Label(frame_main, text="Click to visualize files:", font=("Segoe UI", 12), fg=config.color_label_text, bg=config.color_label_bg).grid(row=3, column=1, padx=10, pady=10)

    # Combobox para listar itens no caminho
    combobox_items = ttk.Combobox(frame_main, font=("Segoe UI", 12), width=39, state="readonly")
    combobox_items.grid(row=4, column=1, padx=10, pady=10)
    combobox_items.set("Visualize files")

    def update_combobox_items(path):
        try:
            combobox_items["values"] = os.listdir(path)
            combobox_items.set("Visualize files")
        except Exception as e:
            combobox_items["values"] = []
            messagebox.showerror("Error", f"Failed to list items: {e}")

    update_combobox_items(previous_path)

    def confirm_path(path):
        global current_path
        try:
            if not os.path.isdir(path):
                raise ValueError("The specified path is not a directory.")
            current_path = path
            messagebox.showinfo("Success", f"Path updated to: {current_path}")
            update_combobox_items(current_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update path: {e}")

    main_create_button(text="Confirm Path", command=lambda: confirm_path(entry_path.get()), row=5, column=1)
    main_create_button(text="Back", command=files_menu, row=6, column=1)

def files_create(previous_path):
    main_clear()

    main_title("File Management")

    # Label para o caminho
    tk.Label(frame_main, text="Current Path:", font=("Segoe UI", 12), fg=config.color_label_text, bg=config.color_label_bg).grid(row=1, column=1, padx=10, pady=10)

    # Combobox única
    combobox_items = ttk.Combobox(frame_main, font=("Segoe UI", 12), width=39, state="readonly")
    combobox_items.grid(row=2, column=1, padx=10, pady=10)
    combobox_items.set(previous_path)

    def update_combobox_items(path):
        try:
            combobox_items["values"] = os.listdir(path)
        except Exception as e:
            combobox_items["values"] = []
            messagebox.showerror("Error", f"Failed to list items: {e}")

    update_combobox_items(previous_path)

    tk.Label(frame_main, text="Enter file name:", font=("Segoe UI", 12), fg=config.color_label_text, bg=config.color_label_bg).grid(row=4, column=1, padx=10, pady=10)

    # Radiobuttons
    creation_type = tk.StringVar(value="File")
    frame_radiobuttons = tk.Frame(frame_main, bg=config.color_label_bg)
    frame_radiobuttons.grid(row=6, column=1, padx=10, pady=10)

    tk.Radiobutton(frame_radiobuttons, text="File", variable=creation_type, value="File", font=("Segoe UI", 12), bg='#868686', width=17, height=2).pack(side=tk.LEFT, padx=5)
    tk.Radiobutton(frame_radiobuttons, text="Directory", variable=creation_type, value="Directory", font=("Segoe UI", 12), bg='#868686', width=17, height=2).pack(side=tk.LEFT, padx=5)

    entry_name = tk.Entry(frame_main, font=("Segoe UI", 12), width=40)
    entry_name.grid(row=5, column=1, padx=10, pady=10)

    def create_item():
        item_name = entry_name.get()
        if not item_name:
            messagebox.showerror("Error", "Please enter a name.")
            return

        full_path = os.path.join(previous_path, item_name)
        try:
            if creation_type.get() == "File":
                open(full_path, "w").close()
                messagebox.showinfo("Success", f"File '{item_name}' created successfully!")
            else:
                os.makedirs(full_path, exist_ok=True)
                messagebox.showinfo("Success", f"Directory '{item_name}' created successfully!")
            update_combobox_items(previous_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create item: {e}")

    main_create_button(text="Create", command=create_item, row=7, column=1)
    main_create_button(text="Back", command=files_menu, row=8, column=1)

def files_delete(previous_path):
    main_clear()

    main_title("File Management")

    tk.Label(frame_main, text="Select file or directory to delete", font=("Segoe UI", 12), fg=config.color_label_text, bg=config.color_label_bg).grid(row=1, column=1, padx=10, pady=10)

    combobox_items = ttk.Combobox(frame_main, font=("Segoe UI", 12), width=39, state="readonly")
    combobox_items.grid(row=2, column=1, padx=10, pady=10)

    def update_combobox_items(path):
        try:
            result = subprocess.run(["ls", path], capture_output=True, text=True)
            if result.returncode != 0:
                raise Exception(result.stderr)
            combobox_items["values"] = result.stdout.splitlines()
        except Exception as e:
            combobox_items["values"] = []
            messagebox.showerror("Error", f"Failed to list items: {e}")

    update_combobox_items(previous_path)

    def delete_item():
        item_name = combobox_items.get()
        full_path = f"{previous_path}/{item_name}"
        try:
            subprocess.run(["rm", "-r", full_path], check=True)
            messagebox.showinfo("Success", f"Item '{item_name}' deleted successfully!")
            update_combobox_items(previous_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete item: {e}")

    main_create_button(text="Delete", command=delete_item, row=3, column=1)
    main_create_button(text="Back", command=files_menu, row=4, column=1)

def files_move(previous_path):
    main_clear()

    main_title("File Management")

    tk.Label(frame_main, text="Current Path (from):", font=("Segoe UI", 12), fg=config.color_label_text, bg=config.color_label_bg).grid(row=1, column=1, padx=10, pady=10)

    combobox_items = ttk.Combobox(frame_main, font=("Segoe UI", 12), width=39, state="readonly")
    combobox_items.grid(row=3, column=1, padx=10, pady=10)
    combobox_items.set("Select file or directory to move")

    def update_combobox_items(path):
        try:
            combobox_items["values"] = os.listdir(path)
        except Exception as e:
            combobox_items["values"] = []
            messagebox.showerror("Error", f"Failed to list items: {e}")

    update_combobox_items(previous_path)

    tk.Label(frame_main, text="Target Path:", font=("Segoe UI", 12), fg=config.color_label_text, bg=config.color_label_bg).grid(row=4, column=1, padx=10, pady=10)

    entry_target = tk.Entry(frame_main, font=("Segoe UI", 12), width=40)
    entry_target.grid(row=5, column=1, padx=10, pady=10)

    def move_item():
        item_name = combobox_items.get()
        target_path = entry_target.get()

        if not item_name or not target_path:
            messagebox.showerror("Error", "Please select an item and enter a target path.")
            return

        full_path = os.path.join(previous_path, item_name)
        target_full_path = os.path.join(target_path, item_name)

        try:
            if not os.path.exists(target_path):
                raise FileNotFoundError("Target path does not exist.")
            os.rename(full_path, target_full_path)
            messagebox.showinfo("Success", f"Item moved to {target_path}")
            update_combobox_items(previous_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to move item: {e}")

    main_create_button(text="Move", command=move_item, row=6, column=1)
    main_create_button(text="Back", command=files_menu, row=7, column=1)

def automations_menu():
    """Interface para gerenciamento de automações."""
    main_clear()
    main_title("Automations")

    main_create_button(text="Add Task", command=automations_add_task, row=1, column=1)
    main_create_button(text="Edit Task", command=automations_edit_task, row=2, column=1)
    main_create_button(text="Delete Task", command=automations_delete_task, row=3, column=1)
    main_create_button(text="Close", command=main_clear, row=4, column=1)

def automations_add_task():
    """Adiciona uma nova tarefa ao crontab com horário e comando."""
    
    def save_task():
        cron_time = entry_time.get().strip()
        cron_command = entry_command.get().strip()

        if not cron_time or not cron_command:
            messagebox.showerror("Error", "Time and Command fields cannot be empty!")
            return

        # Validação do formato de horário (5 campos ou asterisco)
        time_fields = cron_time.split()
        if len(time_fields) != 5:
            messagebox.showerror("Error", "Invalid time format! Must be 'min hour day month weekday'.")
            return

        # Permitir números ou asterisco como valores válidos nos campos de tempo
        for field in time_fields:
            if not (field.isdigit() or field == '*'):
                messagebox.showerror("Error", "Invalid time format! Use numbers or '*' for any field.")
                return

        try:
            # Escape de aspas no comando (isso assegura que as aspas sejam preservadas corretamente)
            cron_command_escaped = cron_command.replace('"', '\\"')  # Escapa aspas duplas
            
            # Escreve a tarefa no crontab
            result = subprocess.run(
                f'(crontab -l; echo "{cron_time} {cron_command_escaped}") | crontab -',
                shell=True,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                messagebox.showinfo("Success", "Task added successfully!")
                entry_time.delete(0, tk.END)
                entry_command.delete(0, tk.END)
            else:
                messagebox.showerror("Error", f"Failed to add task:\n{result.stderr}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    main_clear()
    main_title("Add Task")

    label_command = tk.Label(frame_main, text="Enter command to run:", font=("Segoe UI", 12), fg=config.color_label_text, bg=config.color_label_bg)
    label_command.grid(row=1, column=1, padx=10, pady=10)

    entry_command = tk.Entry(frame_main, font=("Segoe UI", 12), width=40)
    entry_command.grid(row=2, column=1, padx=10, pady=10)

    label_time = tk.Label(frame_main, text="Enter schedule (e.g., '* * * * *'):", font=("Segoe UI", 12), fg=config.color_label_text, bg=config.color_label_bg)
    label_time.grid(row=3, column=1, padx=10, pady=10)

    entry_time = tk.Entry(frame_main, font=("Segoe UI", 12), width=40)
    entry_time.grid(row=4, column=1, padx=10, pady=10)

    main_create_button(text="Save Task", command=save_task, row=5, column=1)
    main_create_button(text="Back", command=automations_menu, row=6, column=1)

def automations_edit_task():
    """Edita o horário de uma tarefa existente no crontab."""

    def load_tasks():
        """Carrega as tarefas existentes do crontab."""
        try:
            result = subprocess.run(
                ["crontab", "-l"],
                capture_output=True,
                text=True
            )

            if result.returncode != 0 or not result.stdout.strip():
                messagebox.showinfo("Info", "No tasks found in crontab.")
                return []

            # Retorna as tarefas como uma lista de strings
            return result.stdout.strip().splitlines()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while loading tasks: {e}")
            return []

    def confirm_edit():
        """Confirma e edita o horário da tarefa selecionada."""
        selected_task = combobox_tasks.get()
        new_time = entry_new_time.get().strip()

        if not selected_task:
            messagebox.showerror("Error", "You must select a task to edit!")
            return

        if not new_time:
            messagebox.showerror("Error", "New time cannot be empty!")
            return

        # Validação do horário (5 campos ou asterisco)
        time_fields = new_time.split()
        if len(time_fields) != 5:
            messagebox.showerror("Error", "Invalid time format! Must have 5 fields (min hour day month weekday).")
            return

        # Permitir números ou asterisco como valores válidos nos campos de tempo
        for field in time_fields:
            if not (field.isdigit() or field == '*'):
                messagebox.showerror("Error", "Invalid time format! Use numbers or '*' for any field.")
                return

        try:
            # Carrega todas as tarefas e edita a linha selecionada
            tasks = load_tasks()
            if not tasks:
                return

            updated_tasks = []
            for task in tasks:
                if task.strip() == selected_task.strip():
                    # Divide a tarefa em horário e comando
                    parts = task.split(' ', 5)  # Divide no máximo em 6 partes
                    if len(parts) >= 6:
                        # Substitui o horário da tarefa com o novo horário
                        updated_tasks.append(f"{new_time} {parts[5]}")
                    else:
                        # Se a tarefa não tiver o formato esperado, apenas copia a linha
                        updated_tasks.append(task)
                else:
                    updated_tasks.append(task)

            # Atualiza o crontab com as tarefas editadas
            result = subprocess.run(
                ["crontab", "-"],
                input="\n".join(updated_tasks) + "\n",  # Reescreve o crontab com as tarefas editadas
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                messagebox.showinfo("Success", f"Task '{selected_task}' updated successfully!")
                update_task_list()  # Atualiza a lista de tarefas após a edição
                entry_new_time.delete(0, tk.END)
            else:
                messagebox.showerror("Error", f"Failed to update crontab:\n{result.stderr}")

        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def update_task_list():
        """Atualiza a lista de tarefas no combobox."""
        tasks = load_tasks()
        combobox_tasks['values'] = tasks
        if tasks:
            combobox_tasks.set('')  # Limpa a seleção atual

    main_clear()
    main_title("Edit Task")

    # Carrega as tarefas existentes
    tasks = load_tasks()
    if not tasks:
        automations_menu()
        return

    label_task = tk.Label(frame_main,
                          text="Select a task to edit:",
                          font=("Segoe UI", 12),
                          fg=config.color_label_text,  # Cor do texto
                          bg=config.color_label_bg)    # Cor do fundo
    label_task.grid(row=1, column=1, padx=10, pady=10)

    combobox_tasks = ttk.Combobox(frame_main, font=("Segoe UI", 12), width=39, values=tasks)
    combobox_tasks.grid(row=2, column=1, padx=10, pady=10)
    combobox_tasks.set('')

    label_new_time = tk.Label(frame_main,
                              text="Enter new time (e.g., '0 5 * * *'):",
                              font=("Segoe UI", 12),
                              fg=config.color_label_text,  # Cor do texto
                              bg=config.color_label_bg)    # Cor do fundo
    label_new_time.grid(row=3, column=1, padx=10, pady=10)

    entry_new_time = tk.Entry(frame_main, font=("Segoe UI", 12), width=40)
    entry_new_time.grid(row=4, column=1, padx=10, pady=10)

    main_create_button(text="Save Changes", command=confirm_edit, row=5, column=1)
    main_create_button(text="Back", command=automations_menu, row=6, column=1)

def automations_delete_task():
    """Remove uma tarefa do crontab com seleção de tarefas existentes."""

    def load_tasks():
        """Carrega as tarefas existentes do crontab."""
        try:
            result = subprocess.run(
                ["crontab", "-l"],
                capture_output=True,
                text=True
            )

            if result.returncode != 0 or not result.stdout.strip():
                messagebox.showinfo("Info", "No tasks found in crontab.")
                return []

            # Retorna as tarefas como uma lista de strings
            return result.stdout.strip().splitlines()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while loading tasks: {e}")
            return []

    def confirm_delete():
        """Confirma e remove a tarefa selecionada."""
        selected_task = combobox_tasks.get()
        if not selected_task:
            messagebox.showerror("Error", "You must select a task to delete!")
            return

        try:
            # Carrega todas as tarefas e exclui a selecionada
            tasks = load_tasks()
            if not tasks:
                return

            # Remove a tarefa selecionada
            tasks = [task for task in tasks if task.strip() != selected_task.strip()]

            # Atualiza o crontab com as tarefas restantes
            if tasks:
                # Atualiza o crontab com as tarefas restantes
                result = subprocess.run(
                    ["crontab", "-"],
                    input="\n".join(tasks) + "\n",  # Reescreve o crontab com as tarefas restantes
                    capture_output=True,
                    text=True
                )

                if result.returncode == 0:
                    messagebox.showinfo("Success", f"Task '{selected_task}' removed successfully!")
                    update_task_list()  # Atualiza a lista de tarefas após a exclusão
                else:
                    messagebox.showerror("Error", f"Failed to update crontab:\n{result.stderr}")
            else:
                # Se não houver tarefas restantes, limpa o crontab
                result_clear = subprocess.run(
                    ["crontab", "-r"],  # Remove todas as tarefas
                    capture_output=True,
                    text=True
                )

                if result_clear.returncode == 0:
                    messagebox.showinfo("Success", f"Task '{selected_task}' removed successfully!")
                    update_task_list()
                else:
                    messagebox.showerror("Error", f"Failed to clear crontab:\n{result_clear.stderr}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def update_task_list():
        """Atualiza a lista de tarefas no combobox."""
        tasks = load_tasks()
        if tasks:
            combobox_tasks['values'] = tasks
            combobox_tasks.set('')  # Limpa a seleção atual
        else:
            automations_menu()

    main_clear()
    main_title("Delete Task")

    # Carrega as tarefas existentes
    tasks = load_tasks()
    if not tasks:
        automations_menu()
        return

    label_task = tk.Label(frame_main,
                          text="Select a task to delete:",
                          font=("Segoe UI", 12),
                          fg=config.color_label_text,  # Cor do texto
                          bg=config.color_label_bg)    # Cor do fundo
    label_task.grid(row=1, column=1, padx=10, pady=10)

    combobox_tasks = ttk.Combobox(frame_main, font=("Segoe UI", 12), width=39, values=tasks)
    combobox_tasks.grid(row=2, column=1, padx=10, pady=10)
    combobox_tasks.set("Select a task")

    main_create_button(text="Delete Task", command=confirm_delete, row=3, column=1)
    main_create_button(text="Back", command=automations_menu, row=4, column=1)

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

frame_main.grid_columnconfigure(0, weight=1)
frame_main.grid_columnconfigure(1, weight=1)
frame_main.grid_columnconfigure(2, weight=1)

""" NAV """
nav_create_button(text="Users", command=users_menu, row=0, column=0)
nav_create_button(text="System", command=system, row=0, column=1)
nav_create_button(text="Services", command=services, row=0, column=2)
nav_create_button(text="Files", command=files_menu, row=0, column=3)
nav_create_button(text="Automations", command=automations_menu, row=0, column=4)
main_title("Welcome to Linux Controller!")

""" MAIN """
root.mainloop()