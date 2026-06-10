import customtkinter as ctk
from tkinter import messagebox, filedialog
import mysql.connector
import os
import pandas as pd
from PIL import Image

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")


class TelaCadastroAlunos(ctk.CTkFrame):
    # ─────────────────────────────────────────────
    #  PALETA DE CORES CENTRALIZADA
    # ─────────────────────────────────────────────
    COR = {
        "fundo":         ("#F0F4F8", "#0D1B2A"),
        "card":          ("#FFFFFF", "#152032"),
        "azul":          ("#0056B3", "#3B82F6"),
        "azul_esc":      ("#003D7A", "#1D4ED8"),
        "azul_hover":    ("#004A9A", "#2563EB"),
        "borda":         ("#D1DCF0", "#1E3A5F"),
        "titulo":        ("#002B5C", "#93C5FD"),
        "texto":         ("#1E3A5F", "#E2EAF8"),
        "suave":         ("#5A7A9F", "#6B9ED2"),
        "sucesso":       ("#059669", "#10B981"),
        "sucesso_hov":   ("#047857", "#059669"),
        "perigo":        ("#DC2626", "#EF4444"),
        "perigo_hov":    ("#B91C1C", "#DC2626"),
        "perigo_bg":     ("#FEF2F2", "#2D0A0A"),
        "linha_a":       ("#F5F8FF", "#111D2E"),
        "linha_b":       ("#FFFFFF", "#152032"),
        "tag_azul_bg":   ("#DBEAFE", "#1E3A5F"),
        "tag_azul_txt":  ("#1D4ED8", "#93C5FD"),
        "verde_bg":      ("#D1FAE5", "#052e16"),
        "verde_txt":     ("#065F46", "#6EE7B7"),
    }

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=self.COR["fundo"], **kwargs)

        self.matricula_var  = ctk.StringVar()
        self.cpf_var        = ctk.StringVar()
        self.nome_var       = ctk.StringVar()
        self.turma_var      = ctk.StringVar()
        self.email_var      = ctk.StringVar()
        self.busca_var      = ctk.StringVar()
        self.acao_atual     = None
        self.modo_lote      = False
        self.vars_chk       = []

        self._build_ui()

        if self._test_conn():
            self._carregar_turmas()
            self._refresh_table()

    # ════════════════════════════════════════════
    #  CONSTRUÇÃO DO LAYOUT
    # ════════════════════════════════════════════
    def _build_ui(self):
        self._build_header()

        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=24, pady=(0, 20))
        body.grid_columnconfigure(0, weight=0, minsize=380)
        body.grid_columnconfigure(1, weight=1)
        body.grid_rowconfigure(0, weight=1)

        self._build_left(body)
        self._build_right(body)

    def _build_header(self):
        hdr = ctk.CTkFrame(self, corner_radius=0,
                           fg_color=self.COR["card"],
                           border_width=1, border_color=self.COR["borda"])
        hdr.pack(fill="x")

        ctk.CTkFrame(hdr, height=3, corner_radius=0,
                     fg_color=self.COR["azul"]).pack(fill="x")

        inner = ctk.CTkFrame(hdr, fg_color="transparent")
        inner.pack(fill="x", padx=28, pady=14)

        self._make_logo(inner).pack(side="left", padx=(0, 16))

        txt = ctk.CTkFrame(inner, fg_color="transparent")
        txt.pack(side="left")
        ctk.CTkLabel(txt, text="Gerenciamento de Alunos",
                     font=ctk.CTkFont("Segoe UI", 22, "bold"),
                     text_color=self.COR["titulo"]).pack(anchor="w")
        ctk.CTkLabel(txt, text="Cadastre, edite e gerencie os alunos matriculados",
                     font=ctk.CTkFont("Segoe UI", 12),
                     text_color=self.COR["suave"]).pack(anchor="w")

        ctk.CTkLabel(inner, text="Tema",
                     font=ctk.CTkFont(size=12),
                     text_color=self.COR["suave"]).pack(side="right", padx=(0, 6))
        seg = ctk.CTkSegmentedButton(
            inner, values=["☀ Claro", "🌙 Escuro"],
            width=155, height=28, font=ctk.CTkFont(size=12),
            fg_color=self.COR["fundo"],
            selected_color=self.COR["azul"],
            selected_hover_color=self.COR["azul_hover"],
            command=self._mudar_tema)
        seg.set("☀ Claro")
        seg.pack(side="right")

    def _build_left(self, parent):
        panel = ctk.CTkFrame(parent, fg_color="transparent", width=380)
        panel.grid(row=0, column=0, sticky="nsew", padx=(0, 18))
        panel.grid_propagate(False)

        card = ctk.CTkFrame(panel, fg_color=self.COR["card"],
                            border_width=1, border_color=self.COR["borda"],
                            corner_radius=14)
        card.pack(fill="x")

        faixa = ctk.CTkFrame(card, fg_color=self.COR["azul"],
                             corner_radius=0, height=38)
        faixa.pack(fill="x")
        faixa.pack_propagate(False)
        ctk.CTkLabel(faixa, text="  👤  CADASTRO DE ALUNO",
                     font=ctk.CTkFont("Segoe UI", 12, "bold"),
                     text_color="white").pack(side="left", pady=8)

        pad = {"padx": 24}

        # Matrícula + busca
        ctk.CTkLabel(card, text="Matrícula",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color=self.COR["texto"]).pack(anchor="w", pady=(18, 3), **pad)

        row_mat = ctk.CTkFrame(card, fg_color="transparent")
        row_mat.pack(fill="x", **pad, pady=(0, 14))

        self.ent_matricula = ctk.CTkEntry(
            row_mat, textvariable=self.matricula_var,
            width=140, height=38, corner_radius=8,
            placeholder_text="Ex: 12345",
            border_color=self.COR["borda"])
        self.ent_matricula.pack(side="left")

        ctk.CTkButton(row_mat, text="🔍 Buscar", width=110, height=38,
                      corner_radius=8,
                      fg_color=self.COR["azul"],
                      hover_color=self.COR["azul_hover"],
                      font=ctk.CTkFont(size=13, weight="bold"),
                      command=self._buscar).pack(side="left", padx=(10, 0))

        # Nome
        ctk.CTkLabel(card, text="Nome Completo",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color=self.COR["texto"]).pack(anchor="w", pady=(0, 3), **pad)
        self.ent_nome = ctk.CTkEntry(
            card, textvariable=self.nome_var,
            width=332, height=38, corner_radius=8,
            placeholder_text="Nome completo do aluno",
            border_color=self.COR["borda"])
        self.ent_nome.pack(anchor="w", pady=(0, 14), **pad)

        # CPF + Turma na mesma linha
        row_cpf_turma = ctk.CTkFrame(card, fg_color="transparent")
        row_cpf_turma.pack(fill="x", **pad, pady=(0, 14))

        col_cpf = ctk.CTkFrame(row_cpf_turma, fg_color="transparent")
        col_cpf.pack(side="left", expand=True, fill="x", padx=(0, 10))
        ctk.CTkLabel(col_cpf, text="CPF",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color=self.COR["texto"]).pack(anchor="w", pady=(0, 3))
        self.ent_cpf = ctk.CTkEntry(
            col_cpf, textvariable=self.cpf_var,
            height=38, corner_radius=8,
            placeholder_text="000.000.000-00",
            border_color=self.COR["borda"])
        self.ent_cpf.pack(fill="x")

        col_turma = ctk.CTkFrame(row_cpf_turma, fg_color="transparent", width=140)
        col_turma.pack(side="left")
        col_turma.pack_propagate(False)
        ctk.CTkLabel(col_turma, text="Turma",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color=self.COR["texto"]).pack(anchor="w", pady=(0, 3))
        self.ent_turma = ctk.CTkOptionMenu(
            col_turma, variable=self.turma_var,
            values=["Carregando..."],
            height=38, corner_radius=8,
            fg_color=self.COR["fundo"],
            button_color=self.COR["azul"],
            button_hover_color=self.COR["azul_hover"],
            text_color=self.COR["texto"],
            dynamic_resizing=False)
        self.ent_turma.pack(fill="x")

        # E-mail
        ctk.CTkLabel(card, text="E-mail",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color=self.COR["texto"]).pack(anchor="w", pady=(0, 3), **pad)
        self.ent_email = ctk.CTkEntry(
            card, textvariable=self.email_var,
            width=332, height=38, corner_radius=8,
            placeholder_text="email@exemplo.com",
            border_color=self.COR["borda"])
        self.ent_email.pack(anchor="w", pady=(0, 22), **pad)

        # Botões de ação
        self.frame_btns = ctk.CTkFrame(panel, fg_color="transparent")
        self.frame_btns.pack(fill="x", pady=(14, 0))

        self._btn(self.frame_btns, "➕  Inserir",
                  self.COR["azul_esc"], self.COR["azul"],
                  self._prep_inserir).pack(side="left", expand=True, fill="x", padx=(0, 5))
        self._btn(self.frame_btns, "✏️  Alterar",
                  self.COR["azul"], self.COR["azul_hover"],
                  self._prep_alterar).pack(side="left", expand=True, fill="x", padx=5)
        self._btn(self.frame_btns, "🗑️  Excluir",
                  self.COR["perigo"], self.COR["perigo_hov"],
                  self._prep_excluir).pack(side="left", expand=True, fill="x", padx=(5, 0))

        self.frame_conf = ctk.CTkFrame(panel, fg_color="transparent")
        self._btn(self.frame_conf, "✔  Confirmar",
                  self.COR["sucesso"], self.COR["sucesso_hov"],
                  self._confirmar).pack(side="left", expand=True, fill="x", padx=(0, 5))
        ctk.CTkButton(
            self.frame_conf, text="✖  Cancelar", height=42, corner_radius=8,
            fg_color="transparent", border_width=1,
            border_color=self.COR["perigo"],
            text_color=self.COR["perigo"],
            hover_color=self.COR["perigo_bg"],
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self._cancelar).pack(side="left", expand=True, fill="x", padx=(5, 0))

        self.lbl_dica = ctk.CTkLabel(
            panel,
            text="💡 Busque pela matrícula para editar ou excluir",
            font=ctk.CTkFont(size=11),
            text_color=self.COR["suave"])
        self.lbl_dica.pack(pady=(12, 0))

    def _build_right(self, parent):
        panel = ctk.CTkFrame(parent, fg_color="transparent")
        panel.grid(row=0, column=1, sticky="nsew")
        panel.grid_rowconfigure(1, weight=1)
        panel.grid_columnconfigure(0, weight=1)

        # Métrica
        metric = ctk.CTkFrame(panel, fg_color=self.COR["card"],
                               border_width=1, border_color=self.COR["borda"],
                               corner_radius=12, height=70)
        metric.grid(row=0, column=0, sticky="ew", pady=(0, 14))
        metric.pack_propagate(False)
        ctk.CTkLabel(metric, text="🎓  Total de Alunos Matriculados:",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color=self.COR["suave"]).pack(side="left", padx=20)
        self.lbl_total = ctk.CTkLabel(metric, text="—",
                                       font=ctk.CTkFont(size=28, weight="bold"),
                                       text_color=self.COR["azul"])
        self.lbl_total.pack(side="right", padx=20)

        # Card tabela
        tcard = ctk.CTkFrame(panel, fg_color=self.COR["card"],
                              border_width=1, border_color=self.COR["borda"],
                              corner_radius=14)
        tcard.grid(row=1, column=0, sticky="nsew")
        tcard.grid_rowconfigure(1, weight=1)
        tcard.grid_columnconfigure(0, weight=1)

        # Barra superior
        barra = ctk.CTkFrame(tcard, fg_color="transparent")
        barra.grid(row=0, column=0, sticky="ew", padx=20, pady=(14, 8))

        ctk.CTkLabel(barra, text="Lista Oficial de Alunos",
                     font=ctk.CTkFont(size=14, weight="bold"),
                     text_color=self.COR["texto"]).pack(side="left")

        # Excluir todos
        self.btn_exc_todos = ctk.CTkButton(
            barra, text="⚠ Excluir Todos", width=125, height=30,
            corner_radius=8, font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=self.COR["perigo"], hover_color=self.COR["perigo_hov"],
            command=self._excluir_todos)
        self.btn_exc_todos.pack(side="right", padx=(5, 0))

        # Modo lote
        self.btn_lote = ctk.CTkButton(
            barra, text="☑  Seleção", width=100, height=30,
            corner_radius=8, font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="transparent", border_width=1,
            border_color=self.COR["azul"],
            text_color=self.COR["azul"],
            hover_color=self.COR["fundo"],
            command=self._toggle_lote)
        self.btn_lote.pack(side="right", padx=(0, 5))

        # Importar Excel
        ctk.CTkButton(
            barra, text="📥 Importar Excel", width=130, height=30,
            corner_radius=8, font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=self.COR["sucesso"], hover_color=self.COR["sucesso_hov"],
            command=self._importar_excel).pack(side="right", padx=(0, 5))

        # Busca
        self.ent_busca = ctk.CTkEntry(
            barra, textvariable=self.busca_var,
            placeholder_text="🔍  Filtrar alunos...",
            width=190, height=30, corner_radius=8)
        self.ent_busca.pack(side="right", padx=(0, 10))
        self.ent_busca.bind("<KeyRelease>", lambda _: self._refresh_table())

        # Scroll
        self.scroll = ctk.CTkScrollableFrame(
            tcard, fg_color=self.COR["fundo"], corner_radius=8)
        self.scroll.grid(row=1, column=0, sticky="nsew", padx=16, pady=(0, 16))

    # ════════════════════════════════════════════
    #  TABELA
    # ════════════════════════════════════════════
    def _refresh_table(self):
        for w in self.scroll.winfo_children():
            w.destroy()
        self.vars_chk.clear()

        # Cabeçalho
        cab = ctk.CTkFrame(self.scroll, fg_color="transparent")
        cab.pack(fill="x", pady=(0, 4))
        if self.modo_lote:
            ctk.CTkLabel(cab, text="", width=30).pack(side="left")
        ctk.CTkLabel(cab, text="MATRÍCULA", font=ctk.CTkFont(size=11, weight="bold"),
                     text_color=self.COR["suave"], width=90, anchor="w").pack(side="left", padx=(8, 0))
        ctk.CTkLabel(cab, text="NOME", font=ctk.CTkFont(size=11, weight="bold"),
                     text_color=self.COR["suave"], anchor="w").pack(side="left", padx=12, fill="x", expand=True)
        ctk.CTkLabel(cab, text="TURMA", font=ctk.CTkFont(size=11, weight="bold"),
                     text_color=self.COR["suave"], width=70, anchor="center").pack(side="right", padx=10)
        ctk.CTkLabel(cab, text="CPF", font=ctk.CTkFont(size=11, weight="bold"),
                     text_color=self.COR["suave"], width=120, anchor="w").pack(side="right", padx=10)

        conn = self._db()
        if not conn:
            ctk.CTkLabel(self.scroll,
                         text="⚠  Sem conexão com o banco de dados.",
                         text_color=self.COR["perigo"],
                         font=ctk.CTkFont(size=13)).pack(pady=40)
            return

        try:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM alunos")
            self.lbl_total.configure(text=str(cur.fetchone()[0]))

            filtro = self.busca_var.get().strip()
            if filtro:
                cur.execute(
                    "SELECT matricula, nome_completo, codturma, cpf FROM alunos "
                    "WHERE CAST(matricula AS CHAR) LIKE %s "
                    "   OR nome_completo LIKE %s "
                    "   OR cpf LIKE %s "
                    "ORDER BY nome_completo",
                    (f"%{filtro}%", f"%{filtro}%", f"%{filtro}%"))
            else:
                cur.execute(
                    "SELECT matricula, nome_completo, codturma, cpf "
                    "FROM alunos ORDER BY nome_completo")

            rows = cur.fetchall()
            if not rows:
                ctk.CTkLabel(self.scroll,
                             text="Nenhum aluno encontrado.",
                             text_color=self.COR["suave"],
                             font=ctk.CTkFont(size=13)).pack(pady=40)
                return

            for i, (mat, nome, turma, cpf) in enumerate(rows):
                bg = self.COR["linha_a"] if i % 2 == 0 else self.COR["linha_b"]
                linha = ctk.CTkFrame(self.scroll, height=40, fg_color=bg,
                                     corner_radius=6, border_width=1,
                                     border_color=self.COR["borda"])
                linha.pack(fill="x", pady=2)
                linha.pack_propagate(False)

                if self.modo_lote:
                    var = ctk.StringVar(value="off")
                    self.vars_chk.append((var, str(mat)))
                    ctk.CTkCheckBox(linha, text="", variable=var,
                                    onvalue="on", offvalue="off",
                                    width=20, fg_color=self.COR["azul"],
                                    border_color=self.COR["borda"],
                                    checkmark_color="white"
                                    ).pack(side="left", padx=(10, 0))

                ctk.CTkLabel(linha, text=str(mat),
                             font=ctk.CTkFont(size=13, weight="bold"),
                             text_color=self.COR["azul"],
                             width=90, anchor="w").pack(side="left", padx=(8, 0))

                ctk.CTkLabel(linha, text=str(nome),
                             font=ctk.CTkFont(size=13),
                             text_color=self.COR["texto"],
                             anchor="w").pack(side="left", padx=12, fill="x", expand=True)

                # CPF
                ctk.CTkLabel(linha, text=str(cpf),
                             font=ctk.CTkFont(size=12),
                             text_color=self.COR["suave"],
                             width=120, anchor="w").pack(side="right", padx=10)

                # Tag turma
                tag = ctk.CTkLabel(
                    linha, text=f"  {turma}  ",
                    font=ctk.CTkFont(size=11, weight="bold"),
                    fg_color=self.COR["tag_azul_bg"],
                    text_color=self.COR["tag_azul_txt"],
                    corner_radius=6, width=65, height=24)
                tag.pack(side="right", padx=10)

        except mysql.connector.Error as e:
            print(f"[tela_alunos] Erro tabela: {e}")
        finally:
            cur.close()
            conn.close()

    # ════════════════════════════════════════════
    #  CRUD
    # ════════════════════════════════════════════
    def _carregar_turmas(self):
        conn = self._db(silencioso=True)
        if not conn:
            return
        try:
            cur = conn.cursor()
            cur.execute("SELECT codturma FROM turmas ORDER BY codturma")
            turmas = [str(t[0]) for t in cur.fetchall()]
            if turmas:
                self.ent_turma.configure(values=turmas)
                self.turma_var.set(turmas[0])
            else:
                self.ent_turma.configure(values=["Sem turmas"])
                self.turma_var.set("Sem turmas")
        except Exception as e:
            print(f"[tela_alunos] carregar_turmas: {e}")
        finally:
            cur.close()
            conn.close()

    def _buscar(self):
        mat = self.matricula_var.get().strip()
        if not mat:
            messagebox.showwarning("Aviso", "Digite uma matrícula para buscar.")
            return
        conn = self._db()
        if not conn:
            return
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT cpf, nome_completo, codturma, email FROM alunos WHERE matricula = %s",
                (mat,))
            res = cur.fetchone()
            if res:
                self.cpf_var.set(res[0])
                self.nome_var.set(res[1])
                self.turma_var.set(str(res[2]))
                self.email_var.set(res[3])
                self.ent_matricula.configure(border_color=self.COR["sucesso"])
                self.after(1500, lambda: self.ent_matricula.configure(border_color=self.COR["borda"]))
            else:
                self._limpar_campos(manter_matricula=True)
                messagebox.showinfo("Matrícula disponível",
                    "Esta matrícula não está cadastrada.\nPreencha os dados e clique em Inserir.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
        finally:
            cur.close()
            conn.close()

    def _confirmar(self):
        mat   = self.matricula_var.get().strip()
        cpf   = self.cpf_var.get().strip()
        nome  = self.nome_var.get().strip()
        turma = self.turma_var.get().strip()
        email = self.email_var.get().strip()

        if turma == "Sem turmas":
            messagebox.showerror("Bloqueado",
                "Não há turmas cadastradas. Cadastre uma turma antes de inserir alunos.")
            return

        if self.acao_atual in ("INSERIR", "ALTERAR"):
            if not mat or not nome or not cpf or not email:
                messagebox.showwarning("Campos obrigatórios",
                    "Matrícula, Nome, CPF e E-mail são obrigatórios.")
                return

        conn = self._db()
        if not conn:
            return
        try:
            cur = conn.cursor()
            if self.acao_atual == "INSERIR":
                cur.execute(
                    "INSERT INTO alunos (matricula, cpf, nome_completo, codturma, email) "
                    "VALUES (%s, %s, %s, %s, %s)",
                    (mat, cpf, nome, turma, email))
                conn.commit()
                messagebox.showinfo("✅ Sucesso", "Aluno cadastrado com sucesso!")
            elif self.acao_atual == "ALTERAR":
                cur.execute(
                    "UPDATE alunos SET cpf=%s, nome_completo=%s, codturma=%s, email=%s "
                    "WHERE matricula=%s",
                    (cpf, nome, turma, email, mat))
                conn.commit()
                messagebox.showinfo("✅ Sucesso", "Cadastro do aluno atualizado!")
            elif self.acao_atual == "EXCLUIR":
                cur.execute("DELETE FROM alunos WHERE matricula = %s", (mat,))
                conn.commit()
                messagebox.showinfo("✅ Sucesso", "Aluno removido.")
            self._reset()
            self._refresh_table()
        except mysql.connector.Error as e:
            if e.errno == 1062:
                messagebox.showwarning("Duplicado",
                    "Matrícula ou CPF já cadastrados no sistema.")
            elif e.errno == 1452:
                messagebox.showerror("Erro de integridade",
                    f"A turma '{turma}' não existe no banco de dados.")
            else:
                messagebox.showerror("Erro SQL", str(e))
        finally:
            cur.close()
            conn.close()

    def _excluir_todos(self):
        if self.modo_lote:
            sels = [mat for var, mat in self.vars_chk if var.get() == "on"]
            if not sels:
                messagebox.showwarning("Aviso", "Nenhum aluno selecionado.")
                return
            if not messagebox.askyesno("Confirmar",
                    f"Excluir permanentemente {len(sels)} aluno(s)?"):
                return
            conn = self._db()
            if not conn:
                return
            try:
                cur = conn.cursor()
                ph = ",".join(["%s"] * len(sels))
                cur.execute(f"DELETE FROM alunos WHERE matricula IN ({ph})", tuple(sels))
                conn.commit()
                messagebox.showinfo("✅ Sucesso", f"{cur.rowcount} aluno(s) removido(s).")
            except Exception as e:
                messagebox.showerror("Erro", str(e))
            finally:
                cur.close()
                conn.close()
            self._toggle_lote()
        else:
            if not messagebox.askyesno("⚠ Atenção",
                    "Excluir TODOS os alunos?\nEsta ação não pode ser desfeita."):
                return
            conn = self._db()
            if not conn:
                return
            try:
                cur = conn.cursor()
                cur.execute("DELETE FROM alunos")
                conn.commit()
                messagebox.showinfo("✅ Concluído", f"{cur.rowcount} aluno(s) removido(s).")
                self._refresh_table()
            except Exception as e:
                messagebox.showerror("Erro", str(e))
            finally:
                cur.close()
                conn.close()

    def _importar_excel(self):
        caminho = filedialog.askopenfilename(
            title="Selecionar planilha de alunos",
            filetypes=[("Excel", "*.xlsx *.xls")])
        if not caminho:
            return

        conn = None
        cur  = None
        try:
            df = pd.read_excel(caminho)
            colunas = ['Matrícula', 'Nome Completo', 'CPF', 'Cód. Turma', 'E-mail']
            if not all(c in df.columns for c in colunas):
                messagebox.showerror("Estrutura inválida",
                    f"A planilha deve ter exatamente as colunas:\n{', '.join(colunas)}")
                return

            conn = self._db(silencioso=True)
            if not conn:
                messagebox.showerror("Erro", "Sem conexão com o banco.")
                return
            cur = conn.cursor()

            inseridos = 0
            erros = []

            for idx, row in df.iterrows():
                linha_excel = idx + 2
                try:
                    if pd.isna(row['Matrícula']):
                        continue
                    mat   = str(row['Matrícula']).strip().replace('.0', '')
                    turma = str(row['Cód. Turma']).strip().replace('.0', '')
                    nome  = str(row['Nome Completo']).strip()
                    cpf   = str(row['CPF']).strip() if not pd.isna(row['CPF']) else ""
                    email = str(row['E-mail']).strip() if not pd.isna(row['E-mail']) else ""

                    if nome.lower() == "nan":
                        continue

                    cur.execute(
                        "INSERT INTO alunos (matricula, cpf, nome_completo, codturma, email) "
                        "VALUES (%s, %s, %s, %s, %s)",
                        (mat, cpf, nome, turma, email))
                    inseridos += 1
                except mysql.connector.Error as e:
                    if e.errno == 1452:
                        erros.append(f"Linha {linha_excel}: Turma '{turma}' inexistente.")
                    elif e.errno == 1062:
                        erros.append(f"Linha {linha_excel}: Matrícula/CPF duplicado.")
                    else:
                        erros.append(f"Linha {linha_excel}: {e.msg}")
                except Exception as e:
                    erros.append(f"Linha {linha_excel}: {str(e)}")

            if inseridos > 0:
                conn.commit()

            self._refresh_table()

            if erros:
                resumo = "\n".join(erros[:10])
                if len(erros) > 10:
                    resumo += f"\n... e mais {len(erros) - 10} erro(s)."
                messagebox.showwarning("Importação com alertas",
                    f"✅ {inseridos} aluno(s) importado(s).\n\nProblemas:\n{resumo}")
            else:
                messagebox.showinfo("✅ Importação concluída",
                    f"Todos os {inseridos} alunos foram importados com sucesso!")

        except Exception as e:
            messagebox.showerror("Erro geral", str(e))
        finally:
            if cur:
                cur.close()
            if conn and conn.is_connected():
                conn.close()

    # ════════════════════════════════════════════
    #  CONTROLE DE INTERFACE
    # ════════════════════════════════════════════
    def _toggle_lote(self):
        self.modo_lote = not self.modo_lote
        if self.modo_lote:
            self.btn_lote.configure(text="✖  Cancelar",
                                     border_color=self.COR["perigo"],
                                     text_color=self.COR["perigo"])
            self.btn_exc_todos.configure(text="🗑 Excluir Sel.")
        else:
            self.btn_lote.configure(text="☑  Seleção",
                                     border_color=self.COR["azul"],
                                     text_color=self.COR["azul"])
            self.btn_exc_todos.configure(text="⚠ Excluir Todos")
        self._refresh_table()

    def _prep_inserir(self):
        if not self.matricula_var.get().strip() or not self.nome_var.get().strip():
            messagebox.showwarning("Campos obrigatórios",
                "Matrícula e Nome são obrigatórios.")
            return
        self.acao_atual = "INSERIR"
        self._show_conf()

    def _prep_alterar(self):
        if not self.matricula_var.get().strip() or not self.nome_var.get().strip():
            messagebox.showwarning("Aviso", "Busque um aluno e edite os dados antes de alterar.")
            return
        self.acao_atual = "ALTERAR"
        self._show_conf()

    def _prep_excluir(self):
        if not self.matricula_var.get().strip():
            messagebox.showwarning("Aviso", "Insira a matrícula do aluno a excluir.")
            return
        self.acao_atual = "EXCLUIR"
        self._show_conf()

    def _show_conf(self):
        self.frame_btns.pack_forget()
        self.lbl_dica.pack_forget()
        self.frame_conf.pack(fill="x", pady=(14, 0))
        self.ent_matricula.configure(state="disabled")
        if self.acao_atual == "EXCLUIR":
            for e in [self.ent_nome, self.ent_cpf,
                      self.ent_turma, self.ent_email]:
                e.configure(state="disabled")

    def _hide_conf(self):
        self.frame_conf.pack_forget()
        self.frame_btns.pack(fill="x", pady=(14, 0))
        self.lbl_dica.pack(pady=(12, 0))
        for e in [self.ent_matricula, self.ent_nome,
                  self.ent_cpf, self.ent_turma, self.ent_email]:
            e.configure(state="normal")

    def _cancelar(self):
        self._reset()

    def _limpar_campos(self, manter_matricula=False):
        if not manter_matricula:
            self.matricula_var.set("")
        self.cpf_var.set("")
        self.nome_var.set("")
        self.email_var.set("")
        if hasattr(self, 'ent_turma'):
            vals = self.ent_turma.cget("values")
            if vals and vals[0] not in ("Carregando...", "Sem turmas"):
                self.turma_var.set(vals[0])

    def _reset(self):
        self._limpar_campos()
        self._hide_conf()
        self.acao_atual = None

    # ════════════════════════════════════════════
    #  UTILITÁRIOS
    # ════════════════════════════════════════════
    def _test_conn(self):
        conn = self._db(silencioso=True)
        if conn:
            conn.close()
            return True
        messagebox.showerror("Erro Crítico", "Falha ao conectar ao banco de dados.")
        return False

    def _db(self, silencioso=False):
        try:
            return mysql.connector.connect(
                host="localhost", user="root",
                password="IzaelMendes123", database="avisos_sistema")
        except mysql.connector.Error as e:
            if not silencioso:
                messagebox.showerror("Erro de Conexão", str(e))
            return None

    @staticmethod
    def _btn(parent, text, fg, hover, cmd):
        return ctk.CTkButton(parent, text=text, height=42, corner_radius=8,
                             fg_color=fg, hover_color=hover,
                             font=ctk.CTkFont(size=13, weight="bold"),
                             command=cmd)

    @staticmethod
    def _mudar_tema(escolha):
        ctk.set_appearance_mode("Dark" if "Escuro" in escolha else "Light")

    def _make_logo(self, parent):
        path = "logo_univap.png"
        if os.path.exists(path):
            try:
                img = Image.open(path)
                cimg = ctk.CTkImage(light_image=img, dark_image=img, size=(52, 52))
                return ctk.CTkLabel(parent, image=cimg, text="")
            except Exception:
                pass
        return ctk.CTkLabel(parent, text="UNIVAP",
                            font=ctk.CTkFont(weight="bold", size=11),
                            fg_color=self.COR["azul"], text_color="white",
                            width=52, height=52, corner_radius=8)


if __name__ == "__main__":
    app = ctk.CTk()
    app.title("Alunos – Sistema Univap")
    app.geometry("1200x700")
    TelaCadastroAlunos(app).pack(fill="both", expand=True)
    app.mainloop()