import customtkinter as ctk
from tkinter import messagebox
import mysql.connector
import os
from PIL import Image

# --- CONFIGURAÇÃO INICIAL DE INTERFACE ---
ctk.set_appearance_mode("Light")  
ctk.set_default_color_theme("blue") 

class TelaCadastroTurmas:
    def __init__(self, master):
        self.master = master
        self.master.title("Sistema de Avisos - Painel Univap (Turmas)")
        
        # --- DESIGN RESPONSIVO ---
        self.master.geometry("1100x650")     
        self.master.minsize(850, 550)        
        self.master.resizable(True, True)   
        self.master.state('zoomed')         

        # --- PALETA DE CORES ---
        self.cor_fundo_tech = ("#F4F7FA", "#0F172A")       
        self.cor_card_branco = ("#FFFFFF", "#1E293B")      
        self.cor_univap_azul = ("#0056B3", "#3B82F6")      
        self.cor_univap_escuro = ("#003366", "#60A5FA")    
        self.cor_borda = ("#E2E8F0", "#334155")            
        self.cor_texto_principal = ("#1A4EA2", "#F8FAFC")  
        self.cor_texto_secundario = ("#64748B", "#B894AC") 
        self.cor_perigo = ("#EF4444", "#EF4444")           
        self.cor_sucesso = ("#10B981", "#10B981")          

        self.master.configure(fg_color=self.cor_fundo_tech)

        # Variáveis da Tela
        self.codturma_var = ctk.StringVar()
        self.curso_selecionado_var = ctk.StringVar()
        self.busca_tabela_var = ctk.StringVar() 
        self.acao_atual = None  
        
        # Dicionário para guardar a relação "Nome exibido" -> "Código do Curso Real"
        self.mapeamento_cursos = {}

        self.criar_interface()
        
        # Carrega os dados iniciais
        if self.testar_conexao_inicial():
            self.carregar_cursos_do_banco()
            self.atualizar_dados_reais() 

    def mudar_tema(self, escolha):
        ctk.set_appearance_mode("Dark" if escolha == "Escuro" else "Light")

    def testar_conexao_inicial(self):
        conexao = self.conectar_banco(silencioso=True)
        if conexao:
            conexao.close()
            return True
        else:
            messagebox.showerror("Erro", "Falha de conexão com o Banco de Dados.")
            return False

    def conectar_banco(self, silencioso=False):
        try:
            conexao = mysql.connector.connect(
                host="localhost",
                user="root",
                password="IzaelMendes123", 
                database="avisos_sistema"
            )
            return conexao
        except mysql.connector.Error as erro:
            if not silencioso:
                messagebox.showerror("Erro de Conexão", f"Falha ao conectar com o MySQL:\n{erro}")
            return None

    def carregar_cursos_do_banco(self):
        """Puxa os cursos da tabela 'cursos' para preencher o menu suspenso em ordem alfabética"""
        conexao = self.conectar_banco(silencioso=True)
        if conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute("SELECT codcurso, descricao FROM cursos ORDER BY descricao ASC")
                resultados = cursor.fetchall()
                
                self.mapeamento_cursos.clear()
                lista_exibicao = []
                
                for cod, desc in resultados:
                    texto = f"{cod} - {desc}"
                    lista_exibicao.append(texto)
                    self.mapeamento_cursos[texto] = cod
                
                if lista_exibicao:
                    self.ent_curso.configure(values=lista_exibicao)
                    self.curso_selecionado_var.set(lista_exibicao[0])
                else:
                    self.ent_curso.configure(values=["Nenhum curso cadastrado"])
                    self.curso_selecionado_var.set("Nenhum curso cadastrado")
            except Exception as erro:
                print(f"Erro ao carregar cursos: {erro}")
            finally:
                cursor.close()
                conexao.close()

    def criar_interface(self):
        # --- CABEÇALHO ---
        self.frame_header = ctk.CTkFrame(self.master, corner_radius=0, fg_color=self.cor_card_branco, border_width=1, border_color=self.cor_borda)
        self.frame_header.pack(fill="x", pady=(0, 20))

        container_top = ctk.CTkFrame(self.frame_header, fg_color="transparent")
        container_top.pack(padx=30, pady=12, fill="x")

        caminho_imagem = "logo_univap.png" 
        lbl_logo = None
        if os.path.exists(caminho_imagem):
            try:
                img_aberta = Image.open(caminho_imagem)
                imagem = ctk.CTkImage(light_image=img_aberta, dark_image=img_aberta, size=(55, 55))
                lbl_logo = ctk.CTkLabel(container_top, image=imagem, text="")
            except Exception:
                pass
        
        if not lbl_logo:
            lbl_logo = ctk.CTkLabel(container_top, text="UNIVAP", font=ctk.CTkFont(weight="bold"), fg_color=self.cor_univap_azul, text_color="white", width=55, height=55, corner_radius=6)
        lbl_logo.pack(side="left", padx=(0, 15))

        self.lbl_titulo = ctk.CTkLabel(container_top, text="Gerenciamento de Turmas", font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"), text_color=self.cor_univap_escuro)
        self.lbl_titulo.pack(side="left", anchor="center")

        self.menu_tema = ctk.CTkOptionMenu(container_top, values=["Claro", "Escuro"], width=90, height=28, fg_color=self.cor_univap_azul, button_color=self.cor_univap_azul, button_hover_color=self.cor_univap_escuro, command=self.mudar_tema)
        self.menu_tema.pack(side="right", anchor="center", padx=(10, 0))
        self.menu_tema.set("Claro")

        self.lbl_tema_texto = ctk.CTkLabel(container_top, text="Tema:", font=ctk.CTkFont(size=12, weight="bold"), text_color=self.cor_texto_principal)
        self.lbl_tema_texto.pack(side="right", anchor="center")

        # --- CORPO DA TELA DIVIDIDO ---
        body_container = ctk.CTkFrame(self.master, fg_color="transparent")
        body_container.pack(fill="both", expand=True, padx=30, pady=(0, 20))
        
        body_container.grid_columnconfigure(0, weight=0) 
        body_container.grid_columnconfigure(1, weight=1) 
        body_container.grid_rowconfigure(0, weight=1)

        # ==========================================
        # PAINEL ESQUERDO: ÁREA DE CADASTRO
        # ==========================================
        left_panel = ctk.CTkFrame(body_container, fg_color="transparent", width=400)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
        
        self.frame_form = ctk.CTkFrame(left_panel, corner_radius=12, fg_color=self.cor_card_branco, border_width=1, border_color=self.cor_borda)
        self.frame_form.pack(fill="both", expand=True)

        self.lbl_instrucao = ctk.CTkLabel(self.frame_form, text="ÁREA DE CADASTRO - TURMA", font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"), text_color=self.cor_univap_azul)
        self.lbl_instrucao.grid(row=0, column=0, columnspan=2, pady=(25, 20), padx=25, sticky="w")

        # Campo: Código da Turma
        self.lbl_codturma = ctk.CTkLabel(self.frame_form, text="Código da Turma", font=ctk.CTkFont(size=13, weight="bold"), text_color=self.cor_texto_principal)
        self.lbl_codturma.grid(row=1, column=0, sticky="w", pady=(5, 2), padx=25)
        
        search_block = ctk.CTkFrame(self.frame_form, fg_color="transparent")
        search_block.grid(row=2, column=0, columnspan=2, sticky="w", padx=25, pady=(0, 15))
        
        self.ent_codturma = ctk.CTkEntry(search_block, textvariable=self.codturma_var, width=140, height=36, corner_radius=6)
        self.ent_codturma.pack(side="left", padx=(0, 10))
        self.ent_codturma.bind("<KeyRelease>", lambda e: self.codturma_var.set(self.codturma_var.get().upper()))
        
        self.btn_buscar = ctk.CTkButton(search_block, text="🔍 Buscar", width=110, height=36, corner_radius=6, fg_color=self.cor_univap_azul, hover_color=self.cor_univap_escuro, command=self.buscar_turma)
        self.btn_buscar.pack(side="left")

        # Campo: Vincular ao Curso (COMBOBOX)
        self.lbl_curso = ctk.CTkLabel(self.frame_form, text="Vincular ao Curso", font=ctk.CTkFont(size=13, weight="bold"), text_color=self.cor_texto_principal)
        self.lbl_curso.grid(row=3, column=0, sticky="w", pady=(10, 2), padx=25)
        
        self.ent_curso = ctk.CTkOptionMenu(self.frame_form, variable=self.curso_selecionado_var, values=["Carregando..."], width=340, height=36, corner_radius=6, fg_color=self.cor_fundo_tech, button_color=self.cor_borda, button_hover_color=self.cor_texto_secundario, text_color=self.cor_texto_principal)
        self.ent_curso.grid(row=4, column=0, columnspan=2, sticky="w", pady=(0, 30), padx=25)

        # Botões Principais
        self.container_botoes_acoes = ctk.CTkFrame(left_panel, fg_color="transparent")
        self.container_botoes_acoes.pack(fill="x", pady=(15, 0))

        self.frame_botoes = ctk.CTkFrame(self.container_botoes_acoes, fg_color="transparent")
        self.frame_botoes.pack(fill="x")

        self.btn_inserir = ctk.CTkButton(self.frame_botoes, text="➕ Inserir", height=42, fg_color=("#003366", "#1E3A8A"), command=self.preparar_inserir)
        self.btn_inserir.pack(side="left", expand=True, fill="x", padx=(0, 5))

        self.btn_alterar = ctk.CTkButton(self.frame_botoes, text="✏️ Alterar", height=42, fg_color=self.cor_univap_azul, command=self.preparar_alterar)
        self.btn_alterar.pack(side="left", expand=True, fill="x", padx=5)
        
        self.btn_excluir = ctk.CTkButton(self.frame_botoes, text="🗑️ Excluir", height=42, fg_color=self.cor_perigo, command=self.preparar_excluir)
        self.btn_excluir.pack(side="left", expand=True, fill="x", padx=(5, 0))

        # Botões de Confirmação
        self.frame_confirma = ctk.CTkFrame(self.container_botoes_acoes, fg_color="transparent")
        self.btn_confirmar = ctk.CTkButton(self.frame_confirma, text="✔️ Confirmar", fg_color=self.cor_sucesso, height=42, font=ctk.CTkFont(weight="bold"), command=self.confirmar)
        self.btn_confirmar.pack(side="left", expand=True, fill="x", padx=(0, 5))
        self.btn_cancelar = ctk.CTkButton(self.frame_confirma, text="❌ Cancelar", height=42, fg_color="transparent", border_width=1, border_color=self.cor_perigo, text_color=self.cor_perigo, command=self.cancelar)
        self.btn_cancelar.pack(side="left", expand=True, fill="x", padx=(5, 0))

        # ==========================================
        # PAINEL DIREITO: VISUALIZAÇÃO (TABELA)
        # ==========================================
        right_panel = ctk.CTkFrame(body_container, fg_color="transparent")
        right_panel.grid(row=0, column=1, sticky="nsew")
        right_panel.grid_rowconfigure(0, weight=0) 
        right_panel.grid_rowconfigure(1, weight=1) 
        right_panel.grid_columnconfigure(0, weight=1)

        # Card de Totalizador
        card_total = ctk.CTkFrame(right_panel, fg_color=self.cor_card_branco, border_width=1, border_color=self.cor_borda, height=65, corner_radius=8)
        card_total.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        card_total.pack_propagate(False)
        
        ctk.CTkLabel(card_total, text="Total de Turmas Cadastradas:", font=ctk.CTkFont(size=12, weight="bold"), text_color=self.cor_texto_secundario).pack(side="left", padx=20)
        self.lbl_metric_total = ctk.CTkLabel(card_total, text="0", font=ctk.CTkFont(size=22, weight="bold"), text_color=self.cor_univap_azul)
        self.lbl_metric_total.pack(side="right", padx=20)

        # Card da Tabela
        table_card = ctk.CTkFrame(right_panel, corner_radius=12, fg_color=self.cor_card_branco, border_width=1, border_color=self.cor_borda)
        table_card.grid(row=1, column=0, sticky="nsew")
        
        table_header = ctk.CTkFrame(table_card, fg_color="transparent")
        table_header.pack(fill="x", padx=20, pady=12)
        
        ctk.CTkLabel(table_header, text="Lista Oficial de Turmas", font=ctk.CTkFont(size=13, weight="bold"), text_color=self.cor_texto_principal).pack(side="left")
        
        self.ent_pesquisa = ctk.CTkEntry(table_header, textvariable=self.busca_tabela_var, placeholder_text="Buscar turma...", width=200, height=30)
        self.ent_pesquisa.pack(side="right", padx=5)
        self.ent_pesquisa.bind("<KeyRelease>", lambda e: self.atualizar_dados_reais())

        # Area de Scroll da Tabela
        self.scroll_table = ctk.CTkScrollableFrame(table_card, fg_color=self.cor_fundo_tech, corner_radius=6)
        self.scroll_table.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def atualizar_dados_reais(self):
        for widget in self.scroll_table.winfo_children():
            widget.destroy()

        h_frame = ctk.CTkFrame(self.scroll_table, fg_color="transparent")
        h_frame.pack(fill="x", pady=2)
        ctk.CTkLabel(h_frame, text="CURSO VINCULADO", font=ctk.CTkFont(size=11, weight="bold"), width=300, anchor="w", text_color=self.cor_texto_secundario).pack(side="left", padx=10)
        ctk.CTkLabel(h_frame, text="TURMA", font=ctk.CTkFont(size=11, weight="bold"), anchor="w", text_color=self.cor_texto_secundario).pack(side="left", padx=10, fill="x", expand=True)

        conexao = self.conectar_banco(silencioso=True)
        if conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute("SELECT COUNT(*) FROM turmas")
                self.lbl_metric_total.configure(text=str(cursor.fetchone()[0]))
                
                filtro = self.busca_tabela_var.get().strip()
                comando_base = """
                    SELECT t.codturma, c.descricao 
                    FROM turmas t
                    LEFT JOIN cursos c ON t.codcurso = c.codcurso
                """
                
                if filtro:
                    comando = comando_base + " WHERE t.codturma LIKE %s OR c.descricao LIKE %s ORDER BY c.descricao ASC, t.codturma ASC"
                    cursor.execute(comando, (f"%{filtro}%", f"%{filtro}%"))
                else:
                    comando = comando_base + " ORDER BY c.descricao ASC, t.codturma ASC"
                    cursor.execute(comando)
                    
                for codturma, nome_curso in cursor.fetchall():
                    row = ctk.CTkFrame(self.scroll_table, height=38, fg_color=self.cor_card_branco, corner_radius=6, border_width=1, border_color=self.cor_borda)
                    row.pack(fill="x", pady=3, padx=2)
                    row.pack_propagate(False)
                    
                    curso_exibir = nome_curso if nome_curso else "Curso Removido"
                    
                    ctk.CTkLabel(row, text=curso_exibir, font=ctk.CTkFont(size=12), width=300, anchor="w", text_color=self.cor_texto_principal).pack(side="left", padx=10)
                    ctk.CTkLabel(row, text=str(codturma), font=ctk.CTkFont(size=13, weight="bold"), anchor="w", text_color=self.cor_univap_azul).pack(side="left", padx=10, fill="x", expand=True)
            except Exception as e:
                print(e)
            finally:
                cursor.close()
                conexao.close()

    def buscar_turma(self):
        codturma = self.codturma_var.get().strip()
        if not codturma:
            messagebox.showwarning("Aviso", "Digite o Código da Turma para buscar.")
            return

        conexao = self.conectar_banco()
        if conexao:
            try:
                cursor = conexao.cursor()
                comando = """
                    SELECT c.codcurso, c.descricao 
                    FROM turmas t
                    JOIN cursos c ON t.codcurso = c.codcurso
                    WHERE t.codturma = %s
                """
                cursor.execute(comando, (codturma,))
                resultado = cursor.fetchone()

                if resultado:
                    id_curso_encontrado = resultado[0]
                    encontrou = False
                    for texto_chave, id_real in self.mapeamento_cursos.items():
                        if id_real == id_curso_encontrado:
                            self.curso_selecionado_var.set(texto_chave)
                            encontrou = True
                            break
                    if not encontrou:
                        self.curso_selecionado_var.set(f"{resultado[0]} - {resultado[1]}")
                else:
                    self.limpar_campos(manter_turma=True)
                    messagebox.showinfo("Aviso", "Código livre. Pode registrar uma nova turma com este código.")
            except Exception as e:
                messagebox.showerror("Erro", str(e))
            finally:
                cursor.close()
                conexao.close()

    def confirmar(self):
        codturma = self.codturma_var.get().strip()
        opcao_curso = self.curso_selecionado_var.get()
        
        if not codturma:
            messagebox.showwarning("Aviso", "Preencha a letra ou código da Turma.")
            return
            
        if opcao_curso in ["Carregando...", "Nenhum curso cadastrado"]:
            messagebox.showerror("Ação Bloqueada", "Você precisa cadastrar um Curso na Tela de Cursos antes de criar uma Turma.")
            return

        cod_curso_real = self.mapeamento_cursos.get(opcao_curso)
        if not cod_curso_real:
            messagebox.showerror("Erro", "Curso selecionado não foi reconhecido pelo sistema de mapeamento.")
            return

        conexao = self.conectar_banco()
        if conexao:
            try:
                cursor = conexao.cursor()
                
                if self.acao_atual == "INSERIR":
                    comando = "INSERT INTO turmas (codturma, codcurso) VALUES (%s, %s)"
                    cursor.execute(comando, (codturma, cod_curso_real))
                    conexao.commit()
                    messagebox.showinfo("Sucesso", "Turma registrada e vinculada ao curso!")

                elif self.acao_atual == "ALTERAR":
                    comando = "UPDATE turmas SET codcurso = %s WHERE codturma = %s"
                    cursor.execute(comando, (cod_curso_real, codturma))
                    conexao.commit()
                    messagebox.showinfo("Sucesso", "Turma atualizada para o novo curso!")
                    
                elif self.acao_atual == "EXCLUIR":
                    comando = "DELETE FROM turmas WHERE codturma = %s"
                    cursor.execute(comando, (codturma,))
                    conexao.commit()
                    messagebox.showinfo("Sucesso", "Turma removida com sucesso!")
                
                self.limpar_e_resetar()
                self.atualizar_dados_reais()

            except mysql.connector.Error as erro:
                if erro.errno == 1451:
                    messagebox.showerror("Exclusão Bloqueada", "Não é possível excluir esta turma porque existem ALUNOS matriculados nela.\nRemova os alunos dessa turma primeiro.")
                else:
                    messagebox.showerror("Erro SQL", f"Erro no banco de dados:\n{erro}")
            finally:
                cursor.close()
                conexao.close()

    def mostrar_botoes(self):
        self.frame_botoes.pack_forget()
        self.frame_confirma.pack(fill="x")
        self.ent_codturma.configure(state="disabled")
        if self.acao_atual == "EXCLUIR":
            self.ent_curso.configure(state="disabled")

    def esconder_botoes(self):
        self.frame_confirma.pack_forget()
        self.frame_botoes.pack(fill="x")
        self.ent_codturma.configure(state="normal")
        self.ent_curso.configure(state="normal")

    def preparar_inserir(self):
        if not self.codturma_var.get():
            messagebox.showwarning("Campos Vazios", "Digite a letra da turma.")
            return
        self.acao_atual = "INSERIR"
        self.mostrar_botoes()

    def preparar_alterar(self):
        if not self.codturma_var.get():
            messagebox.showwarning("Campos Vazios", "Busque uma turma antes de alterar.")
            return
        self.acao_atual = "ALTERAR"
        self.mostrar_botoes()

    def preparar_excluir(self):
        if not self.codturma_var.get():
            messagebox.showwarning("Aviso", "Insira uma turma válida para exclusão.")
            return
        self.acao_atual = "EXCLUIR"
        self.mostrar_botoes()

    def cancelar(self):
        self.limpar_e_resetar()

    def limpar_campos(self, manter_turma=False):
        if not manter_turma: 
            self.codturma_var.set("")
        
        if hasattr(self, 'ent_curso'):
            valores = self.ent_curso.cget("values")
            if valores and valores[0] not in ["Carregando...", "Nenhum curso cadastrado"]:
                self.curso_selecionado_var.set(valores[0])

    def limpar_e_resetar(self):
        self.limpar_campos()
        self.esconder_botoes()
        self.acao_atual = None

if __name__ == "__main__":
    app = ctk.CTk()
    tela = TelaCadastroTurmas(app)
    app.mainloop()