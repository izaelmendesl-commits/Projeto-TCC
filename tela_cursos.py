import customtkinter as ctk
from tkinter import messagebox
import mysql.connector
import os
from PIL import Image

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")


class TelaCadastroCurso(ctk.CTkFrame):
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
        "sidebar":       ("#002B5C", "#001A3D"),
    }

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=self.COR["fundo"], **kwargs)

        self.codigo_var    = ctk.StringVar()
        self.descricao_var = ctk.StringVar()
        self.busca_var     = ctk.StringVar()
        self.acao_atual    = None
        self.modo_selecao  = False
        self.vars_chk      = {}

        self._build_ui()
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

    # ── Cabeçalho ───────────────────────────────
    def _build_header(self):
        hdr = ctk.CTkFrame(self, corner_radius=0,
                           fg_color=self.COR["card"],
                           border_width=1, border_color=self.COR["borda"])
        hdr.pack(fill="x")

        # Linha decorativa azul no topo
        ctk.CTkFrame(hdr, height=3, corner_radius=0,
                     fg_color=self.COR["azul"]).pack(fill="x")

        inner = ctk.CTkFrame(hdr, fg_color="transparent")
        inner.pack(fill="x", padx=28, pady=14)

        # Logo
        lbl_logo = self._make_logo(inner)
        lbl_logo.pack(side="left", padx=(0, 16))

        # Título + subtítulo
        txt_frame = ctk.CTkFrame(inner, fg_color="transparent")
        txt_frame.pack(side="left")
        ctk.CTkLabel(txt_frame, text="Gerenciamento de Cursos",
                     font=ctk.CTkFont("Segoe UI", 22, "bold"),
                     text_color=self.COR["titulo"]).pack(anchor="w")
        ctk.CTkLabel(txt_frame, text="Cadastre, edite e remova cursos do sistema",
                     font=ctk.CTkFont("Segoe UI", 12),
                     text_color=self.COR["suave"]).pack(anchor="w")

        # Seletor de tema
        ctk.CTkLabel(inner, text="Tema",
                     font=ctk.CTkFont(size=12),
                     text_color=self.COR["suave"]).pack(side="right", padx=(0, 6))
        seg = ctk.CTkSegmentedButton(
            inner, values=["☀ Claro", "🌙 Escuro"],
            width=155, height=28,
            font=ctk.CTkFont(size=12),
            fg_color=self.COR["fundo"],
            selected_color=self.COR["azul"],
            selected_hover_color=self.COR["azul_hover"],
            command=self._mudar_tema)
        seg.set("☀ Claro")
        seg.pack(side="right")

    # ── Painel esquerdo (formulário) ─────────────
    def _build_left(self, parent):
        panel = ctk.CTkFrame(parent, fg_color="transparent", width=360)
        panel.grid(row=0, column=0, sticky="nsew", padx=(0, 18))
        panel.grid_propagate(False)

        # Card do formulário
        card = ctk.CTkFrame(panel, fg_color=self.COR["card"],
                            border_width=1, border_color=self.COR["borda"],
                            corner_radius=14)
        card.pack(fill="x")

        # Faixa de título do card
        faixa = ctk.CTkFrame(card, fg_color=self.COR["azul"],
                             corner_radius=0, height=38)
        faixa.pack(fill="x")
        faixa.pack_propagate(False)
        ctk.CTkLabel(faixa, text="  📋  CADASTRO DE CURSO",
                     font=ctk.CTkFont("Segoe UI", 12, "bold"),
                     text_color="white").pack(side="left", pady=8)

        pad = {"padx": 24}

        # Código
        ctk.CTkLabel(card, text="Código do Curso",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color=self.COR["texto"]).pack(anchor="w", pady=(18, 3), **pad)

        row_cod = ctk.CTkFrame(card, fg_color="transparent")
        row_cod.pack(fill="x", **pad, pady=(0, 14))

        self.ent_codigo = ctk.CTkEntry(
            row_cod, textvariable=self.codigo_var,
            width=140, height=38, corner_radius=8,
            placeholder_text="Ex: 101",
            border_color=self.COR["borda"])
        self.ent_codigo.pack(side="left")

        ctk.CTkButton(row_cod, text="🔍 Buscar", width=110, height=38,
                      corner_radius=8,
                      fg_color=self.COR["azul"],
                      hover_color=self.COR["azul_hover"],
                      font=ctk.CTkFont(size=13, weight="bold"),
                      command=self._buscar).pack(side="left", padx=(10, 0))

        # Descrição
        ctk.CTkLabel(card, text="Descrição do Curso",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color=self.COR["texto"]).pack(anchor="w", pady=(0, 3), **pad)

        self.ent_descricao = ctk.CTkEntry(
            card, textvariable=self.descricao_var,
            width=312, height=38, corner_radius=8,
            placeholder_text="Ex: Engenharia de Computação",
            border_color=self.COR["borda"])
        self.ent_descricao.pack(anchor="w", pady=(0, 22), **pad)

        # ── Botões de ação ──
        self.frame_btns = ctk.CTkFrame(panel, fg_color="transparent")
        self.frame_btns.pack(fill="x", pady=(14, 0))

        self.btn_inserir = self._btn(self.frame_btns, " Inserir",
                                     self.COR["azul_esc"], self.COR["azul"],
                                     self._prep_inserir)
        self.btn_inserir.pack(side="left", expand=True, fill="x", padx=(0, 5))

        self.btn_alterar = self._btn(self.frame_btns, " Alterar",
                                     self.COR["azul"], self.COR["azul_hover"],
                                     self._prep_alterar)
        self.btn_alterar.pack(side="left", expand=True, fill="x", padx=5)

        self.btn_excluir = self._btn(self.frame_btns, " Excluir",
                                     self.COR["perigo"], self.COR["perigo_hov"],
                                     self._prep_excluir)
        self.btn_excluir.pack(side="left", expand=True, fill="x", padx=(5, 0))

        # Frame confirmação (oculto)
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

        # Dica de uso
        self.lbl_dica = ctk.CTkLabel(
            panel,
            text=" ",
            font=ctk.CTkFont(size=11),
            text_color=self.COR["suave"])
        self.lbl_dica.pack(pady=(12, 0))

    # ── Painel direito (tabela) ──────────────────
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

        ctk.CTkLabel(metric, text="📚  Total de Cursos Cadastrados:",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color=self.COR["suave"]).pack(side="left", padx=20)
        self.lbl_total = ctk.CTkLabel(metric, text="—",
                                       font=ctk.CTkFont(size=28, weight="bold"),
                                       text_color=self.COR["azul"])
        self.lbl_total.pack(side="right", padx=20)

        # Card da tabela
        tcard = ctk.CTkFrame(panel, fg_color=self.COR["card"],
                              border_width=1, border_color=self.COR["borda"],
                              corner_radius=14)
        tcard.grid(row=1, column=0, sticky="nsew")
        tcard.grid_rowconfigure(1, weight=1)
        tcard.grid_columnconfigure(0, weight=1)

        # Barra superior da tabela
        barra = ctk.CTkFrame(tcard, fg_color="transparent")
        barra.grid(row=0, column=0, sticky="ew", padx=20, pady=(14, 8))

        ctk.CTkLabel(barra, text="Lista Oficial de Cursos",
                     font=ctk.CTkFont(size=14, weight="bold"),
                     text_color=self.COR["texto"]).pack(side="left")

        # Botão excluir todos
        self.btn_exc_todos = ctk.CTkButton(
            barra, text="⚠ Excluir Todos", width=125, height=30,
            corner_radius=8, font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=self.COR["perigo"], hover_color=self.COR["perigo_hov"],
            command=self._excluir_todos)
        self.btn_exc_todos.pack(side="right", padx=(5, 0))

        # Botão seleção múltipla
        self.btn_selecao = ctk.CTkButton(
            barra, text="☑  Selecionar", width=120, height=30,
            corner_radius=8, font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="transparent", border_width=1,
            border_color=self.COR["azul"],
            text_color=self.COR["azul"],
            hover_color=self.COR["fundo"],
            command=self._toggle_selecao)
        self.btn_selecao.pack(side="right", padx=(0, 5))

        # Busca
        self.ent_busca = ctk.CTkEntry(
            barra, textvariable=self.busca_var,
            placeholder_text="🔍  Filtrar cursos...",
            width=200, height=30, corner_radius=8)
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

        # Cabeçalho da tabela
        cab = ctk.CTkFrame(self.scroll, fg_color="transparent")
        cab.pack(fill="x", pady=(0, 4))
        if self.modo_selecao:
            ctk.CTkLabel(cab, text="", width=30).pack(side="left")
        ctk.CTkLabel(cab, text="CÓDIGO", font=ctk.CTkFont(size=11, weight="bold"),
                     text_color=self.COR["suave"], width=90, anchor="w").pack(side="left", padx=(8, 0))
        ctk.CTkLabel(cab, text="DESCRIÇÃO DO CURSO",
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
            cur.execute("SELECT COUNT(*) FROM cursos")
            self.lbl_total.configure(text=str(cur.fetchone()[0]))

            filtro = self.busca_var.get().strip()
            if filtro:
                cur.execute(
                    "SELECT codcurso, descricao FROM cursos "
                    "WHERE CAST(codcurso AS CHAR) LIKE %s OR descricao LIKE %s ORDER BY codcurso",
                    (f"%{filtro}%", f"%{filtro}%"))
            else:
                cur.execute("SELECT codcurso, descricao FROM cursos ORDER BY codcurso")

            rows = cur.fetchall()
            if not rows:
                ctk.CTkLabel(self.scroll,
                             text="Nenhum curso encontrado.",
                             text_color=self.COR["suave"],
                             font=ctk.CTkFont(size=13)).pack(pady=40)
                return

            for i, (cod, desc) in enumerate(rows):
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

                ctk.CTkLabel(linha, text=str(cod),
                             font=ctk.CTkFont(size=13, weight="bold"),
                             text_color=self.COR["azul"],
                             width=90, anchor="w").pack(side="left", padx=(8, 0))

                ctk.CTkLabel(linha, text=str(desc),
                             font=ctk.CTkFont(size=13),
                             text_color=self.COR["texto"],
                             anchor="w").pack(side="left", padx=12, fill="x", expand=True)

        except mysql.connector.Error as e:
            print(f"[tela_cursos] Erro na tabela: {e}")
        finally:
            cur.close()
            conn.close()

    # ════════════════════════════════════════════
    #  CRUD
    # ════════════════════════════════════════════
    def _buscar(self):
        cod = self.codigo_var.get().strip()
        if not cod:
            messagebox.showwarning("Aviso", "Digite um código para buscar.")
            return
        conn = self._db()
        if not conn:
            return
        try:
            cur = conn.cursor()
            cur.execute("SELECT descricao FROM cursos WHERE codcurso = %s", (cod,))
            res = cur.fetchone()
            if res:
                self.descricao_var.set(res[0])
                self.ent_descricao.configure(border_color=self.COR["sucesso"])
                self.after(1500, lambda: self.ent_descricao.configure(border_color=self.COR["borda"]))
            else:
                self.descricao_var.set("")
                messagebox.showinfo("Código livre",
                    f"O código {cod} não existe.\nPreencha a descrição e clique em Inserir.")
        except mysql.connector.Error as e:
            messagebox.showerror("Erro SQL", str(e))
        finally:
            cur.close()
            conn.close()

    def _confirmar(self):
        cod  = self.codigo_var.get().strip()
        desc = self.descricao_var.get().strip()

        if self.acao_atual in ("INSERIR", "ALTERAR") and (not cod or not desc):
            messagebox.showwarning("Campos obrigatórios", "Preencha o código e a descrição.")
            return

        conn = self._db()
        if not conn:
            return
        try:
            cur = conn.cursor()
            if self.acao_atual == "INSERIR":
                cur.execute("INSERT INTO cursos (codcurso, descricao) VALUES (%s, %s)", (cod, desc))
                conn.commit()
                messagebox.showinfo("✅ Sucesso", "Curso cadastrado com sucesso!")
            elif self.acao_atual == "ALTERAR":
                cur.execute("UPDATE cursos SET descricao = %s WHERE codcurso = %s", (desc, cod))
                conn.commit()
                messagebox.showinfo("✅ Sucesso", "Curso atualizado com sucesso!")
            elif self.acao_atual == "EXCLUIR":
                cur.execute("DELETE FROM cursos WHERE codcurso = %s", (cod,))
                conn.commit()
                messagebox.showinfo("✅ Sucesso", "Curso removido.")
            self._reset()
            self._refresh_table()
        except mysql.connector.Error as e:
            if e.errno == 1451:
                messagebox.showwarning("Ação bloqueada",
                    "Este curso possui turmas vinculadas.\nRemova as turmas antes de excluí-lo.")
            elif e.errno == 1062:
                messagebox.showwarning("Duplicado", f"Já existe um curso com o código {cod}.")
            else:
                messagebox.showerror("Erro SQL", str(e))
        finally:
            cur.close()
            conn.close()

    def _excluir_todos(self):
        if self.modo_selecao:
            sels = [c for c, v in self.vars_chk.items() if v.get() == "on"]
            if not sels:
                messagebox.showwarning("Aviso", "Nenhum curso selecionado.")
                return
            if not messagebox.askyesno("Confirmar", f"Excluir {len(sels)} curso(s)?"):
                return
            conn = self._db()
            if not conn:
                return
            try:
                cur = conn.cursor()
                ph = ",".join(["%s"] * len(sels))
                cur.execute(f"DELETE FROM cursos WHERE codcurso IN ({ph})", tuple(sels))
                conn.commit()
                messagebox.showinfo("✅ Sucesso", f"{cur.rowcount} curso(s) removido(s).")
            except mysql.connector.Error as e:
                if e.errno == 1451:
                    messagebox.showwarning("Bloqueado",
                        "Alguns cursos possuem turmas vinculadas e não puderam ser removidos.")
                else:
                    messagebox.showerror("Erro SQL", str(e))
            finally:
                cur.close()
                conn.close()
            self._toggle_selecao()
        else:
            if not messagebox.askyesno("⚠ Atenção",
                    "Excluir TODOS os cursos?\nEsta ação não pode ser desfeita."):
                return
            conn = self._db()
            if not conn:
                return
            try:
                cur = conn.cursor()
                cur.execute("DELETE FROM cursos")
                conn.commit()
                messagebox.showinfo("✅ Concluído", f"{cur.rowcount} curso(s) removido(s).")
                self._refresh_table()
            except mysql.connector.Error as e:
                if e.errno == 1451:
                    messagebox.showwarning("Bloqueado",
                        "Existem turmas vinculadas. Remova as turmas primeiro.")
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
            self.btn_exc_todos.configure(text="🗑 Excluir Sel.",
                                          fg_color=self.COR["perigo"])
        else:
            self.btn_selecao.configure(text="☑  Selecionar",
                                        border_color=self.COR["azul"],
                                        text_color=self.COR["azul"])
            self.btn_exc_todos.configure(text="⚠ Excluir Todos",
                                          fg_color=self.COR["perigo"])
        self._refresh_table()

    def _prep_inserir(self):
        if not self.codigo_var.get().strip() or not self.descricao_var.get().strip():
            messagebox.showwarning("Campos obrigatórios", "Preencha o código e a descrição.")
            return
        self.acao_atual = "INSERIR"
        self._show_conf()

    def _prep_alterar(self):
        if not self.codigo_var.get().strip() or not self.descricao_var.get().strip():
            messagebox.showwarning("Aviso", "Busque um curso e edite os dados antes de alterar.")
            return
        self.acao_atual = "ALTERAR"
        self._show_conf()

    def _prep_excluir(self):
        if not self.codigo_var.get().strip():
            messagebox.showwarning("Aviso", "Insira o código do curso a excluir.")
            return
        self.acao_atual = "EXCLUIR"
        self._show_conf()

    def _show_conf(self):
        self.frame_btns.pack_forget()
        self.lbl_dica.pack_forget()
        self.frame_conf.pack(fill="x", pady=(14, 0))
        self.ent_codigo.configure(state="disabled")
        if self.acao_atual == "EXCLUIR":
            self.ent_descricao.configure(state="disabled")

    def _hide_conf(self):
        self.frame_conf.pack_forget()
        self.frame_btns.pack(fill="x", pady=(14, 0))
        self.lbl_dica.pack(pady=(12, 0))
        self.ent_codigo.configure(state="normal")
        self.ent_descricao.configure(state="normal")

    def _cancelar(self):
        self._reset()

    def _reset(self):
        self.codigo_var.set("")
        self.descricao_var.set("")
        self._hide_conf()
        self.acao_atual = None

    # ════════════════════════════════════════════
    #  UTILITÁRIOS
    # ════════════════════════════════════════════
    def _db(self):
        try:
            return mysql.connector.connect(
                host="localhost", user="root",
                password="IzaelMendes123", database="avisos_sistema")
        except mysql.connector.Error as e:
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
    app.title("Cursos – Sistema Univap")
    app.geometry("1100x680")
    TelaCadastroCurso(app).pack(fill="both", expand=True)
    app.mainloop()