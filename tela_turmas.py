import customtkinter as ctk
from tkinter import messagebox
import mysql.connector
import os
from PIL import Image

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")


class TelaCadastroTurmas(ctk.CTkFrame):
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
    }

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=self.COR["fundo"], **kwargs)

        self.codturma_var  = ctk.StringVar()
        self.curso_var     = ctk.StringVar()
        self.busca_var     = ctk.StringVar()
        self.acao_atual    = None
        self.modo_selecao  = False
        self.vars_chk      = {}
        self.mapa_cursos   = {}   # "101 – Engenharia" → 101

        self._build_ui()

        if self._test_conn():
            self._carregar_cursos()
            self._refresh_table()

    # ════════════════════════════════════════════
    #  CONSTRUÇÃO DO LAYOUT
    # ════════════════════════════════════════════
    def _build_ui(self):
        self._build_header()

        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=24, pady=(0, 20))
        body.grid_columnconfigure(0, weight=0, minsize=360)
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
        ctk.CTkLabel(txt, text="Gerenciamento de Turmas",
                     font=ctk.CTkFont("Segoe UI", 22, "bold"),
                     text_color=self.COR["titulo"]).pack(anchor="w")
        ctk.CTkLabel(txt, text="Vincule turmas aos cursos cadastrados",
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
        panel = ctk.CTkFrame(parent, fg_color="transparent", width=360)
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
        ctk.CTkLabel(faixa, text="  🏫  CADASTRO DE TURMA",
                     font=ctk.CTkFont("Segoe UI", 12, "bold"),
                     text_color="white").pack(side="left", pady=8)

        pad = {"padx": 24}

        # Código da Turma
        ctk.CTkLabel(card, text="Código da Turma",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color=self.COR["texto"]).pack(anchor="w", pady=(18, 3), **pad)

        row_cod = ctk.CTkFrame(card, fg_color="transparent")
        row_cod.pack(fill="x", **pad, pady=(0, 4))

        self.ent_codturma = ctk.CTkEntry(
            row_cod, textvariable=self.codturma_var,
            width=140, height=38, corner_radius=8,
            placeholder_text="Ex: 3A",
            border_color=self.COR["borda"])
        self.ent_codturma.pack(side="left")
        self.ent_codturma.bind("<KeyRelease>",
            lambda e: self.codturma_var.set(self.codturma_var.get().upper()))

        ctk.CTkButton(row_cod, text="🔍 Buscar", width=110, height=38,
                      corner_radius=8,
                      fg_color=self.COR["azul"],
                      hover_color=self.COR["azul_hover"],
                      font=ctk.CTkFont(size=13, weight="bold"),
                      command=self._buscar).pack(side="left", padx=(10, 0))

        ctk.CTkLabel(card,
                     text="  Letras maiúsculas. Ex: 3A, 3I, 4N",
                     font=ctk.CTkFont(size=11),
                     text_color=self.COR["suave"]).pack(anchor="w", pady=(0, 14), **pad)

        # Curso vinculado
        ctk.CTkLabel(card, text="Vincular ao Curso",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color=self.COR["texto"]).pack(anchor="w", pady=(0, 3), **pad)

        self.ent_curso = ctk.CTkOptionMenu(
            card, variable=self.curso_var,
            values=["Carregando..."],
            width=312, height=38, corner_radius=8,
            fg_color=self.COR["fundo"],
            button_color=self.COR["azul"],
            button_hover_color=self.COR["azul_hover"],
            text_color=self.COR["texto"],
            dynamic_resizing=False)
        self.ent_curso.pack(anchor="w", pady=(0, 24), **pad)

        # Botões
        self.frame_btns = ctk.CTkFrame(panel, fg_color="transparent")
        self.frame_btns.pack(fill="x", pady=(14, 0))

        self._btn(self.frame_btns, " Inserir",
                  self.COR["azul_esc"], self.COR["azul"],
                  self._prep_inserir).pack(side="left", expand=True, fill="x", padx=(0, 5))

        self._btn(self.frame_btns, " Alterar",
                  self.COR["azul"], self.COR["azul_hover"],
                  self._prep_alterar).pack(side="left", expand=True, fill="x", padx=5)

        self._btn(self.frame_btns, " Excluir",
                  self.COR["perigo"], self.COR["perigo_hov"],
                  self._prep_excluir).pack(side="left", expand=True, fill="x", padx=(5, 0))

        self.frame_conf = ctk.CTkFrame(panel, fg_color="transparent")
        self._btn(self.frame_conf, " Confirmar",
                  self.COR["sucesso"], self.COR["sucesso_hov"],
                  self._confirmar).pack(side="left", expand=True, fill="x", padx=(0, 5))
        ctk.CTkButton(
            self.frame_conf, text=" Cancelar", height=42, corner_radius=8,
            fg_color="transparent", border_width=1,
            border_color=self.COR["perigo"],
            text_color=self.COR["perigo"],
            hover_color=self.COR["perigo_bg"],
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self._cancelar).pack(side="left", expand=True, fill="x", padx=(5, 0))

        self.lbl_dica = ctk.CTkLabel(
            panel,
            text=" ",
            font=ctk.CTkFont(size=11),
            text_color=self.COR["suave"])
        self.lbl_dica.pack(pady=(12, 0))

    def _build_right(self, parent):
        panel = ctk.CTkFrame(parent, fg_color="transparent")
        panel.grid(row=0, column=1, sticky="nsew")
        panel.grid_rowconfigure(1, weight=1)
        panel.grid_columnconfigure(0, weight=1)

        metric = ctk.CTkFrame(panel, fg_color=self.COR["card"],
                               border_width=1, border_color=self.COR["borda"],
                               corner_radius=12, height=70)
        metric.grid(row=0, column=0, sticky="ew", pady=(0, 14))
        metric.pack_propagate(False)
        ctk.CTkLabel(metric, text="🏫  Total de Turmas Cadastradas:",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color=self.COR["suave"]).pack(side="left", padx=20)
        self.lbl_total = ctk.CTkLabel(metric, text="—",
                                       font=ctk.CTkFont(size=28, weight="bold"),
                                       text_color=self.COR["azul"])
        self.lbl_total.pack(side="right", padx=20)

        tcard = ctk.CTkFrame(panel, fg_color=self.COR["card"],
                              border_width=1, border_color=self.COR["borda"],
                              corner_radius=14)
        tcard.grid(row=1, column=0, sticky="nsew")
        tcard.grid_rowconfigure(1, weight=1)
        tcard.grid_columnconfigure(0, weight=1)

        barra = ctk.CTkFrame(tcard, fg_color="transparent")
        barra.grid(row=0, column=0, sticky="ew", padx=20, pady=(14, 8))

        ctk.CTkLabel(barra, text="Lista Oficial de Turmas",
                     font=ctk.CTkFont(size=14, weight="bold"),
                     text_color=self.COR["texto"]).pack(side="left")

        self.btn_exc_todos = ctk.CTkButton(
            barra, text="⚠ Excluir Todas", width=130, height=30,
            corner_radius=8, font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=self.COR["perigo"], hover_color=self.COR["perigo_hov"],
            command=self._excluir_todos)
        self.btn_exc_todos.pack(side="right", padx=(5, 0))

        self.btn_selecao = ctk.CTkButton(
            barra, text="☑  Selecionar", width=120, height=30,
            corner_radius=8, font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="transparent", border_width=1,
            border_color=self.COR["azul"],
            text_color=self.COR["azul"],
            hover_color=self.COR["fundo"],
            command=self._toggle_selecao)
        self.btn_selecao.pack(side="right", padx=(0, 5))

        self.ent_busca = ctk.CTkEntry(
            barra, textvariable=self.busca_var,
            placeholder_text="🔍  Filtrar turmas...",
            width=200, height=30, corner_radius=8)
        self.ent_busca.pack(side="right", padx=(0, 10))
        self.ent_busca.bind("<KeyRelease>", lambda _: self._refresh_table())

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

        cab = ctk.CTkFrame(self.scroll, fg_color="transparent")
        cab.pack(fill="x", pady=(0, 4))
        if self.modo_selecao:
            ctk.CTkLabel(cab, text="", width=30).pack(side="left")
        ctk.CTkLabel(cab, text="TURMA", font=ctk.CTkFont(size=11, weight="bold"),
                     text_color=self.COR["suave"], width=90, anchor="w").pack(side="left", padx=(8, 0))
        ctk.CTkLabel(cab, text="CURSO VINCULADO",
                     font=ctk.CTkFont(size=11, weight="bold"),
                     text_color=self.COR["suave"], anchor="w").pack(side="left", padx=12, fill="x", expand=True)

        conn = self._db()
        if not conn:
            ctk.CTkLabel(self.scroll,
                         text="⚠  Sem conexão com o banco de dados.",
                         text_color=self.COR["perigo"],
                         font=ctk.CTkFont(size=13)).pack(pady=40)
            return

        try:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM turmas")
            self.lbl_total.configure(text=str(cur.fetchone()[0]))

            filtro = self.busca_var.get().strip()
            sql = """
                SELECT t.codturma, c.descricao, c.codcurso
                FROM turmas t
                LEFT JOIN cursos c ON t.codcurso = c.codcurso
            """
            if filtro:
                sql += " WHERE t.codturma LIKE %s OR c.descricao LIKE %s"
                sql += " ORDER BY LENGTH(t.codturma) ASC, t.codturma ASC"
                cur.execute(sql, (f"%{filtro}%", f"%{filtro}%"))
            else:
                sql += " ORDER BY LENGTH(t.codturma) ASC, t.codturma ASC"
                cur.execute(sql)

            rows = cur.fetchall()
            if not rows:
                ctk.CTkLabel(self.scroll,
                             text="Nenhuma turma encontrada.",
                             text_color=self.COR["suave"],
                             font=ctk.CTkFont(size=13)).pack(pady=40)
                return

            for i, (cod, nome_curso, _) in enumerate(rows):
                bg = self.COR["linha_a"] if i % 2 == 0 else self.COR["linha_b"]
                linha = ctk.CTkFrame(self.scroll, height=40, fg_color=bg,
                                     corner_radius=6, border_width=1,
                                     border_color=self.COR["borda"])
                linha.pack(fill="x", pady=2)
                linha.pack_propagate(False)

                if self.modo_selecao:
                    var = ctk.StringVar(value="off")
                    self.vars_chk[cod] = var
                    ctk.CTkCheckBox(linha, text="", variable=var,
                                    onvalue="on", offvalue="off",
                                    width=20, fg_color=self.COR["azul"],
                                    border_color=self.COR["borda"],
                                    checkmark_color="white"
                                    ).pack(side="left", padx=(10, 0))

                # Tag visual da turma
                tag = ctk.CTkLabel(
                    linha, text=f"  {cod}  ",
                    font=ctk.CTkFont(size=12, weight="bold"),
                    fg_color=self.COR["tag_azul_bg"],
                    text_color=self.COR["tag_azul_txt"],
                    corner_radius=6, width=75, height=26)
                tag.pack(side="left", padx=(8, 0))

                curso_txt = nome_curso if nome_curso else "Curso removido"
                ctk.CTkLabel(linha, text=curso_txt,
                             font=ctk.CTkFont(size=13),
                             text_color=self.COR["texto"],
                             anchor="w").pack(side="left", padx=12, fill="x", expand=True)

        except mysql.connector.Error as e:
            print(f"[tela_turmas] Erro: {e}")
        finally:
            cur.close()
            conn.close()

    # ════════════════════════════════════════════
    #  CRUD
    # ════════════════════════════════════════════
    def _carregar_cursos(self):
        conn = self._db(silencioso=True)
        if not conn:
            return
        try:
            cur = conn.cursor()
            cur.execute("SELECT codcurso, descricao FROM cursos ORDER BY descricao")
            self.mapa_cursos.clear()
            lista = []
            for cod, desc in cur.fetchall():
                txt = f"{cod} – {desc}"
                lista.append(txt)
                self.mapa_cursos[txt] = cod
            if lista:
                self.ent_curso.configure(values=lista)
                self.curso_var.set(lista[0])
            else:
                self.ent_curso.configure(values=["Nenhum curso cadastrado"])
                self.curso_var.set("Nenhum curso cadastrado")
        except Exception as e:
            print(f"[tela_turmas] carregar_cursos: {e}")
        finally:
            cur.close()
            conn.close()

    def _buscar(self):
        cod = self.codturma_var.get().strip()
        if not cod:
            messagebox.showwarning("Aviso", "Digite o código da turma para buscar.")
            return
        conn = self._db()
        if not conn:
            return
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT c.codcurso, c.descricao FROM turmas t
                JOIN cursos c ON t.codcurso = c.codcurso
                WHERE t.codturma = %s
            """, (cod,))
            res = cur.fetchone()
            if res:
                for txt, id_real in self.mapa_cursos.items():
                    if id_real == res[0]:
                        self.curso_var.set(txt)
                        break
                self.ent_codturma.configure(border_color=self.COR["sucesso"])
                self.after(1500, lambda: self.ent_codturma.configure(border_color=self.COR["borda"]))
            else:
                messagebox.showinfo("Código livre",
                    f"A turma '{cod}' não existe.\nPreencha os dados e clique em Inserir.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
        finally:
            cur.close()
            conn.close()

    def _confirmar(self):
        cod   = self.codturma_var.get().strip()
        opcao = self.curso_var.get()

        if not cod:
            messagebox.showwarning("Aviso", "Preencha o código da turma.")
            return
        if opcao in ("Carregando...", "Nenhum curso cadastrado"):
            messagebox.showerror("Bloqueado",
                "Cadastre um curso antes de criar uma turma.")
            return

        cod_curso = self.mapa_cursos.get(opcao)
        if not cod_curso:
            messagebox.showerror("Erro", "Curso selecionado inválido.")
            return

        conn = self._db()
        if not conn:
            return
        try:
            cur = conn.cursor()
            if self.acao_atual == "INSERIR":
                cur.execute("INSERT INTO turmas (codturma, codcurso) VALUES (%s, %s)",
                            (cod, cod_curso))
                conn.commit()
                messagebox.showinfo("✅ Sucesso", "Turma cadastrada e vinculada ao curso!")
            elif self.acao_atual == "ALTERAR":
                cur.execute("UPDATE turmas SET codcurso = %s WHERE codturma = %s",
                            (cod_curso, cod))
                conn.commit()
                messagebox.showinfo("✅ Sucesso", "Turma atualizada!")
            elif self.acao_atual == "EXCLUIR":
                cur.execute("DELETE FROM turmas WHERE codturma = %s", (cod,))
                conn.commit()
                messagebox.showinfo("✅ Sucesso", "Turma removida.")
            self._reset()
            self._refresh_table()
        except mysql.connector.Error as e:
            if e.errno == 1451:
                messagebox.showerror("Bloqueado",
                    "Não é possível excluir: existem alunos matriculados nesta turma.")
            elif e.errno == 1062:
                messagebox.showwarning("Duplicado",
                    f"Já existe uma turma com o código '{cod}'.")
            else:
                messagebox.showerror("Erro SQL", str(e))
        finally:
            cur.close()
            conn.close()

    def _excluir_todos(self):
        if self.modo_selecao:
            sels = [c for c, v in self.vars_chk.items() if v.get() == "on"]
            if not sels:
                messagebox.showwarning("Aviso", "Nenhuma turma selecionada.")
                return
            if not messagebox.askyesno("Confirmar",
                    f"Excluir {len(sels)} turma(s) selecionada(s)?"):
                return
            conn = self._db()
            if not conn:
                return
            erros = 0
            try:
                cur = conn.cursor()
                for c in sels:
                    try:
                        cur.execute("DELETE FROM turmas WHERE codturma = %s", (c,))
                    except mysql.connector.Error as e:
                        if e.errno == 1451:
                            erros += 1
                conn.commit()
                if erros:
                    messagebox.showwarning("Atenção",
                        f"{erros} turma(s) não removida(s) — possuem alunos vinculados.")
                else:
                    messagebox.showinfo("✅ Sucesso", "Turmas selecionadas removidas.")
            except Exception as e:
                messagebox.showerror("Erro", str(e))
            finally:
                cur.close()
                conn.close()
            self._toggle_selecao()
        else:
            if not messagebox.askyesno("⚠ Atenção",
                    "Excluir TODAS as turmas?\nEsta ação não pode ser desfeita."):
                return
            conn = self._db()
            if not conn:
                return
            try:
                cur = conn.cursor()
                cur.execute("DELETE FROM turmas")
                conn.commit()
                messagebox.showinfo("✅ Concluído", f"{cur.rowcount} turma(s) removida(s).")
                self._refresh_table()
            except mysql.connector.Error as e:
                if e.errno == 1451:
                    messagebox.showerror("Bloqueado",
                        "Existem alunos matriculados. Remova os alunos primeiro.")
                else:
                    messagebox.showerror("Erro SQL", str(e))
            finally:
                cur.close()
                conn.close()

    # ════════════════════════════════════════════
    #  CONTROLE DE INTERFACE
    # ════════════════════════════════════════════
    def _toggle_selecao(self):
        self.modo_selecao = not self.modo_selecao
        if self.modo_selecao:
            self.btn_selecao.configure(text="✖  Cancelar",
                                        border_color=self.COR["perigo"],
                                        text_color=self.COR["perigo"])
            self.btn_exc_todos.configure(text="🗑 Excluir Sel.")
        else:
            self.btn_selecao.configure(text="☑  Selecionar",
                                        border_color=self.COR["azul"],
                                        text_color=self.COR["azul"])
            self.btn_exc_todos.configure(text="⚠ Excluir Todas")
        self._refresh_table()

    def _prep_inserir(self):
        if not self.codturma_var.get().strip():
            messagebox.showwarning("Campo obrigatório", "Digite o código da turma.")
            return
        self.acao_atual = "INSERIR"
        self._show_conf()

    def _prep_alterar(self):
        if not self.codturma_var.get().strip():
            messagebox.showwarning("Aviso", "Busque uma turma antes de alterar.")
            return
        self.acao_atual = "ALTERAR"
        self._show_conf()

    def _prep_excluir(self):
        if not self.codturma_var.get().strip():
            messagebox.showwarning("Aviso", "Insira o código da turma a excluir.")
            return
        self.acao_atual = "EXCLUIR"
        self._show_conf()

    def _show_conf(self):
        self.frame_btns.pack_forget()
        self.lbl_dica.pack_forget()
        self.frame_conf.pack(fill="x", pady=(14, 0))
        self.ent_codturma.configure(state="disabled")
        if self.acao_atual == "EXCLUIR":
            self.ent_curso.configure(state="disabled")

    def _hide_conf(self):
        self.frame_conf.pack_forget()
        self.frame_btns.pack(fill="x", pady=(14, 0))
        self.lbl_dica.pack(pady=(12, 0))
        self.ent_codturma.configure(state="normal")
        self.ent_curso.configure(state="normal")

    def _cancelar(self):
        self._reset()

    def _reset(self):
        self.codturma_var.set("")
        if self.mapa_cursos:
            self.curso_var.set(next(iter(self.mapa_cursos)))
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
    app.title("Turmas – Sistema Univap")
    app.geometry("1100x680")
    TelaCadastroTurmas(app).pack(fill="both", expand=True)
    app.mainloop()