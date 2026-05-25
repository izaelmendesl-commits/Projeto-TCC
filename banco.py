import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Função para conectar ao banco
def conectar():
    try:
        conexao = mysql.connector.connect(
            host="localhost",       # servidor
            user="root",            # usuário do MySQL
            password="IzaelMendes123",  
            database="avisos_sistema"  # nome do banco
        )

        if conexao.is_connected():
            messagebox.showinfo("Conexão", "Banco conectado com sucesso!")

            cursor = conexao.cursor()

            # Exemplo de comando SQL
            cursor.execute("SHOW TABLES")

            tabelas = cursor.fetchall()

            texto = "Tabelas do banco:\n"
            for tabela in tabelas:
                texto += f"{tabela[0]}\n"

            resultado.config(text=texto)

            cursor.close()
            conexao.close()

    except mysql.connector.Error as erro:
        messagebox.showerror("Erro", f"Erro ao conectar:\n{erro}")

# Janela Tkinter
janela = tk.Tk()
janela.title("Conexão MySQL")
janela.geometry("400x300")

titulo = tk.Label(janela, text="Teste de Conexão MySQL", font=("Arial", 14))
titulo.pack(pady=10)

botao = tk.Button(janela, text="Conectar", command=conectar)
botao.pack(pady=10)

resultado = tk.Label(janela, text="")
resultado.pack(pady=10)

janela.mainloop()