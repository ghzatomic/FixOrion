import os
import urllib.request
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from datetime import datetime

# Função para renomear o arquivo existente, caso já exista
def rename_existing_file(file_path):
    if os.path.exists(file_path):
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_file_name = f"Cliloc_old_{current_time}.enu"
        new_file_path = os.path.join(os.path.dirname(file_path), new_file_name)
        os.rename(file_path, new_file_path)
        messagebox.showinfo("Arquivo Existente", f"O arquivo existente foi renomeado para: {new_file_name}")

# Função para baixar o arquivo do FTP com barra de progresso
def download_file(destination_folder):
    url = "https://gildakp.altervista.org/UO/Cliloc.enu"
    file_name = os.path.join(destination_folder, "Cliloc.enu")

    # Verifica se o arquivo já existe e renomeia
    rename_existing_file(file_name)
    
    def reporthook(count, block_size, total_size):
        progress = int(count * block_size * 100 / total_size)
        progress_var.set(progress)
        root.update_idletasks()

    try:
        urllib.request.urlretrieve(url, file_name, reporthook)
        messagebox.showinfo("Sucesso", f"Download concluído e salvo em: {file_name}")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha no download: {e}")
    
    # Após o download, reiniciar a barra de progresso
    progress_var.set(0)

# Função chamada ao clicar no botão para selecionar a pasta
def select_folder():
    folder_selected = filedialog.askdirectory(initialdir=r"C:\Program Files (x86)\Electronic Arts\Ultima Online Classic")
    if folder_selected:
        folder_label.config(text=folder_selected)
        selected_folder_label.config(text=f"Pasta selecionada: {folder_selected}")

# Função chamada ao clicar no botão "Iniciar Fix"
def start_fix():
    folder = folder_label.cget("text")
    if folder:
        download_file(folder)
    else:
        messagebox.showwarning("Atenção", "Por favor, selecione uma pasta de destino.")

# Interface gráfica usando Tkinter
root = tk.Tk()
root.title("Download Fix - Scrambler & GHZATOMIC")

# Label para exibir a pasta selecionada
folder_label = tk.Label(root, text="Selecione uma pasta de destino", width=60)
folder_label.pack(pady=10)

# Botão para selecionar a pasta de destino
select_button = tk.Button(root, text="Selecionar Pasta", command=select_folder)
select_button.pack(pady=10)

# Label para mostrar qual pasta foi selecionada (com centralização)
selected_folder_label = tk.Label(root, text="Pasta selecionada: Nenhuma", width=80, anchor='center')
selected_folder_label.pack(pady=10)

# Barra de progresso
progress_var = tk.IntVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100, length=400)
progress_bar.pack(pady=10)

# Botão para iniciar o download
start_button = tk.Button(root, text="Iniciar Fix", command=start_fix)
start_button.pack(pady=10)

# Label com os créditos
credits_label = tk.Label(root, text="Feito por Scrambler & GHZATOMIC", font=("Arial", 10), fg="gray")
credits_label.pack(pady=20)

# Executa a aplicação
root.mainloop()
