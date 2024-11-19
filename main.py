import psutil
import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import subprocess
import config
import random

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
    
    def update_system_info():
        """Atualiza as informações de uso de CPU, memória e disco a cada 1 segundo."""
        if not label_cpu_usage.winfo_exists():  # Verifica se o rótulo ainda existe
            return

        cpu_usage = psutil.cpu_percent(interval=1)  # Uso de CPU em porcentagem
        memory_info = psutil.virtual_memory()  # Informações de memória
        memory_usage = memory_info.percent  # Percentual de memória usada
        disk_info = psutil.disk_usage('/')  # Uso de disco na raiz
        disk_usage = disk_info.percent  # Percentual de uso do disco

        # Atualiza os rótulos com as novas informações
        label_cpu_usage.config(text=f"CPU Usage: {cpu_usage}%")
        label_memory_usage.config(text=f"Memory Usage: {memory_usage}%")
        label_disk_usage.config(text=f"Disk Usage: {disk_usage}%")

        # Atualiza as informações a cada 1000 ms (1 segundo)
        root.after(1000, update_system_info)


    # Limpa a interface principal
    main_clear()
    main_title("System Monitoring")

    # Rótulos para exibir as informações
    label_cpu_usage = tk.Label(frame_main,
                               text="CPU Usage: 0%",
                               font=("Segoe UI", 12),
                               fg=config.color_label_text,
                               bg=config.color_label_bg)
    label_cpu_usage.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

    label_memory_usage = tk.Label(frame_main,
                                  text="Memory Usage: 0%",
                                  font=("Segoe UI", 12),
                                  fg=config.color_label_text,
                                  bg=config.color_label_bg)
    label_memory_usage.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

    label_disk_usage = tk.Label(frame_main,
                                text="Disk Usage: 0%",
                                font=("Segoe UI", 12),
                                fg=config.color_label_text,
                                bg=config.color_label_bg)
    label_disk_usage.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

    # Botão para voltar ao menu anterior
    main_create_button(text="Close", command=main_clear, row=4, column=1)

    # Começa a atualização das informações de sistema
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
    main_create_button(text="Back", command=main_clear, row=6, column=1)

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

frame_main.grid_columnconfigure(0, weight=1)
frame_main.grid_columnconfigure(1, weight=1)
frame_main.grid_columnconfigure(2, weight=1)

""" NAV """
nav_create_button(text="Users", command=users_menu, row=0, column=0)
nav_create_button(text="System", command=system, row=0, column=1)
nav_create_button(text="Services", command=services, row=0, column=2)
nav_create_button(text="Files", command=lambda: test("Files"), row=0, column=3)
nav_create_button(text="Automations", command=lambda: test("Automations"), row=0, column=4)

""" MAIN """
root.mainloop()