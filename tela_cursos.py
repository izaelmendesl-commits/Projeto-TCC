import tkinter as tk
from tkinter import messagebox
import mysql.connector

class TelaCadastroCurso:
    def __init__(self, master):
        self.master = master
        self.master.title("Cadastro de Cursos - Sistema de Avisos")
        self.master.geometry("450x350")
        self.master.resizable(False, False)

        # Variáveis para armazenar os dados
        self.codigo_var = tk.StringVar()
        self.descricao_var = tk.StringVar()
        self.acao_atual = None  

        self.frame_principal = tk.Frame(self.master, padx=20, pady=20)
        self.frame_principal.pack(fill=tk.BOTH, expand=True)

        # Linha 1: Código do Curso e Lupa 
        self.lbl_codigo = tk.Label(self.frame_principal, text="Código Curso:")
        self.lbl_codigo.grid(row=0, column=0, sticky="e", pady=5, padx=5)
        
        self.ent_codigo = tk.Entry(self.frame_principal, textvariable=self.codigo_var, width=10)
        self.ent_codigo.grid(row=0, column=1, sticky="w", pady=5)
        
        self.btn_buscar = tk.Button(self.frame_principal, text="🔍", command=self.buscar_curso)
        self.btn_buscar.grid(row=0, column=2, sticky="w", padx=5)

        # Linha 2: Descrição do Curso
        self.lbl_descricao = tk.Label(self.frame_principal, text="Descrição:")
        self.lbl_descricao.grid(row=1, column=0, sticky="e", pady=5, padx=5)
        
        self.ent_descricao = tk.Entry(self.frame_principal, textvariable=self.descricao_var, width=25)
        self.ent_descricao.grid(row=1, column=1, columnspan=2, sticky="w", pady=5)

        # Frame para os Botões 
        self.frame_botoes = tk.Frame(self.master, pady=10)
        self.frame_botoes.pack()

        # Botões de Ação 
        self.btn_alterar = tk.Button(self.frame_botoes, text="Alterar", width=10, command=self.preparar_alterar)
        self.btn_alterar.grid(row=0, column=0, padx=5, pady=5)
        
        self.btn_excluir = tk.Button(self.frame_botoes, text="Excluir", width=10, command=self.preparar_excluir)
        self.btn_excluir.grid(row=0, column=1, padx=5, pady=5)

        # Botões de Confirmação 
        self.btn_confirmar = tk.Button(self.frame_botoes, text="Confirmar", width=10, command=self.confirmar)
        self.btn_cancelar = tk.Button(self.frame_botoes, text="Cancelar", width=10, command=self.cancelar)

    # --- INTEGRAÇÃO COM O BANCO DE DADOS ---

    def conectar_banco(self):
        """Estabelece a conexão com o banco de dados avisos_sistema."""
        try:
            conexao = mysql.connector.connect(
                host="localhost",
                user="root",
                password="IzaelMendes123",
                database="avisos_sistema"
            )
            return conexao
        except mysql.connector.Error as erro:
            messagebox.showerror("Erro de Conexão", f"Não foi possível conectar ao banco:\n{erro}")
            return None

    def buscar_curso(self):
        codigo = self.codigo_var.get()
        if not codigo:
            messagebox.showwarning("Aviso", "Digite um Código de Curso para buscar.")
            return

        conexao = self.conectar_banco()
        if conexao:
            try:
                cursor = conexao.cursor()
                # CORREÇÃO: Alterado de 'codigo' para 'codcurso'
                comando = "SELECT descricao FROM cursos WHERE codcurso = %s"
                cursor.execute(comando, (codigo,))
                resultado = cursor.fetchone()

                if resultado:
                    self.descricao_var.set(resultado[0])
                    messagebox.showinfo("Busca", f"Curso {codigo} encontrado com sucesso!")
                else:
                    self.descricao_var.set("")
                    messagebox.showwarning("Aviso", f"O curso com código {codigo} não existe no banco.")
            except mysql.connector.Error as erro:
                messagebox.showerror("Erro de SQL", f"Erro ao buscar dados:\n{erro}")
            finally:
                cursor.close()
                conexao.close()

    def confirmar(self):
        codigo = self.codigo_var.get()
        descricao = self.descricao_var.get()
        
        conexao = self.conectar_banco()
        if conexao:
            try:
                cursor = conexao.cursor()
                
                if self.acao_atual == "ALTERAR":
                    # CORREÇÃO: Alterado de 'codigo' para 'codcurso'
                    comando = "UPDATE cursos SET descricao = %s WHERE codcurso = %s"
                    cursor.execute(comando, (descricao, codigo))
                    conexao.commit()
                    messagebox.showinfo("Sucesso", "Dados do curso alterados com sucesso!")
                    
                elif self.acao_atual == "EXCLUIR":
                    # CORREÇÃO: Alterado de 'codigo' para 'codcurso'
                    comando = "DELETE FROM cursos WHERE codcurso = %s"
                    cursor.execute(comando, (codigo,))
                    conexao.commit()
                    messagebox.showinfo("Sucesso", f"O curso {codigo} foi excluído do sistema!")
                
                self.limpar_e_resetar()

            except mysql.connector.Error as erro:
                messagebox.showerror("Erro de SQL", f"Erro ao executar a operação:\n{erro}")
            finally:
                cursor.close()
                conexao.close()

    # --- LÓGICA DE INTERFACE ---

    def mostrar_botoes(self):
        self.btn_confirmar.grid(row=1, column=0, padx=5, pady=5)
        self.btn_cancelar.grid(row=1, column=1, padx=5, pady=5)

    def esconder_botoes(self):
        self.btn_confirmar.grid_remove()
        self.btn_cancelar.grid_remove()

    def preparar_alterar(self):
        if not self.codigo_var.get() or not self.descricao_var.get():
            messagebox.showwarning("Aviso", "Busque um curso primeiro antes de alterar.")
            return
        
        self.acao_atual = "ALTERAR"
        self.mostrar_botoes()

    def preparar_excluir(self):
        if not self.codigo_var.get() or not self.descricao_var.get():
            messagebox.showwarning("Aviso", "Busque um curso primeiro antes de excluir.")
            return

        self.acao_atual = "EXCLUIR"
        self.mostrar_botoes()

    def cancelar(self):
        self.limpar_e_resetar()

    def limpar_e_resetar(self):
        self.codigo_var.set("")
        self.descricao_var.set("")
        self.esconder_botoes()
        self.acao_atual = None


# Inicialização do Programa
if __name__ == "__main__":
    root = tk.Tk()
    app = TelaCadastroCurso(root)
    root.mainloop()