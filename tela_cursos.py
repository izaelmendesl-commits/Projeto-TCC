import customtkinter as ctk
from tkinter import messagebox
import mysql.connector
import os
from PIL import Image

# --- CONFIGURAÇÃO INICIAL ---
ctk.set_appearance_mode("Light")  
ctk.set_default_color_theme("blue") 

# Transformando em Frame para caber no Main
class TelaCadastroCurso(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # --- PALETA DE CORES ADAPTATIVA ---
        self.cor_fundo_tech = ("#F4F7FA", "#0F172A")       
        self.cor_card_branco = ("#FFFFFF", "#1E293B")      
        self.cor_univap_azul = ("#0056B3", "#3B82F6")      
        self.cor_univap_escuro = ("#003366", "#60A5FA")    
        self.cor_borda = ("#E2E8F0", "#334155")            
        self.cor_texto_principal = ("#1E293B", "#F8FAFC")  
        self.cor_texto_secundario = ("#64748B", "#94A3B8") 
        self.cor_perigo = ("#EF4444", "#EF4444")           
        self.cor_sucesso = ("#10B981", "#10B981")          

        self.configure(fg_color=self.cor_fundo_tech)

        # Variáveis Reais do Sistema
        self.codigo_var = ctk.StringVar()
        self.descricao_var = ctk.StringVar()
        self.busca_tabela_var = ctk.StringVar() # Variável para o filtro de pesquisa
        self.acao_atual = None  

        self.criar_interface()
        self.atualizar_dados_reais() # Carrega os dados reais do banco de dados ao iniciar

    def mudar_tema(self, escolha):
        """Altera dinamicamente o tema do sistema"""
        if escolha == "Escuro":
            ctk.set_appearance_mode("Dark")
        else:
            ctk.set_appearance_mode("Light")

    def criar_interface(self):
        # --- TOP BAR (CABEÇALHO INTEGRADO) ---
        self.frame_header = ctk.CTkFrame(self, corner_radius=0, fg_color=self.cor_card_branco, 
                                         border_width=1, border_color=self.cor_borda)
        self.frame_header.pack(fill="x", pady=(0, 20))

        container_top = ctk.CTkFrame(self.frame_header, fg_color="transparent")
        container_top.pack(padx=30, pady=12, fill="x")

        # LOGO UNIVAP
        caminho_imagem = "logo_univap.png" 
        if os.path.exists(caminho_imagem):
            try:
                img_aberta = Image.open(caminho_imagem)
                imagem = ctk.CTkImage(light_image=img_aberta, dark_image=img_aberta, size=(55, 55))
                lbl_logo = ctk.CTkLabel(container_top, image=imagem, text="")
                lbl_logo.pack(side="left", padx=(0, 15))
            except Exception as erro:
                print(f"[AVISO IMAGEM]: Arquivo encontrado mas não pôde ser aberto: {erro}")

        # TÍTULO
        self.lbl_titulo = ctk.CTkLabel(container_top, text="Gerenciamento de Cursos", 
                                       font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"),
                                       text_color=self.cor_univap_escuro)
        self.lbl_titulo.pack(side="left", anchor="center")

        # SELETOR DE TEMA
        self.menu_tema = ctk.CTkOptionMenu(container_top, values=["Claro", "Escuro"], width=90, height=28,
                                           fg_color=self.cor_univap_azul, button_color=self.cor_univap_azul,
                                           button_hover_color=self.cor_univap_escuro, command=self.mudar_tema)
        self.menu_tema.pack(side="right", anchor="center", padx=(10, 0))
        self.menu_tema.set("Claro")

        self.lbl_tema_texto = ctk.CTkLabel(container_top, text="Tema:", font=ctk.CTkFont(size=12, weight="bold"), text_color=self.cor_texto_principal)
        self.lbl_tema_texto.pack(side="right", anchor="center")

        # =========================================================================
        # --- CORPO DA TELA DIVIDIDO PROPORCIONALMENTE (EVITA DISTORÇÃO) ---
        # =========================================================================
        body_container = ctk.CTkFrame(self, fg_color="transparent")
        body_container.pack(fill="both", expand=True, padx=30, pady=(0, 20))
        
        # Configuração das Colunas: Coluna 0 fixa para o formulário, Coluna 1 expande com a tabela
        body_container.grid_columnconfigure(0, weight=0) 
        body_container.grid_columnconfigure(1, weight=1) 
        body_container.grid_rowconfigure(0, weight=1)

        # -------------------------------------------------------------------------
        # PAINEL ESQUERDO: ÁREA DE CADASTRO (FICA INTACTO E COMPACTO AO MAXIMIZAR)
        # -------------------------------------------------------------------------
        left_panel = ctk.CTkFrame(body_container, fg_color="transparent", width=400)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
        
        self.frame_form = ctk.CTkFrame(left_panel, corner_radius=12, fg_color=self.cor_card_branco,
                                       border_width=1, border_color=self.cor_borda)
        self.frame_form.pack(fill="both", expand=True)

        self.lbl_instrucao = ctk.CTkLabel(self.frame_form, text="ÁREA DE CADASTRO", 
                                          font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"), 
                                          text_color=self.cor_univap_azul)
        self.lbl_instrucao.grid(row=0, column=0, columnspan=3, pady=(25, 15), padx=25, sticky="w")

        # Campo: Código do Curso
        self.lbl_codigo = ctk.CTkLabel(self.frame_form, text="Código do Curso", font=ctk.CTkFont(size=13, weight="bold"), text_color=self.cor_texto_principal)
        self.lbl_codigo.grid(row=1, column=0, sticky="w", pady=5, padx=25)
        
        # Bloco de Código + Botão Buscar lado a lado
        search_block = ctk.CTkFrame(self.frame_form, fg_color="transparent")
        search_block.grid(row=2, column=0, columnspan=3, sticky="w", padx=25, pady=(0, 15))
        
        self.ent_codigo = ctk.CTkEntry(search_block, textvariable=self.codigo_var, width=140, height=38, corner_radius=6)
        self.ent_codigo.pack(side="left", padx=(0, 10))
        
        self.btn_buscar = ctk.CTkButton(search_block, text="🔍 Buscar", width=110, height=38, corner_radius=6, 
                                        fg_color=self.cor_univap_azul, hover_color=self.cor_univap_escuro, command=self.buscar_curso)
        self.btn_buscar.pack(side="left")

        # Campo: Descrição
        self.lbl_descricao = ctk.CTkLabel(self.frame_form, text="Descrição do Curso", font=ctk.CTkFont(size=13, weight="bold"), text_color=self.cor_texto_principal)
        self.lbl_descricao.grid(row=3, column=0, sticky="w", pady=5, padx=25)
        
        self.ent_descricao = ctk.CTkEntry(self.frame_form, textvariable=self.descricao_var, width=340, height=38, corner_radius=6)
        self.ent_descricao.grid(row=4, column=0, columnspan=3, sticky="w", pady=(0, 25), padx=25)

        # --- CONTAINER DE BOTÕES DE AÇÃO (FIXADOS ABAIXO DO FORMULÁRIO) ---
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

        # CONTAINER DE CONFIRMAÇÃO (OCULTO INICIALMENTE)
        self.frame_confirma = ctk.CTkFrame(self.container_botoes_acoes, fg_color="transparent")
        
        self.btn_confirmar = ctk.CTkButton(self.frame_confirma, text="✔️ Confirmar Operação", fg_color=self.cor_sucesso, height=42, font=ctk.CTkFont(weight="bold"), command=self.confirmar)
        self.btn_confirmar.pack(side="left", expand=True, fill="x", padx=(0, 5))

        self.btn_cancelar = ctk.CTkButton(self.frame_confirma, text="❌ Cancelar", height=42, fg_color="transparent", border_width=1, border_color=self.cor_perigo, text_color=self.cor_perigo, command=self.cancelar)
        self.btn_cancelar.pack(side="left", expand=True, fill="x", padx=(5, 0))

        # -------------------------------------------------------------------------
        # PAINEL DIREITO: CONSULTA REAL EM TEMPO REAL (OCUPA O ESPAÇO EXPANDIDO)
        # -------------------------------------------------------------------------
        right_panel = ctk.CTkFrame(body_container, fg_color="transparent")
        right_panel.grid(row=0, column=1, sticky="nsew")
        
        right_panel.grid_rowconfigure(0, weight=0) # Contador de cursos superior
        right_panel.grid_rowconfigure(1, weight=1) # Tabela real inferior
        right_panel.grid_columnconfigure(0, weight=1)

        # Indicador Real Superior (Totalizador de linhas do banco)
        card_total = ctk.CTkFrame(right_panel, fg_color=self.cor_card_branco, border_width=1, border_color=self.cor_borda, height=65, corner_radius=8)
        card_total.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        card_total.pack_propagate(False)
        
        ctk.CTkLabel(card_total, text="Total de Cursos Cadastrados no Banco:", font=ctk.CTkFont(size=12, weight="bold"), text_color=self.cor_texto_secundario).pack(side="left", padx=20)
        self.lbl_metric_total = ctk.CTkLabel(card_total, text="0", font=ctk.CTkFont(size=22, weight="bold"), text_color=self.cor_univap_azul)
        self.lbl_metric_total.pack(side="right", padx=20)

        # Card de Fundo da Tabela Geral
        table_card = ctk.CTkFrame(right_panel, corner_radius=12, fg_color=self.cor_card_branco, border_width=1, border_color=self.cor_borda)
        table_card.grid(row=1, column=0, sticky="nsew")
        
        # Cabeçalho interno da tabela com Barra de Pesquisa Integrada
        table_header = ctk.CTkFrame(table_card, fg_color="transparent")
        table_header.pack(fill="x", padx=20, pady=12)
        
        ctk.CTkLabel(table_header, text="Lista Oficial de Cursos (Banco de Dados)", font=ctk.CTkFont(size=13, weight="bold"), text_color=self.cor_texto_principal).pack(side="left")
        
        self.ent_pesquisa = ctk.CTkEntry(table_header, textvariable=self.busca_tabela_var, placeholder_text="Filtrar dados da tabela...", width=200, height=30)
        self.ent_pesquisa.pack(side="right", padx=5)
        # Evento que atualiza a listagem a cada letra digitada pelo usuário
        self.ent_pesquisa.bind("<KeyRelease>", lambda e: self.atualizar_dados_reais())

        # Janela de rolagem (Scrollable Frame) para listar os registros dinamicamente
        self.scroll_table = ctk.CTkScrollableFrame(table_card, fg_color=self.cor_fundo_tech, corner_radius=6)
        self.scroll_table.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def atualizar_dados_reais(self):
        """Busca as informações oficiais do MySQL e reconstrói as linhas da tabela"""
        # Limpa todos os widgets antigos de dentro da tabela rolável
        for widget in self.scroll_table.winfo_children():
            widget.destroy()

        # Cria a barra estática de títulos da coluna
        h_frame = ctk.CTkFrame(self.scroll_table, fg_color="transparent")
        h_frame.pack(fill="x", pady=2)
        ctk.CTkLabel(h_frame, text="CÓDIGO", font=ctk.CTkFont(size=11, weight="bold"), width=90, anchor="w", text_color=self.cor_texto_secundario).pack(side="left", padx=10)
        ctk.CTkLabel(h_frame, text="DESCRIÇÃO DO CURSO", font=ctk.CTkFont(size=11, weight="bold"), anchor="w", text_color=self.cor_texto_secundario).pack(side="left", padx=10, fill="x", expand=True)

        conexao = self.conectar_banco()
        if conexao:
            try:
                cursor = conexao.cursor()
                
                # 1. Conta quantos registros existem de verdade
                cursor.execute("SELECT COUNT(*) FROM cursos")
                total_linhas = cursor.fetchone()[0]
                self.lbl_metric_total.configure(text=str(total_linhas))
                
                # 2. Executa a listagem com base no filtro digitado
                filtro = self.busca_tabela_var.get().strip()
                if filtro:
                    comando = "SELECT codcurso, descricao FROM cursos WHERE codcurso LIKE %s OR descricao LIKE %s ORDER BY codcurso"
                    cursor.execute(comando, (f"%{filtro}%", f"%{filtro}%"))
                else:
                    cursor.execute("SELECT codcurso, descricao FROM cursos ORDER BY codcurso")
                    
                registros = cursor.fetchall()
                
                # 3. Desenha os cards reais das linhas na tela
                for cod, desc in registros:
                    row = ctk.CTkFrame(self.scroll_table, height=38, fg_color=self.cor_card_branco, corner_radius=6, border_width=1, border_color=self.cor_borda)
                    row.pack(fill="x", pady=3, padx=2)
                    row.pack_propagate(False)
                    
                    ctk.CTkLabel(row, text=str(cod), font=ctk.CTkFont(size=12, weight="bold"), width=90, anchor="w", text_color=self.cor_univap_azul).pack(side="left", padx=10)
                    ctk.CTkLabel(row, text=str(desc), font=ctk.CTkFont(size=12), anchor="w", text_color=self.cor_texto_principal).pack(side="left", padx=10, fill="x", expand=True)
                    
            except mysql.connector.Error as erro:
                print(f"[ERRO AO CARREGAR TABELA]: {erro}")
            finally:
                cursor.close()
                conexao.close()

    # =========================================================================
    # --- INTEGRAÇÃO COM O BANCO DE DADOS ---
    # =========================================================================

    def conectar_banco(self):
        try:
            conexao = mysql.connector.connect(
                host="localhost",
                user="root",
                password="IzaelMendes123",
                database="avisos_sistema"
            )
            return conexao
        except mysql.connector.Error as erro:
            messagebox.showerror("Erro de Conexão", f"Não foi possível conectar:\n{erro}")
            return None

    def buscar_curso(self):
        codigo = self.codigo_var.get()
        if not codigo:
            messagebox.showwarning("Aviso", "Digite um Código para buscar.")
            return

        conexao = self.conectar_banco()
        if conexao:
            try:
                cursor = conexao.cursor()
                comando = "SELECT descricao FROM cursos WHERE codcurso = %s"
                cursor.execute(comando, (codigo,))
                resultado = cursor.fetchone()

                if resultado:
                    self.descricao_var.set(resultado[0])
                    self.ent_descricao.configure(border_color=self.cor_sucesso) 
                    # Corrigido o after para funcionar no novo frame
                    self.after(1500, lambda: self.ent_descricao.configure(border_color=self.cor_borda))
                else:
                    self.descricao_var.set("")
                    messagebox.showinfo("Aviso", f"O curso {codigo} não existe. Você pode preencher e inserir.")
            except mysql.connector.Error as erro:
                messagebox.showerror("Erro de SQL", f"Erro ao buscar:\n{erro}")
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
                
                if self.acao_atual == "INSERIR":
                    comando = "INSERT INTO cursos (codcurso, descricao) VALUES (%s, %s)"
                    cursor.execute(comando, (codigo, descricao))
                    conexao.commit()
                    messagebox.showinfo("Sucesso", "Curso cadastrado com sucesso!")

                elif self.acao_atual == "ALTERAR":
                    comando = "UPDATE cursos SET descricao = %s WHERE codcurso = %s"
                    cursor.execute(comando, (descricao, codigo))
                    conexao.commit()
                    messagebox.showinfo("Sucesso", "Curso alterado com sucesso!")
                    
                elif self.acao_atual == "EXCLUIR":
                    comando = "DELETE FROM cursos WHERE codcurso = %s"
                    cursor.execute(comando, (codigo,))
                    conexao.commit()
                    messagebox.showinfo("Sucesso", "Curso excluído!")
                
                self.limpar_e_resetar()
                self.atualizar_dados_reais() # Atualiza instantaneamente a listagem e o contador

            except mysql.connector.Error as erro:
                # Tratamento específico para o erro de chave estrangeira (1451) adicionado aqui
                if erro.errno == 1451:
                    messagebox.showwarning("Ação Bloqueada", "Não é possível excluir este curso, pois existem turmas vinculadas a ele.")
                else:
                    messagebox.showerror("Erro de SQL", f"Erro no banco:\n{erro}")
            finally:
                cursor.close()
                conexao.close()

    # =========================================================================
    # --- CONTROLE DE INTERFACE ---
    # =========================================================================

    def mostrar_botoes(self):
        self.frame_botoes.pack_forget()
        self.frame_confirma.pack(fill="x")
        if self.acao_atual == "EXCLUIR":
            self.ent_descricao.configure(state="disabled")
        self.ent_codigo.configure(state="disabled")

    def esconder_botoes(self):
        self.frame_confirma.pack_forget()
        self.frame_botoes.pack(fill="x")
        self.ent_codigo.configure(state="normal")
        self.ent_descricao.configure(state="normal")

    def prevenir_vazio(self):
        return not self.codigo_var.get() or not self.descricao_var.get()

    def preparar_inserir(self):
        if self.prevenir_vazio():
            messagebox.showwarning("Aviso", "Preencha os campos para inserir.")
            return
        self.acao_atual = "INSERIR"
        self.mostrar_botoes()

    def preparar_alterar(self):
        if self.prevenir_vazio():
            messagebox.showwarning("Aviso", "Busque e altere os dados primeiro.")
            return
        self.acao_atual = "ALTERAR"
        self.mostrar_botoes()

    def preparar_excluir(self):
        if not self.codigo_var.get():
            messagebox.showwarning("Aviso", "Insira o código do curso que deseja excluir.")
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

# Inicialização apenas para teste isolado
if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("1050x600")
    app.title("Teste - Tela de Cursos")
    
    # Injeta a tela na janela de teste
    tela = TelaCadastroCurso(app)
    tela.pack(fill="both", expand=True)
    
    app.mainloop()