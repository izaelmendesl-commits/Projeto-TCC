import customtkinter as ctk
from tkinter import messagebox, filedialog
import mysql.connector
import os
import pandas as pd
from PIL import Image

# --- CONFIGURAÇÃO INICIAL DE INTERFACE ---
ctk.set_appearance_mode("Light")  
ctk.set_default_color_theme("blue") 

# A classe agora herda de CTkFrame para se encaixar no main.py
class TelaCadastroAlunos(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # --- PALETA DE CORES ---
        self.cor_fundo_tech = ("#F4F7FA", "#0F172A")       
        self.cor_card_branco = ("#FFFFFF", "#1E293B")      
        self.cor_univap_azul = ("#0056B3", "#3B82F6")      
        self.cor_univap_escuro = ("#003366", "#60A5FA")    
        self.cor_borda = ("#E2E8F0", "#334155")            
        self.cor_texto_principal = ("#1E293B", "#F8FAFC")  
        self.cor_texto_secundario = ("#64748B", "#94A3B8") 
        self.cor_perigo = ("#EF4444", "#EF4444")           
        self.cor_sucesso = ("#10B981", "#10B981")          

        # Configura a cor de fundo do próprio Frame
        self.configure(fg_color=self.cor_fundo_tech)

        # Variáveis
        self.matricula_var = ctk.StringVar()
        self.cpf_var = ctk.StringVar()
        self.nome_completo_var = ctk.StringVar()
        self.codturma_var = ctk.StringVar()
        self.email_var = ctk.StringVar()
        
        self.busca_tabela_var = ctk.StringVar() 
        self.acao_atual = None  

        self.criar_interface()
        
        if self.testar_conexao_inicial():
            self.carregar_turmas_do_banco() 
            self.atualizar_dados_reais() 

    def mudar_tema(self, escolha):
        ctk.set_appearance_mode("Dark" if escolha == "Escuro" else "Light")

    def testar_conexao_inicial(self):
        conexao = self.conectar_banco(silencioso=True)
        if conexao:
            conexao.close()
            return True
        else:
            messagebox.showerror("Erro Crítico", "Falha de conexão com o Banco de Dados.")
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

    def carregar_turmas_do_banco(self):
        conexao = self.conectar_banco(silencioso=True)
        if conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute("SELECT codturma FROM turmas ORDER BY codturma")
                turmas = cursor.fetchall()
                
                lista_turmas = [str(t[0]) for t in turmas]
                
                if lista_turmas:
                    self.ent_turma.configure(values=lista_turmas)
                    self.codturma_var.set(lista_turmas[0]) 
                else:
                    self.ent_turma.configure(values=["Sem Turmas"])
                    self.codturma_var.set("Sem Turmas")
                    
            except Exception as erro:
                print(f"Erro ao carregar turmas: {erro}")
            finally:
                cursor.close()
                conexao.close()

    def criar_interface(self):
        # Usamos 'self' em vez de 'self.master' para que os elementos fiquem dentro do Frame
        self.frame_header = ctk.CTkFrame(self, corner_radius=0, fg_color=self.cor_card_branco, border_width=1, border_color=self.cor_borda)
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

        self.lbl_titulo = ctk.CTkLabel(container_top, text="Gerenciamento de Alunos", font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"), text_color=self.cor_univap_escuro)
        self.lbl_titulo.pack(side="left", anchor="center")

        self.menu_tema = ctk.CTkOptionMenu(container_top, values=["Claro", "Escuro"], width=90, height=28, fg_color=self.cor_univap_azul, button_color=self.cor_univap_azul, button_hover_color=self.cor_univap_escuro, command=self.mudar_tema)
        self.menu_tema.pack(side="right", anchor="center", padx=(10, 0))
        self.menu_tema.set("Claro")

        self.lbl_tema_texto = ctk.CTkLabel(container_top, text="Tema:", font=ctk.CTkFont(size=12, weight="bold"), text_color=self.cor_texto_principal)
        self.lbl_tema_texto.pack(side="right", anchor="center")

        body_container = ctk.CTkFrame(self, fg_color="transparent")
        body_container.pack(fill="both", expand=True, padx=30, pady=(0, 20))
        
        body_container.grid_columnconfigure(0, weight=0) 
        body_container.grid_columnconfigure(1, weight=1) 
        body_container.grid_rowconfigure(0, weight=1)

        left_panel = ctk.CTkFrame(body_container, fg_color="transparent", width=400)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
        
        self.frame_form = ctk.CTkFrame(left_panel, corner_radius=12, fg_color=self.cor_card_branco, border_width=1, border_color=self.cor_borda)
        self.frame_form.pack(fill="both", expand=True)

        self.lbl_instrucao = ctk.CTkLabel(self.frame_form, text="ÁREA DE CADASTRO", font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"), text_color=self.cor_univap_azul)
        self.lbl_instrucao.grid(row=0, column=0, columnspan=2, pady=(25, 15), padx=25, sticky="w")

        self.lbl_matricula = ctk.CTkLabel(self.frame_form, text="Matrícula", font=ctk.CTkFont(size=13, weight="bold"), text_color=self.cor_texto_principal)
        self.lbl_matricula.grid(row=1, column=0, sticky="w", pady=(5, 2), padx=25)
        
        search_block = ctk.CTkFrame(self.frame_form, fg_color="transparent")
        search_block.grid(row=2, column=0, columnspan=2, sticky="w", padx=25, pady=(0, 12))
        
        self.ent_matricula = ctk.CTkEntry(search_block, textvariable=self.matricula_var, width=140, height=36, corner_radius=6)
        self.ent_matricula.pack(side="left", padx=(0, 10))
        
        self.btn_buscar = ctk.CTkButton(search_block, text="🔍 Buscar", width=110, height=36, corner_radius=6, fg_color=self.cor_univap_azul, hover_color=self.cor_univap_escuro, command=self.buscar_aluno)
        self.btn_buscar.pack(side="left")

        self.lbl_nome = ctk.CTkLabel(self.frame_form, text="Nome Completo", font=ctk.CTkFont(size=13, weight="bold"), text_color=self.cor_texto_principal)
        self.lbl_nome.grid(row=3, column=0, sticky="w", pady=(5, 2), padx=25)
        
        self.ent_nome = ctk.CTkEntry(self.frame_form, textvariable=self.nome_completo_var, width=340, height=36, corner_radius=6)
        self.ent_nome.grid(row=4, column=0, columnspan=2, sticky="w", pady=(0, 12), padx=25)

        self.lbl_cpf = ctk.CTkLabel(self.frame_form, text="CPF", font=ctk.CTkFont(size=13, weight="bold"), text_color=self.cor_texto_principal)
        self.lbl_cpf.grid(row=5, column=0, sticky="w", pady=(5, 2), padx=25)
        
        self.lbl_turma = ctk.CTkLabel(self.frame_form, text="Turma do Aluno", font=ctk.CTkFont(size=13, weight="bold"), text_color=self.cor_texto_principal)
        self.lbl_turma.grid(row=5, column=1, sticky="w", pady=(5, 2), padx=5)

        self.ent_cpf = ctk.CTkEntry(self.frame_form, textvariable=self.cpf_var, width=165, height=36, corner_radius=6)
        self.ent_cpf.grid(row=6, column=0, sticky="w", pady=(0, 12), padx=25)

        self.ent_turma = ctk.CTkOptionMenu(self.frame_form, variable=self.codturma_var, values=["Carregando..."], width=165, height=36, corner_radius=6, fg_color=self.cor_fundo_tech, button_color=self.cor_borda, button_hover_color=self.cor_texto_secundario, text_color=self.cor_texto_principal)
        self.ent_turma.grid(row=6, column=1, sticky="w", pady=(0, 12), padx=5)

        self.lbl_email = ctk.CTkLabel(self.frame_form, text="E-mail", font=ctk.CTkFont(size=13, weight="bold"), text_color=self.cor_texto_principal)
        self.lbl_email.grid(row=7, column=0, sticky="w", pady=(5, 2), padx=25)
        
        self.ent_email = ctk.CTkEntry(self.frame_form, textvariable=self.email_var, width=340, height=36, corner_radius=6)
        self.ent_email.grid(row=8, column=0, columnspan=2, sticky="w", pady=(0, 25), padx=25)

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

        self.frame_confirma = ctk.CTkFrame(self.container_botoes_acoes, fg_color="transparent")
        self.btn_confirmar = ctk.CTkButton(self.frame_confirma, text="✔️ Confirmar Operação", fg_color=self.cor_sucesso, height=42, font=ctk.CTkFont(weight="bold"), command=self.confirmar)
        self.btn_confirmar.pack(side="left", expand=True, fill="x", padx=(0, 5))
        self.btn_cancelar = ctk.CTkButton(self.frame_confirma, text="❌ Cancelar", height=42, fg_color="transparent", border_width=1, border_color=self.cor_perigo, text_color=self.cor_perigo, command=self.cancelar)
        self.btn_cancelar.pack(side="left", expand=True, fill="x", padx=(5, 0))

        right_panel = ctk.CTkFrame(body_container, fg_color="transparent")
        right_panel.grid(row=0, column=1, sticky="nsew")
        right_panel.grid_rowconfigure(0, weight=0) 
        right_panel.grid_rowconfigure(1, weight=1) 
        right_panel.grid_columnconfigure(0, weight=1)

        card_total = ctk.CTkFrame(right_panel, fg_color=self.cor_card_branco, border_width=1, border_color=self.cor_borda, height=65, corner_radius=8)
        card_total.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        card_total.pack_propagate(False)
        
        ctk.CTkLabel(card_total, text="Total de Alunos Matriculados:", font=ctk.CTkFont(size=12, weight="bold"), text_color=self.cor_texto_secundario).pack(side="left", padx=20)
        self.lbl_metric_total = ctk.CTkLabel(card_total, text="0", font=ctk.CTkFont(size=22, weight="bold"), text_color=self.cor_univap_azul)
        self.lbl_metric_total.pack(side="right", padx=20)

        table_card = ctk.CTkFrame(right_panel, corner_radius=12, fg_color=self.cor_card_branco, border_width=1, border_color=self.cor_borda)
        table_card.grid(row=1, column=0, sticky="nsew")
        
        table_header = ctk.CTkFrame(table_card, fg_color="transparent")
        table_header.pack(fill="x", padx=20, pady=12)
        
        ctk.CTkLabel(table_header, text="Lista Oficial de Alunos", font=ctk.CTkFont(size=13, weight="bold"), text_color=self.cor_texto_principal).pack(side="left")
        
        self.ent_pesquisa = ctk.CTkEntry(table_header, textvariable=self.busca_tabela_var, placeholder_text="Buscar...", width=200, height=30)
        self.ent_pesquisa.pack(side="right", padx=(5, 0))
        self.ent_pesquisa.bind("<KeyRelease>", lambda e: self.atualizar_dados_reais())

        self.btn_importar = ctk.CTkButton(table_header, text="Importar Excel", width=140, height=30, fg_color=self.cor_sucesso, font=ctk.CTkFont(weight="bold"), command=self.importar_alunos_excel)
        self.btn_importar.pack(side="right", padx=5)

        self.scroll_table = ctk.CTkScrollableFrame(table_card, fg_color=self.cor_fundo_tech, corner_radius=6)
        self.scroll_table.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def importar_alunos_excel(self):
        caminho_arquivo = filedialog.askopenfilename(
            title="Selecionar Planilha de Alunos",
            filetypes=[("Arquivos Excel", "*.xlsx *.xls")]
        )
        
        if not caminho_arquivo:
            return

        conexao = None
        cursor = None

        try:
            df = pd.read_excel(caminho_arquivo)
            colunas_obrigatorias = ['Matrícula', 'Nome Completo', 'CPF', 'Cód. Turma', 'E-mail']
            
            if not all(col in df.columns for col in colunas_obrigatorias):
                messagebox.showerror(
                    "Erro de Estrutura", 
                    f"A planilha precisa conter exatamente as colunas:\n{', '.join(colunas_obrigatorias)}"
                )
                return

            conexao = self.conectar_banco(silencioso=True)
            if not conexao:
                messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados.")
                return
                
            cursor = conexao.cursor()
            linhas_inseridas = 0
            erros = []

            for index, linha in df.iterrows():
                num_linha_excel = index + 2 
                
                try:
                    if pd.isna(linha['Matrícula']) or str(linha['Nome Completo']).strip().lower() == "nan":
                        continue

                    # Conversão segura para limpar dados do Excel
                    # Transforma em string, remove espaços e depois converte para evitar erros com floats/strings misturados
                    matricula_str = str(linha['Matrícula']).strip().replace('.0', '')
                    turma_str = str(linha['Cód. Turma']).strip().replace('.0', '')
                    
                    matricula = int(matricula_str)
                    codturma = int(turma_str)
                    
                    nome_completo = str(linha['Nome Completo']).strip()
                    cpf = str(linha['CPF']).strip() if not pd.isna(linha['CPF']) else ""
                    email = str(linha['E-mail']).strip() if not pd.isna(linha['E-mail']) else ""

                    sql = """
                        INSERT INTO alunos (matricula, cpf, nome_completo, codturma, email) 
                        VALUES (%s, %s, %s, %s, %s)
                    """
                    valores = (matricula, cpf, nome_completo, codturma, email)
                    cursor.execute(sql, valores)
                    linhas_inseridas += 1

                except mysql.connector.Error as mysql_err:
                    if mysql_err.errno == 1452:
                        erros.append(f"Linha {num_linha_excel}: Código de turma '{codturma}' não existe.")
                    elif mysql_err.errno == 1062:
                        erros.append(f"Linha {num_linha_excel}: Matrícula '{matricula}' ou CPF já cadastrados.")
                    else:
                        erros.append(f"Linha {num_linha_excel}: Erro {mysql_err.errno} - {mysql_err.msg}")
                        
                except ValueError:
                    erros.append(f"Linha {num_linha_excel}: As colunas 'Matrícula' e 'Cód. Turma' não podem conter texto, apenas números.")
                except Exception as e:
                    erros.append(f"Linha {num_linha_excel}: Falha: {str(e)}")

            if linhas_inseridas > 0:
                conexao.commit()

            self.atualizar_dados_reais()

            if erros:
                resumo_erros = "\n".join(erros[:10])
                if len(erros) > 10:
                    resumo_erros += f"\n... e mais {len(erros) - 10} erro(s)."
                messagebox.showwarning(
                    "Importação Concluída com Alertas",
                    f"Sucesso: {linhas_inseridas} aluno(s) inserido(s).\n\nProblemas encontrados:\n{resumo_erros}"
                )
            else:
                messagebox.showinfo("Sucesso", f"Todos os {linhas_inseridas} alunos foram cadastrados com sucesso!")

        except Exception as general_err:
            messagebox.showerror("Erro Geral", f"Não foi possível processar o arquivo:\n{general_err}")
        finally:
            if cursor:
                cursor.close()
            if conexao and conexao.is_connected():
                conexao.close()

    def atualizar_dados_reais(self):
        for widget in self.scroll_table.winfo_children():
            widget.destroy()

        h_frame = ctk.CTkFrame(self.scroll_table, fg_color="transparent")
        h_frame.pack(fill="x", pady=2)
        ctk.CTkLabel(h_frame, text="MATRÍCULA", font=ctk.CTkFont(size=11, weight="bold"), width=95, anchor="w", text_color=self.cor_texto_secundario).pack(side="left", padx=10)
        ctk.CTkLabel(h_frame, text="NOME COMPLETO", font=ctk.CTkFont(size=11, weight="bold"), anchor="w", text_color=self.cor_texto_secundario).pack(side="left", padx=10, fill="x", expand=True)
        ctk.CTkLabel(h_frame, text="TURMA", font=ctk.CTkFont(size=11, weight="bold"), width=70, anchor="w", text_color=self.cor_texto_secundario).pack(side="right", padx=10)

        conexao = self.conectar_banco(silencioso=True)
        if conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute("SELECT COUNT(*) FROM alunos")
                self.lbl_metric_total.configure(text=str(cursor.fetchone()[0]))
                
                filtro = self.busca_tabela_var.get().strip()
                if filtro:
                    comando = "SELECT matricula, nome_completo, codturma FROM alunos WHERE matricula LIKE %s OR nome_completo LIKE %s ORDER BY nome_completo"
                    cursor.execute(comando, (f"%{filtro}%", f"%{filtro}%"))
                else:
                    comando = "SELECT matricula, nome_completo, codturma FROM alunos ORDER BY nome_completo"
                    cursor.execute(comando)
                    
                for mat, nome, turma in cursor.fetchall():
                    row = ctk.CTkFrame(self.scroll_table, height=38, fg_color=self.cor_card_branco, corner_radius=6, border_width=1, border_color=self.cor_borda)
                    row.pack(fill="x", pady=3, padx=2)
                    row.pack_propagate(False)
                    
                    ctk.CTkLabel(row, text=str(mat), font=ctk.CTkFont(size=12, weight="bold"), width=95, anchor="w", text_color=self.cor_univap_azul).pack(side="left", padx=10)
                    ctk.CTkLabel(row, text=str(nome), font=ctk.CTkFont(size=12), anchor="w", text_color=self.cor_texto_principal).pack(side="left", padx=10, fill="x", expand=True)
                    ctk.CTkLabel(row, text=str(turma), font=ctk.CTkFont(size=12, weight="bold"), width=70, anchor="center", text_color=self.cor_texto_principal).pack(side="right", padx=10)
            except Exception as e:
                print(e)
            finally:
                cursor.close()
                conexao.close()

    def buscar_aluno(self):
        matricula = self.matricula_var.get().strip()
        if not matricula:
            messagebox.showwarning("Aviso", "Digite uma Matrícula para buscar.")
            return

        conexao = self.conectar_banco()
        if conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute("SELECT cpf, nome_completo, codturma, email FROM alunos WHERE matricula = %s", (matricula,))
                resultado = cursor.fetchone()

                if resultado:
                    self.cpf_var.set(resultado[0])
                    self.nome_completo_var.set(resultado[1])
                    self.codturma_var.set(str(resultado[2]))
                    self.email_var.set(resultado[3])
                else:
                    self.limpar_campos(manter_matricula=True)
                    messagebox.showinfo("Aviso", "Matrícula disponível para novo cadastro.")
            except Exception as e:
                messagebox.showerror("Erro", str(e))
            finally:
                cursor.close()
                conexao.close()

    def confirmar(self):
        mat = self.matricula_var.get().strip()
        cpf = self.cpf_var.get().strip()
        nome = self.nome_completo_var.get().strip()
        turma = self.codturma_var.get().strip()
        email = self.email_var.get().strip()
        
        if turma == "Sem Turmas":
            messagebox.showerror("Ação Bloqueada", "Você não pode cadastrar um aluno sem turma. Cadastre uma turma no sistema primeiro.")
            return

        conexao = self.conectar_banco()
        if conexao:
            try:
                cursor = conexao.cursor()
                
                if self.acao_atual == "INSERIR":
                    comando = "INSERT INTO alunos (matricula, cpf, nome_completo, codturma, email) VALUES (%s, %s, %s, %s, %s)"
                    cursor.execute(comando, (mat, cpf, nome, turma, email))
                    conexao.commit()
                    messagebox.showinfo("Sucesso", "Aluno cadastrado!")

                elif self.acao_atual == "ALTERAR":
                    comando = "UPDATE alunos SET cpf = %s, nome_completo = %s, codturma = %s, email = %s WHERE matricula = %s"
                    cursor.execute(comando, (cpf, nome, turma, email, mat))
                    conexao.commit()
                    messagebox.showinfo("Sucesso", "Cadastro atualizado!")
                    
                elif self.acao_atual == "EXCLUIR":
                    comando = "DELETE FROM alunos WHERE matricula = %s"
                    cursor.execute(comando, (mat,))
                    conexao.commit()
                    messagebox.showinfo("Sucesso", "Aluno removido!")
                
                self.limpar_e_resetar()
                self.atualizar_dados_reais()

            except mysql.connector.Error as erro:
                messagebox.showerror("Erro SQL", f"Detalhes do erro:\n{erro}")
            finally:
                cursor.close()
                conexao.close()

    def mostrar_botoes(self):
        self.frame_botoes.pack_forget()
        self.frame_confirma.pack(fill="x")
        self.ent_matricula.configure(state="disabled")
        if self.acao_atual == "EXCLUIR":
            for e in [self.ent_nome, self.ent_cpf, self.ent_turma, self.ent_email]: e.configure(state="disabled")

    def esconder_botoes(self):
        self.frame_confirma.pack_forget()
        self.frame_botoes.pack(fill="x")
        for e in [self.ent_matricula, self.ent_nome, self.ent_cpf, self.ent_turma, self.ent_email]: e.configure(state="normal")

    def verificar_campos_vazios(self):
        return not self.matricula_var.get() or not self.nome_completo_var.get()

    def preparar_inserir(self):
        if self.verificar_campos_vazios():
            messagebox.showwarning("Campos Vazios", "Matrícula e Nome Completo são obrigatórios.")
            return
        self.acao_atual = "INSERIR"
        self.mostrar_botoes()

    def preparar_alterar(self):
        if self.verificar_campos_vazios():
            messagebox.showwarning("Campos Vazios", "Busque um aluno e preencha os campos antes de alterar.")
            return
        self.acao_atual = "ALTERAR"
        self.mostrar_botoes()

    def preparar_excluir(self):
        if not self.matricula_var.get():
            messagebox.showwarning("Aviso", "Insira uma matrícula válida para exclusão.")
            return
        self.acao_atual = "EXCLUIR"
        self.mostrar_botoes()

    def cancelar(self):
        self.limpar_e_resetar()

    def limpar_campos(self, manter_matricula=False):
        if not manter_matricula: self.matricula_var.set("")
        self.cpf_var.set("")
        self.nome_completo_var.set("")
        self.email_var.set("")
        
        if hasattr(self, 'ent_turma'):
            valores = self.ent_turma.cget("values")
            if valores and valores[0] != "Carregando...":
                self.codturma_var.set(valores[0])

    def limpar_e_resetar(self):
        self.limpar_campos()
        self.esconder_botoes()
        self.acao_atual = None

# O bloco abaixo foi adaptado para você ainda conseguir testar este arquivo isoladamente
if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("1100x650")
    app.title("Teste - Tela de Alunos")
    
    # Agora a tela é instanciada e em seguida "empacotada" na janela de teste
    tela = TelaCadastroAlunos(app)
    tela.pack(fill="both", expand=True)
    
    app.mainloop()