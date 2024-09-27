import os
import urllib.request
import zipfile
import rarfile
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from datetime import datetime
import threading  # Para mover o download e a extração para uma thread separada

# Função para renomear o arquivo existente
def rename_existing_file(file_path):
    if os.path.exists(file_path):
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_file_name = f"{os.path.basename(file_path).split('.')[0]}_old_{current_time}.{os.path.basename(file_path).split('.')[-1]}"
        new_file_path = os.path.join(os.path.dirname(file_path), new_file_name)
        os.rename(file_path, new_file_path)
        messagebox.showinfo("Arquivo Existente", f"O arquivo existente foi renomeado para: {new_file_name}")

# Função para descompactar o ZIP e renomear arquivos existentes com barra de progresso
def extract_zip(destination_folder, zip_file_path):
    try:
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            files_in_zip = zip_ref.namelist()  # Lista todos os arquivos no zip
            total_files = len([f for f in files_in_zip if os.path.basename(f)])  # Conta os arquivos (ignora pastas)

            # Atualiza a barra de progresso para o total de arquivos
            progress_var.set(0)
            progress_step = 100 / total_files if total_files > 0 else 1

            extracted_files_count = 0

            # Atualiza o status para extração
            status_label.config(text="Extraindo arquivos ZIP...")

            # Para cada arquivo no zip, extrai diretamente na pasta de destino
            for file_name in files_in_zip:
                base_name = os.path.basename(file_name)

                if base_name:  # Apenas extrair se for um arquivo, não uma pasta
                    extracted_path = os.path.join(destination_folder, base_name)

                    # Renomeia o arquivo existente, se já estiver na pasta de destino
                    rename_existing_file(extracted_path)

                    # Extrai o arquivo diretamente na pasta de destino
                    with zip_ref.open(file_name) as source_file:
                        with open(extracted_path, "wb") as target_file:
                            target_file.write(source_file.read())

                    # Atualiza o progresso
                    extracted_files_count += 1
                    progress_var.set(progress_step * extracted_files_count)
                    status_label.config(text=f"Extraindo arquivo ZIP {extracted_files_count} de {total_files}")
                    root.update_idletasks()  # Atualiza a interface

        status_label.config(text="Extração do ZIP concluída.")
        messagebox.showinfo("Sucesso", f"Arquivos extraídos com sucesso em: {destination_folder}")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao descompactar o arquivo ZIP: {e}")
        status_label.config(text="Erro durante a extração do ZIP.")

# Função para baixar o arquivo RAR e mostrar progresso
def download_file(url, destination_path):
    # Função de callback para monitorar o progresso do download
    def reporthook(count, block_size, total_size):
        downloaded = count * block_size
        percent = int(downloaded * 100 / total_size)
        progress_var.set(percent)
        status_label.config(text=f"Baixando... {downloaded // (1024)} KB de {total_size // (1024)} KB ({percent}%)")
        root.update_idletasks()  # Atualiza a interface

    try:
        # Atualiza o status para mostrar que está baixando
        status_label.config(text="Iniciando o download do RAR...")
        urllib.request.urlretrieve(url, destination_path, reporthook)
        status_label.config(text="Download do RAR concluído.")
        return True
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao baixar o arquivo: {e}")
        return False

# Função para descompactar o RAR e renomear arquivos existentes com barra de progresso
def extract_rar(destination_folder, rar_file_path):
    try:
        with rarfile.RarFile(rar_file_path, 'r') as rar_ref:
            files_in_rar = rar_ref.namelist()  # Lista todos os arquivos no rar
            total_files = len([f for f in files_in_rar if os.path.basename(f)])  # Conta os arquivos (ignora pastas)

            # Atualiza a barra de progresso para o total de arquivos
            progress_var.set(0)
            progress_step = 100 / total_files if total_files > 0 else 1

            extracted_files_count = 0

            # Atualiza o status para extração
            status_label.config(text="Extraindo arquivos RAR...")

            # Para cada arquivo no rar, extrai diretamente na pasta de destino
            for file_name in files_in_rar:
                base_name = os.path.basename(file_name)

                if base_name:  # Apenas extrair se for um arquivo, não uma pasta
                    extracted_path = os.path.join(destination_folder, base_name)

                    # Renomeia o arquivo existente, se já estiver na pasta de destino
                    rename_existing_file(extracted_path)

                    # Extrai o arquivo diretamente na pasta de destino
                    with rar_ref.open(file_name) as source_file:
                        with open(extracted_path, "wb") as target_file:
                            target_file.write(source_file.read())

                    # Atualiza o progresso
                    extracted_files_count += 1
                    progress_var.set(progress_step * extracted_files_count)
                    status_label.config(text=f"Extraindo arquivo RAR {extracted_files_count} de {total_files}")
                    root.update_idletasks()  # Atualiza a interface

        status_label.config(text="Extração do RAR concluída.")
        messagebox.showinfo("Sucesso", f"Arquivos extraídos com sucesso em: {destination_folder}")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao descompactar o arquivo RAR: {e}")
        status_label.config(text="Erro durante a extração do RAR.")

# Função chamada ao clicar no botão para selecionar a pasta
def select_folder():
    folder_selected = filedialog.askdirectory()
    
    if folder_selected:
        folder_label.config(text=folder_selected)
        selected_folder_label.config(text=f"Pasta selecionada: {folder_selected}")

# Função para iniciar o processo em uma nova thread (evita o travamento da interface)
def start_fix_thread(folder):
    zip_file_path = os.path.join(os.getcwd(), "Uofixer.zip")
    rar_file_path = os.path.join(os.getcwd(), "Uofixer_01.rar")
    
    if os.path.exists(zip_file_path):
        # Se o ZIP estiver na raiz, extrai diretamente o ZIP
        extract_zip(folder, zip_file_path)
    elif os.path.exists(rar_file_path):
        # Se o RAR estiver na raiz, extrai diretamente o RAR
        extract_rar(folder, rar_file_path)
    else:
        # Se nenhum dos arquivos estiver presente, baixa o RAR e extrai
        rar_url = "https://gildakp.altervista.org/UO/Uofixer_01.rar"
        if download_file(rar_url, rar_file_path):
            # Se o download foi bem-sucedido, descompacta o RAR
            extract_rar(folder, rar_file_path)

# Função chamada ao clicar no botão "Iniciar Fix"
def start_fix():
    folder = folder_label.cget("text")
    if folder:
        # Iniciar o processo em uma nova thread
        threading.Thread(target=start_fix_thread, args=(folder,), daemon=True).start()
    else:
        messagebox.showwarning("Atenção", "Por favor, selecione a pasta do Ultima Online.")

# Interface gráfica usando Tkinter
root = tk.Tk()
root.title("Download Fix - Scrambler & GHZATOMIC")

# Label para exibir a pasta selecionada
folder_label = tk.Label(root, text="Selecione a pasta do Ultima Online", width=60)
folder_label.pack(pady=10)

# Botão para selecionar a pasta de destino
select_button = tk.Button(root, text="Selecionar Pasta", command=select_folder)
select_button.pack(pady=10)

# Label para mostrar qual pasta foi selecionada (com centralização)
selected_folder_label = tk.Label(root, text="Pasta selecionada: Nenhuma", width=80, anchor='center')
selected_folder_label.pack(pady=10)

# Barra de progresso
progress_var = tk.DoubleVar()  # Usamos DoubleVar para permitir passos com decimais
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100, length=400)
progress_bar.pack(pady=10)

# Status Label para mostrar o que está acontecendo no momento
status_label = tk.Label(root, text="Status: Aguardando ação do usuário", width=80)
status_label.pack(pady=10)

# Adicionar o Label que informa sobre o WinRAR
winrar_label = tk.Label(root, text="Se o Uofixer.zip não estiver na raiz, é necessário ter o WinRAR instalado.", fg="red", font=("Arial", 10))
winrar_label.pack(pady=10)

# Botão para iniciar o processo
start_button = tk.Button(root, text="Iniciar Fix", command=start_fix)
start_button.pack(pady=10)

# Label com os créditos
credits_label = tk.Label(root, text="Feito por Scrambler & GHZATOMIC", font=("Arial", 10), fg="gray")
credits_label.pack(pady=20)

# Executa a aplicação
root.mainloop()
